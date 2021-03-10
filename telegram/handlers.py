import os
import csv
import base64
import rsa
import random
import datetime
from datetime import timedelta, datetime
from aiohttp import web
from telegram import sql_queries as sql
from telegram import ai
from telegram import shared
from quotes.stock_quotes_news import StockStat
from telegram import instructions as ins
from telegram import buttons
import re
from project_shared import *
from telegram.sql_queries import get_all_users
from telethon.tl.types import InputMediaPoll, Poll, PollAnswer, DocumentAttributeFilename, DocumentAttributeVideo
from telethon import functions, types
from mimetypes import guess_type
# from messages.message import *


class WebHandler:

    def __init__(self, payment_token, command_token, pubkey, client, engine):
        self.payment_token = payment_token
        self.command_token = command_token
        self.pubkey = pubkey
        self.client = client
        self.engine = engine

    # ============================== Payment request handler ======================
    # process only requests with correct payment token
    async def success_payment_handler(self, request):
        if request.match_info.get("token") == self.payment_token:
            request_json = await request.json()
            # debug("JSON:" + str(request_json))
            order_id = str(request_json['order_id'])
            summa = str(request_json['summa'])
            data = ":" + order_id + ":" + summa + ":"
            sign = base64.b64decode(str(request_json['sign']))

            if self.pubkey is None:
                return web.Response(status=403)

            try:
                rsa.verify(data.encode(), sign, self.pubkey)
            except:
                debug("Verification failed")
                return web.Response(status=403)

            value = shared.ORDER_MAP.get(order_id)
            if value is not None:
                debug("Send message \"payment is ok\"")
                sender_id, message_id = value
                # удаляем платежное сообщение в чате, чтобы клиент не нажимал на него еще
                await self.client.delete_messages(sender_id, message_id)
                # сообщаем клиенту об успешном платеже
                tariff_str = ""
                td = ""
                subscribe_level = ""
                if summa == "15":
                    tariff_str = '__Тариф: ' + shared.SUBSCRIBES[shared.TARIFF_START_ID].get_name() + '__\n'
                    td = timedelta(days=shared.SUBSCRIBES[shared.TARIFF_START_ID].get_duration())
                    subscribe_level = shared.SUBSCRIBES[shared.TARIFF_START_ID].get_level()
                elif summa == "25":
                    tariff_str = '__Тариф: ' + shared.SUBSCRIBES[shared.TARIFF_BASE_ID].get_name() + '__\n'
                    td = timedelta(days=shared.SUBSCRIBES[shared.TARIFF_BASE_ID].get_duration())
                    subscribe_level = shared.SUBSCRIBES[shared.TARIFF_BASE_ID].get_level()
                elif summa == "30":
                    tariff_str = '__Тариф: ' + shared.SUBSCRIBES[shared.TARIFF_ADVANCED_ID].get_name() + '__\n'
                    td = timedelta(days=shared.SUBSCRIBES[shared.TARIFF_ADVANCED_ID].get_duration())
                    subscribe_level = shared.SUBSCRIBES[shared.TARIFF_ADVANCED_ID].get_level()
                elif summa == "40":
                    tariff_str = '__Тариф: ' + shared.SUBSCRIBES[shared.TARIFF_PROFESSIONAL_ID].get_name() + '__\n'
                    td = timedelta(days=shared.SUBSCRIBES[shared.TARIFF_PROFESSIONAL_ID].get_duration())
                    subscribe_level = shared.SUBSCRIBES[shared.TARIFF_PROFESSIONAL_ID].get_level()
                await self.client.send_message(sender_id,
                                               'Оплата прошла успешно:\n'
                                               + tariff_str
                                               + '__Ордер: ' + order_id + '__\n'
                                               + '__Сумма: ' + summa + '__\n'
                                               + '**Спасибо, что пользуетесь моими услугами!**')
                # удаляем данные о платеже из памяти и из базы, они нам больше не нужны
                shared.ORDER_MAP.pop(order_id)
                await sql.delete_from_payment_message(order_id, self.engine)

                # добавляем запись в базу о том  когда закончится подписка
                expired_data = (datetime.now() + td).isoformat(timespec='minutes')
                await sql.db_save_expired_data(expired_data, subscribe_level, sender_id, self.engine)
                return web.Response(status=200)
            else:
                debug("Global SenderID is None")
                return web.Response(status=403)
        elif request.match_info.get("token") == self.command_token:
            debug(f'Received cmd token!')
            res_ack = {'result': 'ACK'}
            res_nack = {'result': 'NACK'}
            request_json = await request.json()
            debug(f'request_json:{request_json}')
            action = str(request_json['action'])
            value = str(request_json['value'])
            if action == "send_to":
                debug(f'Action = send_to')
                toid = request_json.get("id", None)
                if toid is not None and check_int(toid):
                    toid = int(toid)
                if value == "sac_pies":
                    debug(f'Value = sac_pies')
                    res = await send_sac_pie(self.client, toid)
                    if res:
                        return web.json_response(res_ack)
                if value == "message":
                    debug(f'Value = message')
                    msg = request_json.get("msg", None)
                    res = await send_to_message(self.client, toid, msg)
                    if res:
                        return web.json_response(res_ack)
                if value == "broadcast_message":
                    debug(f'Value = broadcast_message')
                    msg = request_json.get("msg", None)
                    res = await send_broadcast_message(self.client, self.engine, msg)
                    if res:
                        return web.json_response(res_ack)
            return web.json_response(res_nack)


def set_route(app, payment_token, command_tiken, pubkey, client, engine):
    web_handler = WebHandler(payment_token, command_tiken, pubkey, client, engine)
    app.router.add_post("/{token}/", web_handler.success_payment_handler)


# ============================== Commands ===============================

async def send_to_handler(event, client_, owner=None):
    parse = str(event.text).split('|')
    try:
        sender_id = event.input_sender
    except ValueError as e:
        sender_id = await event.get_input_sender()
    try:
        if int(sender_id.user_id) == int(owner):
            entity = await client_.get_entity(int(parse[1]))
            await client_.send_message(entity, parse[2])
        else:
            await client_.send_message(sender_id, 'Order dismissed!')
    except ValueError as e:
        debug(e, 'Some errors from send_to()')


async def publish_to_handler(event, client_, owner=None):
    parse = str(event.text).split('|')
    try:
        channel = await client_.get_entity('https://t.me/' + str(parse[1]))
    except ValueError as e:
        debug(e, 'Can\'t get channel entity')
    try:
        if int(event.input_sender.user_id) == int(owner):
            await client_.send_message(channel, parse[2])
        else:
            await client_.send_message(event.input_sender, 'Order dismissed!')
    except ValueError as e:
        debug(e, 'Some errors from publish_to()')


async def dialog_flow_handler(event, client_):
    msg_text = event.message.text
    if msg_text == '' or msg_text is None:
        msg = 'Я воспринимаю только текст и ничего кроме текста.'
        await client_.send_message(event.input_sender, msg)
    else:
        no_match = ['\U0001F9D0', '\U0001F633', 'Ясно', 'Мы должны подумать над этим']
        fallback = random.choice(no_match)
        try:
            sender_id = event.input_sender
        except ValueError as e:
            sender_id = await event.get_input_sender()
        if ins.pattern.search(event.text) is None:
            user_message = event.text
            project_id = 'common-bot-1'
            try:
                dialogflow_answer = ai.detect_intent_texts(project_id, sender_id.user_id, user_message, 'ru-RU')
                await client_.send_message(sender_id, dialogflow_answer)
                await client_.send_message(-1001262211476, str(sender_id.user_id) +
                                           '  \n' + str(event.text) +
                                           '  \n' + dialogflow_answer)
                # TODO Внимание! изменить айди чата при деплое
            except ValueError as e:
                debug(e, 'Dialogflow response failure')
                await client_.send_message(sender_id, fallback)


async def quotes_to_handler(event, client_, limit=20):
    parse = str(event.text)
    parse = re.split('/q |#|@|\$', parse)
    # print(parse)
    stock = parse[1]
    stock = stock.upper()
    message1 = await client_.send_message(event.input_sender, message='Получаю описание, ожидайте...')
    message2 = await client_.send_message(event.input_sender, message='Рассчитываю ключевые статистики, ожидайте...')
    message3 = await client_.send_message(event.input_sender, message='Строю скоринг, ожидайте...')
    img_path = os.path.join('results/ticker_stat', f'{stock}.png')
    ss = StockStat(stock=stock)
    ss.stock_download()
    if ss.returns is not None:
        ss.stock_snapshot()
        msg2 = ss.stock_stat()
    else:
        msg2 = 'Нет данных для данного тикера'

    get = ss.stock_description_v2()
    if get[0] or get[1] is not None:
        msg1 = get[0]
        msg3 = get[1]
    else:
        msg1 = 'Нет данных для данного тикера'
        msg3 = msg1

    await client_.edit_message(message1, msg1)
    await client_.edit_message(message2, msg2)
    await client_.edit_message(message3, '__Оценка Ипсилона:__ ' + '\n' + msg3 + '\n \n ' +
                               '\U00002757 Как использовать скоринг? - \n /instruction28')
    await client_.send_file(event.input_sender, img_path)
    os.remove(img_path)


async def news_to_handler(event, client_, limit=20):
    parse = str(event.text).split(' ')
    stock = parse[1]
    ss = StockStat(stock=stock)
    try:
        msg = ss.stock_news()
    except Exception as e4:
        debug(e4)
        msg = 'Новости недоступны'
    await client_.send_message(event.input_sender, f'Последние новости с упоминанием {stock}')
    await client_.send_message(event.input_sender, msg)


async def about_handler(event, client_):
    await client_.send_message(event.input_sender, ins.about)


async def goals_handler(event, client_):
    await client_.send_message(event.input_sender, ins.goals)


async def skills_handler(event, client_):
    await client_.send_message(event.input_sender, ins.skills)


async def future_handler(event, client_):
    await client_.send_message(event.input_sender, ins.future)


async def support_handler(event, client_):
    # await client_.send_message(-1001262211476, str(event.input_sender) +
    #                            '  \n' + str(event.text))
    await client_.forward_messages(-1001262211476, event.message)
    await client_.send_message(event.input_sender, 'Сообщение успешно отправлено. Спасибо!')


async def instructions_handler(event, client_):
    pattern = event.original_update.message.message
    pattern = str(pattern).strip('/')
    if pattern == 'instruction00':
        await client_.send_message(event.input_sender, ins.instruction00)
    elif pattern == 'instruction01':
        await client_.send_message(event.input_sender, ins.instruction01)
    elif pattern == 'instruction02':
        await client_.send_message(event.input_sender, ins.instruction02)
    elif pattern == 'instruction03':
        await client_.send_message(event.input_sender, ins.instruction03)
    elif pattern == 'instruction04':
        await client_.send_message(event.input_sender, ins.instruction04)
    elif pattern == 'instruction05':
        await client_.send_message(event.input_sender, ins.instruction05)
    elif pattern == 'instruction06':
        await client_.send_message(event.input_sender, ins.instruction06)
    elif pattern == 'instruction07':
        await client_.send_message(event.input_sender, ins.instruction07)
    elif pattern == 'instruction08':
        await client_.send_message(event.input_sender, ins.instruction08)
    elif pattern == 'instruction09':
        await client_.send_message(event.input_sender, ins.instruction09)
    elif pattern == 'instruction10':
        await client_.send_message(event.input_sender, ins.instruction10)
    elif pattern == 'instruction11':
        await client_.send_message(event.input_sender, ins.instruction11)
    elif pattern == 'instruction12':
        await client_.send_message(event.input_sender, ins.instruction12)
    elif pattern == 'instruction13':
        await client_.send_message(event.input_sender, ins.instruction13)
    elif pattern == 'instruction14':
        await client_.send_message(event.input_sender, ins.instruction14)
    elif pattern == 'instruction15':
        await client_.send_message(event.input_sender, ins.instruction15)
    elif pattern == 'instruction16':
        await client_.send_message(event.input_sender, ins.instruction16)
    elif pattern == 'instruction17':
        await client_.send_message(event.input_sender, ins.instruction17)
    elif pattern == 'instruction18':
        await client_.send_message(event.input_sender, ins.instruction18)
    elif pattern == 'instruction19':
        await client_.send_message(event.input_sender, ins.instruction19)
    elif pattern == 'mindepo':
        await client_.send_message(event.input_sender, ins.mindepo)
    elif pattern == 'managers_form':
        await client_.send_message(event.input_sender, ins.managers_form)
    elif pattern == 'instruction20':
        await client_.send_message(event.input_sender, ins.instruction20)
    elif pattern == 'instruction21':
        await client_.send_message(event.input_sender, ins.instruction21)
    elif pattern == 'instruction22':
        await client_.send_message(event.input_sender, ins.instruction22)
    elif pattern == 'instruction23':
        await client_.send_message(event.input_sender, ins.instruction23)
    elif pattern == 'instruction24':
        await client_.send_message(event.input_sender, ins.instruction24)
    elif pattern == 'instruction25':
        await client_.send_message(event.input_sender, ins.instruction25)
    elif pattern == 'instruction26':
        await client_.send_message(event.input_sender, ins.instruction26)
    elif pattern == 'instruction27':
        await client_.send_message(event.input_sender, ins.instruction27)
    elif pattern == 'instruction28':
        await client_.send_message(event.input_sender, ins.instruction28)


async def portfolio_candle_chart_handler(event, client_):
    pattern = event.original_update.message.message
    pattern = str(pattern).strip('/').split('_')[1]
    if pattern == 'parking':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'parking_port_chart_over_TLT.png',
                                buttons=buttons.keyboard_a2)
    elif pattern == 'allweather':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'allweather_port_chart_over_SPY.png',
                                buttons=buttons.keyboard_a2)
    elif pattern == 'balanced':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'balanced_port_chart_over_QQQ.png',
                                buttons=buttons.keyboard_a2)
    elif pattern == 'aggressive':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'aggressive_port_chart_over_QQQ.png',
                                buttons=buttons.keyboard_a2)
    elif pattern == 'leveraged':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'leveraged_port_chart_over_QQQ.png',
                                buttons=buttons.keyboard_a2)
    elif pattern == 'elastic':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'elastic_port_chart_over_QQQ.png',
                                buttons=buttons.keyboard_a2)
    elif pattern == 'yolo':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'yolo_port_chart_over_SPY.png',
                                buttons=buttons.keyboard_a2)


async def managers_form_handler(event, client_):
    # msg_text = event.message.text
    sender_id = await event.get_input_sender()
    user_message = event.text
    await client_.send_message(sender_id, 'Запрос на регистрацию принят')
    await client_.send_message(-1001262211476, str(sender_id.user_id) + '  \n' + str(user_message))


async def send_sac_pie(clnt, toid):
    debug('send_sac_pie')
    try:
        entity = await clnt.get_entity(toid)
        debug(f'entity={entity}')
        user_message = f'Ежемесячное обновление аллокаций портфелей'
        await clnt.send_message(entity, user_message)
        await clnt.send_file(entity, CHARTER_IMAGES_PATH + 'sac_parking_portfolio_pie.png')
        await clnt.send_file(entity, CHARTER_IMAGES_PATH + 'sac_balanced_portfolio_pie.png')
        await clnt.send_file(entity, CHARTER_IMAGES_PATH + 'sac_growth_portfolio_pie.png')
        return True
    except Exception as e:
        debug(e, ERROR)
        return False


async def send_to_message(clnt, toid, msg):
    try:
        await clnt.send_message(toid, msg)
        return True
    except Exception as e:
        debug(e, ERROR)
        return False


async def send_broadcast_message(clnt, engine, msg):
    users = await get_all_users(engine)
    succsess_message_log = "messages_send.log"
    fail_message_log = "messages_fail.log"
    sfname = f'{LOGS_PATH}{succsess_message_log}'
    ffname = f'{LOGS_PATH}{fail_message_log}'
    bufsize = 1
    sm_log_file = open(sfname, "a", buffering=bufsize)
    fm_log_file = open(ffname, "a", buffering=bufsize)
    fdt = datetime.datetime.now()
    sm_log_file.write(f'[{fdt.strftime("%H:%M:%S")}]:***************** Start send new message *****************\n')
    fm_log_file.write(f'[{fdt.strftime("%H:%M:%S")}]:***************** Start send new message *****************\n')
    # msg_id = save_message(msg, '', fdt, SIMPLE_MESSAGE_TYPE)
    sent_users_dict = {}
    fail_users_dict = {}
    for user_id in users:
        try:
            await clnt.send_message(user_id, msg)
            dt = datetime.datetime.now()
            sm_log_file.write(f'[{dt.strftime("%H:%M:%S")}]:{user_id}\n')
            sent_users_dict[user_id] = dt
        except Exception as e:
            debug(e, ERROR)
            dt = datetime.datetime.now()
            fm_log_file.write(f'[{dt.strftime("%H:%M:%S")}]:{user_id}\n')
            fail_users_dict[user_id] = dt
    # update_mailing_lists(msg_id, sent_users_dict, fail_users_dict, {})
    sm_log_file.close()
    fm_log_file.close()
    return True


async def send_broadcast_poll(clnt):
    # _question = "Вы хотите что бы мы сделели более глубокий анализ по акциям?"
    # _poll_id = get_next_id()
    # _answers = [PollAnswer('Yes', b'1'), PollAnswer('No', b'2')]
    # _answersdict = {"Yes": 1, "No": 2}
    # poll = Poll(id=_poll_id,
    #             question=_question,
    #             answers=_answers)
    # input_nedia_poll = InputMediaPoll(poll)
    # users = await get_all_users(engine)
    # succsess_message_log = "messages_send.log"
    # fail_message_log = "messages_fail.log"
    # sfname = f'{LOGS_PATH}{succsess_message_log}'
    # ffname = f'{LOGS_PATH}{fail_message_log}'
    # bufsize = 1
    # sm_log_file = open(sfname, "a", buffering=bufsize)
    # fm_log_file = open(ffname, "a", buffering=bufsize)
    # fdt = datetime.datetime.now()
    # sm_log_file.write(f'[{fdt.strftime("%H:%M:%S")}]:***************** Start send new poll *****************\n')
    # fm_log_file.write(f'[{fdt.strftime("%H:%M:%S")}]:***************** Start send new poll *****************\n')
    # # msgdict = {"Question": _question, _answersdict}
    # # msg_id = save_message(msgdict, '', fdt, POLL_MESSAGE_TYPE)
    # sent_users_dict = {}
    # fail_users_dict = {}
    # for user_id in users:
    #     try:
    #         await clnt.send_message(user_id, file=input_nedia_poll)
    #         dt = datetime.datetime.now()
    #         sm_log_file.write(f'[{dt.strftime("%H:%M:%S")}]:{user_id}\n')
    #         sent_users_dict[user_id] = dt
    #     except Exception as e:
    #         debug(e, ERROR)
    #         dt = datetime.datetime.now()
    #         fm_log_file.write(f'[{dt.strftime("%H:%M:%S")}]:{user_id}\n')
    #         fail_users_dict[user_id] = dt
    # # update_mailing_lists(msg_id, sent_users_dict, fail_users_dict, {})
    # sm_log_file.close()
    # fm_log_file.close()
    return True


    # results = await clnt.send_message(toid, file=InputMediaPoll(
    #     poll=Poll(
    #         id=53453159,
    #         question="Вы хотите что бы мы сделели более глубокий анализ по акциям?",
    #         answers=[PollAnswer('Yes', b'1'), PollAnswer('No', b'2')])))
    # debug(f"Result:{results}")
