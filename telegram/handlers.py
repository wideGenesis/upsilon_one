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
from project_shared import *


class WebHandler:

    def __init__(self, payment_token, pubkey, client, engine):
        self.payment_token = payment_token
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
        else:
            return web.Response(status=403)


def set_route(app, payment_token, pubkey, client, engine):
    web_handler = WebHandler(payment_token, pubkey, client, engine)
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
    no_match = ['\U0001F9D0', '\U0001F633', 'Ясно', 'Мы должны подумать над этим']
    fallback = random.choice(no_match)
    try:
        sender_id = event.input_sender
    except ValueError as e:
        sender_id = await event.get_input_sender()
    if not any(value in event.text for value in
               ('/start', '/help', '/publish_to', '/to', 'Главное меню', 'Профиль', 'Помощь', 'Donate', '/q', '/n',
                '/about', '/goals', '/skills', '/future',
                '/instruction00',
                '/instruction01',
                '/instruction02',
                '/instruction03',
                '/instruction04',
                '/instruction05',
                '/instruction06',
                '/instruction07',
                '/instruction08',
                '/instruction09',
                '/instruction10',
                )):
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
    parse = str(event.text).split(' ')
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

    await client_.send_message(event.input_sender, msg2)
    await client_.send_file(event.input_sender, img_path)
    await client_.send_message(event.input_sender, msg1)
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
