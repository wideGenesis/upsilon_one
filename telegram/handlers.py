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
    print(parse)
    stock = parse[1]
    stock = stock.upper()
    img_path = os.path.join('results/ticker_stat', f'{stock}.png')
    ss = StockStat(stock=stock)
    try:
        ss.stock_download()
    except Exception as e0:
        debug(e0)
    try:
        msg1 = ss.stock_description()
    except Exception as e1:
        debug(e1)
        msg1 = 'Описание для ETF недоступно'
    try:
        ss.stock_snapshot()
    except Exception as e2:
        debug(e2)
    try:
        msg2 = ss.stock_stat()
    except Exception as e3:
        debug(e3)
        msg2 = 'Статистика недоступна'
    try:
        msg3 = ss.company_rank()
    except Exception as e4:
        debug(e4)
        msg3 = 'Рекомендация недоступна'

    await client_.send_message(event.input_sender, msg2)
    await client_.send_file(event.input_sender, img_path)
    await client_.send_message(event.input_sender, msg1)
    await client_.send_message(event.input_sender, 'Оценка Ипсилона: ' + '\n' + msg3)
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


async def portfolio_candle_chart_handler(event, client_):
    pattern = event.original_update.message.message
    pattern = str(pattern).strip('/').split('_')[1]
    if pattern == 'parking':
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'parking_port_chart_over_TLT.png')
    elif pattern == 'allweather':
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'allweather_port_chart_over_SPY.png')
    elif pattern == 'balanced':
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'balanced_port_chart_over_QQQ.png')
    elif pattern == 'aggressive':
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'aggressive_port_chart_over_QQQ.png')
    elif pattern == 'leveraged':
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'leveraged_port_chart_over_QQQ.png')
    elif pattern == 'elastic':
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'elastic_port_chart_over_QQQ.png')
    elif pattern == 'yolo':
        await client_.send_file(event.input_sender, CHARTER_IMAGES_PATH + 'yolo_port_chart_over_SPY.png')


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
    try:
        users = await get_all_users(engine)
        for user_id in users:
            await clnt.send_message(user_id, msg)
        return True
    except Exception as e:
        debug(e, ERROR)
        return False
