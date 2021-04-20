import importlib
import os
import csv
import base64
import rsa
import random
import time
import uuid
from fastnumbers import *

from datetime import timedelta, datetime
from aiohttp import web
from telethon import errors as terr

from charter.finance2 import create_revenue_histogram
from quotes import sql_queries as qsql
from quotes import eodhistoricaldata as eod
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
from messages.message import *
from payments.payagregator import PaymentAgregator
from telethon import utils

PAYMENT_AGGREGATOR = None
PAYMENT_AGGREGATOR_TIMER = None


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

            value = shared.get_order_data(order_id)
            if value is not None:
                debug("Send message \"payment is ok\"")
                debug(f'Before agregate payment: shared.ORDER_MAP=')
                shared.print_order_map()
                sender_id, message_id, order_type = value
                debug(f'Shared data by order_id: '
                      f'sender_id:[{sender_id}], message_id:[{message_id}], order_type:[{order_type}]')
                if order_type == 'subscription' or order_type == 'replenishment':
                    # Подгрузим динамически модуль - вдруг ценообразование изменилось?!
                    pricing = None
                    if "telegram.pricing" in sys.modules:
                        debug(f'module imported --- try reload')
                        pricing = importlib.reload(sys.modules["telegram.pricing"])
                    else:
                        debug(f'module NOT imported --- try first import')
                        pricing = importlib.import_module("telegram.pricing")

                    # расчитываем и сохраняем количество доступных запросов
                    summ = fast_float(summa, 0)
                    await pricing.calc_save_balance(sender_id, summ)
                    await sql.save_payment_data(sender_id, order_id, summ)

                    # удаляем платежное сообщение в чате, чтобы клиент не нажимал на него еще
                    if sender_id is not None and message_id is not None:
                        try:
                            await self.client.delete_messages(sender_id, message_id)
                        except Exception as e:
                            debug(e, ERROR)

                    # сообщаем клиенту об успешном платеже
                    await self.client.send_message(sender_id,
                                                   'Оплата прошла успешно:\n'
                                                   + '__Ордер: ' + order_id + '__\n'
                                                   + '__Сумма: ' + summa + '__\n'
                                                   + '**Спасибо, что пользуетесь моими услугами!**')
                    # удаляем данные о платеже из памяти и из базы, они нам больше не нужны
                    shared.pop_old_order(order_id)
                    await sql.delete_from_payment_message(order_id, self.engine)
                    debug(f'After agregate payment: shared.ORDER_MAP=')
                    shared.print_order_map()
                    return web.Response(status=200)
                elif order_type == 'donate':
                    # удаляем платежное сообщение в чате, чтобы клиент не нажимал на него еще
                    if sender_id is not None and message_id is not None:
                        try:
                            await self.client.delete_messages(sender_id, message_id)
                        except Exception as e:
                            debug(e, ERROR)
                    # сообщаем клиенту об успешном платеже
                    await self.client.send_message(sender_id,
                                                   'Оплата прошла успешно:\n'
                                                   + '__Ордер: ' + order_id + '__\n'
                                                   + '__Сумма: ' + summa + '__\n'
                                                   + '**Спасибо, что пользуешься моими услугами!**')
                    # удаляем данные о платеже из памяти и из базы, они нам больше не нужны
                    shared.pop_old_order(order_id)
                    await sql.delete_from_payment_message(order_id, self.engine)
                    if not is_table_exist(DONATE_DATA_TABLE_NAME):
                        await sql.create_donate_data_table(self.engine)
                    await sql.save_donate_data(sender_id, fast_float(summa))
                    debug(f'After agregate payment: shared.ORDER_MAP=')
                    shared.print_order_map()
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
                if value == "broadcast_poll":
                    debug(f'Value = broadcast_poll')
                    msg = request_json.get("msg", None)
                    res = await send_broadcast_poll(self.client)
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
            await flow_cheker(client_, event)
            user_message = event.text
            project_id = 'common-bot-1'
            try:
                dialogflow_answer = ai.detect_intent_texts(project_id, sender_id.user_id, user_message, 'ru-RU')
                await client_.send_message(sender_id, dialogflow_answer)
                usr_data = ''
                if event.message.sender.username:
                    usr_data = f'{event.message.sender.username}'
                else:
                    if event.message.sender.first_name:
                        usr_data += f'{event.message.sender.first_name} '
                    if event.message.sender.last_name:
                        usr_data += f'{event.message.sender.last_name}'
                await client_.send_message(-1001262211476,
                                           f'{sender_id.user_id} - {usr_data}\n'
                                           f'{event.text}\n'
                                           f'{dialogflow_answer}')
                # TODO Внимание! изменить айди чата при деплое
            except ValueError as e:
                debug(e, 'Dialogflow response failure')
                await client_.send_message(sender_id, fallback)


async def quotes_to_handler(event, client_, limit=20):
    await flow_cheker(client_, event)
    # Подгрузим динамически модуль - вдруг ценообразование изменилось?!
    pricing = None
    if "telegram.pricing" in sys.modules:
        debug(f'module imported --- try reload')
        pricing = importlib.reload(sys.modules["telegram.pricing"])
    else:
        debug(f'module NOT imported --- try first import')
        pricing = importlib.import_module("telegram.pricing")

    pricing_result = await pricing.check_request_amount(event.input_sender.user_id, client_)
    if not pricing_result["result"]:
        return

    parse = str(event.text)
    parse = re.split('^[#@$]', parse)
    # print(parse)
    stock = parse[1]
    stock = stock.upper()
    await client_.send_message(event.input_sender, message='\U000026A0 \n__Выбирая отдельные акции '
                                                           'следует придерживаться стратегии, учитывать возможные '
                                                           'риски и последствия, а также придерживаться разумной '
                                                           'диверсификации и аллокации__' + '\n\n' +
                               '\U00002757 Как построен рейтинг? - /instruction28' + '\n'
                               '\U00002757\U00002757 Как использовать рейтинг? - /instruction34')
    message1 = await client_.send_message(event.input_sender, message='Получаю описание \U000023F3')
    message2 = await client_.send_message(event.input_sender, message='Провожу финансовый анализ \U000023F3')
    message3 = await client_.send_message(event.input_sender, message='Провожу статистический анализ \U000023F3')

    path = f'{PROJECT_HOME_DIR}/results/ticker_stat/'
    img_path = f'{path}{stock}.png'

    ss = StockStat(stock=stock)
    ss.stock_download()

    sma_sig = ss.higher_sma8()

    get = ss.stock_description_v3()
    if get[0] or get[1] or get[2] is not None:
        msg1 = get[0]
        msg2 = get[1]
        msg3 = get[2]
        msg2 = msg2.replace('\n\n\n\n', '\n')
        msg2 = msg2.replace('\n\n\n', '\n')
    else:
        msg1 = 'Нет данных для данного тикера'
        msg2 = msg1
        msg3 = get[2]
        # вернем баланс в случае если тикер не найден или это ETF
        if pricing_result['Paid'] > 0:
            await sql.increment_paid_request_amount(event.input_sender.user_id, pricing_result['Paid'])
        if pricing_result['Free'] > 0:
            await sql.increment_free_request_amount(event.input_sender.user_id, pricing_result['Free'])

    revenue_data = None
    if len(get) == 4:
        revenue_data = get[3]
        debug(f'revenue_data = {revenue_data}!!!!!!')

    if ss.returns is not None:
        ss.stock_snapshot()
        if msg3 is not None:
            msg4 = ss.stock_stat_v3(rank_type=msg3['other'], rank=msg3['rank'], sma_sig=sma_sig)
        else:
            msg4 = 'Нет данных для данного тикера'
    else:
        msg4 = 'Нет данных для данного тикера'
    await client_.edit_message(message1, msg1)
    await client_.edit_message(message2, '__Оценка Ипсилона:__ ' + '\n' + msg2)
    await client_.edit_message(message3, msg4)

    if os.path.exists(img_path):
        add_watermark(img_path, img_path, 64, wtermark_color=(217, 217, 217, 50))
        await client_.send_file(event.input_sender, img_path)
        os.remove(img_path)

    if revenue_data is not None and len(revenue_data) != 0:
        create_revenue_histogram(stock, revenue_data, path)

    revenue_hist_path = f'{path}revenue_{stock}.png'
    if os.path.exists(revenue_hist_path):
        await client_.send_file(event.input_sender, revenue_hist_path)
        os.remove(revenue_hist_path)


async def news_to_handler(event, client_, limit=20):
    await flow_cheker(client_, event)
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


async def goals_handler(event, client_):
    await flow_cheker(client_, event)
    await client_.send_message(event.input_sender, ins.goals)


async def skills_handler(event, client_):
    await flow_cheker(client_, event)
    await client_.send_message(event.input_sender, ins.skills)


async def support_handler(event, client_):
    await flow_cheker(client_, event)
    await client_.forward_messages(-1001262211476, event.message)
    await client_.send_message(event.input_sender, 'Сообщение успешно отправлено. Спасибо!')


async def instructions_handler(event, client_):
    await flow_cheker(client_, event)
    pattern = event.original_update.message.message
    pattern = str(pattern).strip('/')
    if pattern == 'instruction00':
        await client_.send_message(event.input_sender, ins.instruction00, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction01':
        await client_.send_message(event.input_sender, ins.instruction01, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction02':
        await client_.send_message(event.input_sender, ins.instruction02, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction03':
        await client_.send_message(event.input_sender, ins.instruction03, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction04':
        await client_.send_message(event.input_sender, ins.instruction04, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction05':
        await client_.send_message(event.input_sender, ins.instruction05, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction06':
        await client_.send_message(event.input_sender, ins.instruction06, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction07':
        await client_.send_message(event.input_sender, ins.instruction07, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction08':
        await client_.send_message(event.input_sender, ins.instruction08, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction09':
        await client_.send_message(event.input_sender, ins.instruction09, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction10':
        await client_.send_message(event.input_sender, ins.instruction10, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction11':
        await client_.send_message(event.input_sender, ins.instruction11, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction12':
        await client_.send_message(event.input_sender, ins.instruction12, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction13':
        await client_.send_message(event.input_sender, ins.instruction13, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction14':
        await client_.send_message(event.input_sender, ins.instruction14, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction15':
        await client_.send_message(event.input_sender, ins.instruction15, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction16':
        await client_.send_message(event.input_sender, ins.instruction16, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction17':
        await client_.send_message(event.input_sender, ins.instruction17, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction18':
        await client_.send_message(event.input_sender, ins.instruction18, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction19':
        await client_.send_message(event.input_sender, ins.instruction19, buttons=buttons.keyboard_0_back)
    elif pattern == 'mindepo':
        await client_.send_message(event.input_sender, ins.mindepo, buttons=buttons.keyboard_0_back)
    elif pattern == 'managers_form':
        await client_.send_message(event.input_sender, ins.managers_form, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction20':
        await client_.send_message(event.input_sender, ins.instruction20, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction21':
        await client_.send_message(event.input_sender, ins.instruction21, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction22':
        await client_.send_message(event.input_sender, ins.instruction22, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction23':
        await client_.send_message(event.input_sender, ins.instruction23, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction24':
        await client_.send_message(event.input_sender, ins.instruction24, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction25':
        await client_.send_message(event.input_sender, ins.instruction25, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction26':
        await client_.send_message(event.input_sender, ins.instruction26, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction27':
        await client_.send_message(event.input_sender, ins.instruction27, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction28':
        await client_.send_message(event.input_sender, ins.instruction28, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction29':
        await client_.send_message(event.input_sender, ins.instruction29, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction30':
        await client_.send_message(event.input_sender, ins.instruction30, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction31':
        await client_.send_message(event.input_sender, ins.instruction31, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction32':
        await client_.send_message(event.input_sender, ins.instruction32, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction33':
        await client_.send_message(event.input_sender, ins.instruction33, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction34':
        await client_.send_message(event.input_sender, ins.instruction34, buttons=buttons.keyboard_0_back)
    elif pattern == 'instruction35':
        await client_.send_message(event.input_sender, ins.instruction35, buttons=buttons.keyboard_0_back)


async def portfolio_candle_chart_handler(event, client_):
    await flow_cheker(client_, event)
    pattern = event.original_update.message.message
    pattern = str(pattern).strip('/').split('_')[1]
    if pattern == 'parking':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'parking_port_chart_over_TLT.png',
                                buttons=buttons.keyboard_historical_tests)
    elif pattern == 'allweather':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'allweather_port_chart_over_SPY.png',
                                buttons=buttons.keyboard_historical_tests)
    elif pattern == 'balanced':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'balanced_port_chart_over_QQQ.png',
                                buttons=buttons.keyboard_historical_tests)
    elif pattern == 'aggressive':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'aggressive_port_chart_over_QQQ.png',
                                buttons=buttons.keyboard_historical_tests)
    elif pattern == 'leveraged':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'leveraged_port_chart_over_QQQ.png',
                                buttons=buttons.keyboard_historical_tests)
    elif pattern == 'elastic':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'elastic_port_chart_over_QQQ.png',
                                buttons=buttons.keyboard_historical_tests)
    elif pattern == 'yolo':
        await client_.send_message(event.input_sender, 'Чарт обновляется ежедневно в 11:00 (МСК)')
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'yolo_port_chart_over_SPY.png',
                                buttons=buttons.keyboard_historical_tests)


async def managers_form_handler(event, client_):
    await flow_cheker(client_, event)
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
    msg_id = save_message(msg, '', fdt, SIMPLE_MESSAGE_TYPE)
    sent_users_dict = {}
    fail_users_dict = {}
    for user_id in users:
        try:
            await clnt.send_message(user_id, msg)
            dt = datetime.datetime.now()
            sm_log_file.write(f'[{dt.strftime("%H:%M:%S")}]:{user_id}\n')
            sent_users_dict[user_id] = dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            debug(e, ERROR)
            dt = datetime.datetime.now()
            fm_log_file.write(f'[{dt.strftime("%H:%M:%S")}]:{user_id}\n')
            fail_users_dict[user_id] = dt.strftime("%Y-%m-%d %H:%M:%S")
    update_mailing_lists(msg_id, sent_users_dict, fail_users_dict, {})
    sm_log_file.close()
    fm_log_file.close()
    return True


async def send_broadcast_poll(clnt):
    _question = "Какой функционал более интересен, необходим тебе?"
    _poll_id = get_next_id()
    _answers = [PollAnswer('Инспектор риска', b'1'),
                PollAnswer('Upsilon Radar', b'2'),
                PollAnswer('Топ10 тикеров', b'3'),
                PollAnswer('Ничего из перечисленного не интересует', b'4')]
    _answersdict = {"Инспектор риска": 1,
                    "Upsilon Radar": 2,
                    "Топ10 тикеров": 3,
                    "Ничего из перечисленного не интересует": 4}
    poll = Poll(id=_poll_id,
                question=_question,
                answers=_answers)
    input_media_poll = InputMediaPoll(poll)
    users = await get_all_users(engine)
    succsess_message_log = "messages_send.log"
    fail_message_log = "messages_fail.log"
    sfname = f'{LOGS_PATH}{succsess_message_log}'
    ffname = f'{LOGS_PATH}{fail_message_log}'
    bufsize = 1
    sm_log_file = open(sfname, "a", buffering=bufsize)
    fm_log_file = open(ffname, "a", buffering=bufsize)
    fdt = datetime.datetime.now()
    sm_log_file.write(f'[{fdt.strftime("%H:%M:%S")}]:***************** Start send new poll *****************\n')
    fm_log_file.write(f'[{fdt.strftime("%H:%M:%S")}]:***************** Start send new poll *****************\n')
    msgdict = {"question": _question, "answers": _answersdict}
    msg_id = save_message(msgdict, '', fdt, POLL_MESSAGE_TYPE)
    sent_users_dict = {}
    fail_users_dict = {}
    for user_id in users:
        try:
            pll = await clnt.send_message(user_id, file=input_media_poll)
            real_poll_id = pll.media.poll.id
            debug(f'user_id:{user_id}  poll_id:{real_poll_id}', WARNING)
            dt = datetime.datetime.now()
            sm_log_file.write(f'[{dt.strftime("%H:%M:%S")}]:{user_id}\n')
            sent_users_dict[user_id] = dt.strftime("%Y-%m-%d %H:%M:%S")
            save_user_poll_map(user_id, real_poll_id, msg_id)
        except Exception as e:
            debug(e, ERROR)
            dt = datetime.datetime.now()
            fm_log_file.write(f'[{dt.strftime("%H:%M:%S")}]:{user_id}\n')
            fail_users_dict[user_id] = dt.strftime("%Y-%m-%d %H:%M:%S")
    update_mailing_lists(msg_id, sent_users_dict, fail_users_dict, {})
    sm_log_file.close()
    fm_log_file.close()
    return True


async def flow_cheker(client, event):
    # 1. Если недопрошли  опрос - сбросить
    # 2. Если было какое-то запомненное сообщение на редактирование - сбросить и удалить сообщение
    sender_id = event.input_sender.user_id
    if not is_user_profile_done(sender_id):
        reset_user_profiler_data(sender_id)
    await shared.delete_old_message(client, sender_id)
    shared.pop_old_msg_poll(sender_id)


async def portfolios_cmd(client, event):
    sender_id = event.input_sender.user_id
    await flow_cheker(client, event)
    msg = await client.send_message(event.input_sender, 'Портфели', buttons=buttons.keyboard_historical_tests)
    await shared.save_old_message(sender_id, msg)


async def inspector_to_handler(event, client_):
    sender_id = event.input_sender.user_id
    await client_.delete_messages(sender_id, event.message.id)
    regex = r"^\![a-zA-Z]{1,5} ((\d*[\%]?$)|(\d*(?!\.$)\.?\d{1,2}\%$))"
    parse = str(event.text)
    match = re.match(regex, parse)
    parse = re.split('!', parse)
    parse = parse[1]
    parse = re.split(' ', parse)
    stock = ''
    size = ''
    if match is not None and len(parse) == 2 and len(parse[0]) <= 5:
        stock, size = parse[0], parse[1]
        stock = stock.upper()
        is_percent = size.endswith('%')
        size_value = 0.0
        if is_percent:
            size_value = fast_float(re.split('%', size)[0], None)
        else:
            size_value = fast_int(size, None)

        now = datetime.datetime.now()
        start_date = add_months(now, -13)
        spy_bars_amount = qsql.get_bars_amount('SPY', start_date=start_date)
        is_error = False
        if is_percent:
            if size_value > 0.0:
                ticker_bars_amount = eod.get_bars_amount(stock, start_date, now)
                if ticker_bars_amount < spy_bars_amount:
                    debug(f'spy_bars_amount={spy_bars_amount}  ticker_bars_amount={ticker_bars_amount}')
                    msg = f'По этому тикеру не достаточно данных для анализа.'
                    is_error = True
                else:
                    msg = f'Ты ввёл тикер {stock} в размере {size} Long?'
            else:
                msg = f'{stock} {size} позиция не будет сохранена, нажмите кнопку исправить'
                is_error = True
        else:
            if size_value > 0:
                ticker_bars_amount = eod.get_bars_amount(stock, start_date, now)
                if ticker_bars_amount < spy_bars_amount:
                    debug(f'spy_bars_amount={spy_bars_amount}  ticker_bars_amount={ticker_bars_amount}')
                    msg = f'По этому тикеру не достаточно данных для анализа.'
                    is_error = True
                else:
                    msg = f'Ты ввёл тикер {stock} в размере {size} Long?'
            elif size_value < 0:
                ticker_bars_amount = eod.get_bars_amount(stock, start_date, now)
                if ticker_bars_amount < spy_bars_amount:
                    debug(f'spy_bars_amount={spy_bars_amount}  ticker_bars_amount={ticker_bars_amount}')
                    msg = f'По этому тикеру не достаточно данных для анализа.'
                    is_error = True
                else:
                    msg = f'Ты ввёл тикер {stock} в размере {size} Short?'
            else:
                msg = f'{stock} {size} позиция не будет сохранена, нажмите кнопку исправить'
                is_error = True
    else:
        msg = 'Ошибочный ввод: не соответствует формату. Нажмите кнопку исправить'
        is_error = True

    if not is_error:
        shared.set_inspector_ticker(sender_id, stock, size)
    debug(f'portfolio_ticker={stock}:{size}')
    old_msg_id = await shared.get_old_msg_id(sender_id)
    ibuttons = buttons.inspector_next if not is_error else buttons.inspector_error
    if old_msg_id is not None:
        try:
            await client_.edit_message(event.input_sender, old_msg_id, msg, buttons=ibuttons)
        except terr.MessageNotModifiedError:
            pass
    else:
        msg = await client_.send_message(event.input_sender, msg, buttons=ibuttons)
        await shared.save_old_message(sender_id, msg)
    #
    # path = f'{PROJECT_HOME_DIR}/results/ticker_stat/'
    # img_path = f'{path}{stock}.png'

