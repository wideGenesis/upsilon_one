#!/usr/bin/env python3

import os
import sys
import yaml
import logging
import socket
import selectors
import traceback
import rsa
import asyncio
import importlib
from fastnumbers import *

from sqlalchemy import create_engine
from alchemysession import AlchemySessionContainer
from telethon import events, TelegramClient, types, functions
from aiohttp import web
from telegram import menu
from telegram import sql_queries as sql
from telegram import handlers
from telegram import callbacks
from telegram import shared
from telegram import instructions as ins
from telegram import buttons
from project_shared import *
from tcp_client_server.libserver import *
import concurrent.futures
from messages.message import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from pprint import pprint

# ============================== Environment Setup ======================
from telegram.db_init import db_init_new_tables
from telegram.sql_queries import save_action_data

PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PYTHON_PATH)
ABS_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/Common Bot 1-43c490d227df.json"
os.environ["PYTHONUNBUFFERED"] = "1"

PUBKEY = None

# ============================== Init ===================================
client = TelegramClient(alchemy_session, API_KEY, API_HASH).start(bot_token=UPSILON)

app = web.Application()


# ============================== Main Menu ===============================
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await menu.start_menu(event, client, engine=engine)


@client.on(events.NewMessage(pattern='Главное меню|\U0001F4C1 Главное меню|📁 Главное меню'))
async def tools(event):
    await acion_info(event, 'main menu', f'Главное меню')
    await menu.tools_menu(event, client)


@client.on(events.NewMessage(pattern='menu|Menu|Меню|меню'))
async def meta_tools(event):
    await acion_info(event, 'cmd', f'Меню')
    await menu.meta_menu(event, client)


@client.on(events.NewMessage(pattern='Профиль|профиль|Profile|profile|👤 Профиль|\U0001F464 Профиль'))
async def profile(event):
    await acion_info(event, 'main menu', f'Профиль')
    await menu.profile_menu(event, client, engine=engine)


@client.on(events.NewMessage(pattern='Помощь|инструкции|Инструкции|помощь|help|Help|/help'))
async def helper(event):
    await acion_info(event, 'main menu', f'Помощь')
    await menu.information_menu(event, client, engine=engine)


@client.on(events.NewMessage(pattern='Информация|инфомация|инфо|Инфо|🛎 Информация|\U0001F6CE Информация'))
async def information(event):
    await acion_info(event, 'main menu', f'Информация')
    await menu.information_menu(event, client, engine=engine)


# ============================== Commands ===============================
@client.on(events.NewMessage(pattern='портфель|портфели|Портфель|Портфели|portfolio|portfolios'))
async def portfolios(event):
    await acion_info(event, 'cmd', f'Портфель')
    await handlers.portfolios_cmd(client, event)


@client.on(events.NewMessage(pattern='/to'))  # TODO Сделать блокирующую функцию для ДФ
async def send_to(event):
    await handlers.send_to_handler(event, client, owner=OWNER)


@client.on(events.NewMessage(pattern='/publish_to'))
async def publish_to(event):
    await handlers.publish_to_handler(event, client, owner=OWNER)


@client.on(events.NewMessage())
async def dialog_flow(event):
    await handlers.dialog_flow_handler(event, client)


@client.on(events.NewMessage(pattern='[$#@]'))
async def quotes_to(event):
    await acion_info(event, 'ticker data', f'Try get ticker data')
    debug(f'--== {str(event.text)} ==--')
    await handlers.quotes_to_handler(event, client, limit=0)


@client.on(events.NewMessage(pattern='news'))
async def news_to(event):
    await acion_info(event, 'cmd',  f'news')
    await handlers.news_to_handler(event, client, limit=0)


@client.on(events.NewMessage(pattern='!'))
async def inspector_to(event):
    await acion_info(event, 'cmd', f'Enter ticker for inspector')
    await handlers.inspector_to_handler(event, client)


# ============================== Callbacks =======================
@client.on(events.CallbackQuery)
async def callback(event):
    button = event.data
    action = f'Press button {button.decode("utf-8")}'
    await acion_info(event, 'press button', action)
    await callbacks.callback_handler(event, client, img_path=IMAGES_OUT_PATH, yahoo_path=YAHOO_PATH,
                                     engine=engine)


@client.on(events.Raw)
async def handler(update):
    await callbacks.polls_handler(update, client)


# ============================== Instructions ===============================
@client.on(events.NewMessage(pattern='/goals'))
async def goals(event):
    await acion_info(event, 'cmd', f'goals')
    await handlers.goals_handler(event, client)


@client.on(events.NewMessage(pattern='/skills'))
async def skills(event):
    await acion_info(event, 'cmd', f'skills')
    await handlers.skills_handler(event, client)


@client.on(events.NewMessage(pattern='^/(instruction[0-9][0-9]|mindepo)$'))
async def instructions(event):
    await acion_info(event, 'cmd', f'instruction')
    await handlers.instructions_handler(event, client)


# @client.on(events.NewMessage(pattern='^/chart_(parking|allweather|balanced|aggressive|leveraged|elastic|yolo)$'))
# async def instructions(event):
#     await handlers.portfolio_candle_chart_handler(event, client)


@client.on(events.NewMessage(pattern='Анкета регистрации управляющего'))
async def instructions(event):
    await acion_info(event, 'cmd', f'Анкета регистрации управляющего')
    await handlers.managers_form_handler(event, client)


@client.on(events.NewMessage(pattern='/(support|adv|bug)'))
async def support(event):
    await acion_info(event, 'cmd', f'support|adv|bug')
    await handlers.support_handler(event, client)


async def acion_info(event, action_type, action):
    msg = getattr(event, "message", None)
    sender = getattr(event.message, "sender", None) if msg else None
    if msg is None and sender is None:
        sender = getattr(event, "sender", None)
    if sender is not None:
        usr_data = ''
        if sender.username:
            debug(f' -- {action} -- {sender.id} - {sender.username}')
        else:
            if sender.first_name is not None:
                usr_data += f'{sender.first_name} '
            if sender.last_name is not None:
                usr_data += f'{sender.last_name}'
            debug(f' -- {action} -- {sender.id} - ( {usr_data} )')
        await sql.save_action_data(sender.id, action_type, action)


# That event is handled when customer enters his card/etc, on final pre-checkout
# If we don't `SetBotPrecheckoutResultsRequest`, money won't be charged from buyer, and nothing will happen next.
@client.on(events.Raw(types.UpdateBotPrecheckoutQuery))
async def payment_pre_checkout_handler(event: types.UpdateBotPrecheckoutQuery):
    payload_json = event.payload.decode('UTF-8')
    payload = json.loads(payload_json)
    if payload['o_t'] == 'replenishment' or payload['o_t'] == 'donate':
        await client(
            functions.messages.SetBotPrecheckoutResultsRequest(
                query_id=event.query_id,
                success=True,
                error=None
            )
        )
    else:
        # for example, something went wrong (whatever reason). We can tell customer about that:
        await client(
            functions.messages.SetBotPrecheckoutResultsRequest(
                query_id=event.query_id,
                success=False,
                error='Something went wrong'
            )
        )

    raise events.StopPropagation


# That event is handled at the end, when customer payed.
@client.on(events.Raw(types.UpdateNewMessage))
async def payment_received_handler(event):
    if isinstance(event.message.action, types.MessageActionPaymentSentMe):
        payment: types.MessageActionPaymentSentMe = event.message.action
        # do something after payment was recieved
        payload_json = payment.payload.decode('UTF-8')
        payload = json.loads(payload_json)
        if payload['o_t'] == 'replenishment':
            # Подгрузим динамически модуль - вдруг ценообразование изменилось?!
            pricing = None
            if "telegram.pricing" in sys.modules:
                debug(f'module imported --- try reload')
                pricing = importlib.reload(sys.modules["telegram.pricing"])
            else:
                debug(f'module NOT imported --- try first import')
                pricing = importlib.import_module("telegram.pricing")

            # расчитываем и сохраняем количество доступных запросов
            summ = fast_float(payload["s"], 0)
            await pricing.calc_save_balance(payload["s_i"], summ)
            await sql.save_payment_data(payload["s_i"], payload["o_i"], summ)

            await client.send_message(payload['s_i'],
                                      f'Оплата прошла успешно:\n'
                                      f'**Покупка {payload["r_a"]} запросов**\n'
                                      f'__Ордер: {payload["o_i"]} __\n'
                                      f'__Сумма: {payload["s"]}$ __\n'
                                      f'**Спасибо, что пользуешься моими услугами!**')
            debug("!!!!!!!!!!!!!! Tis is replenishment !!!!!!!!!!!!!!!!!!!")
        elif payload['o_t'] == 'donate':
            await client.send_message(payload['s_i'],
                                      f'Оплата прошла успешно:\n'
                                      f'**Пожертвование**\n'
                                      f'__Ордер: {payload["o_i"]} __\n'
                                      f'__Сумма: {payload["s"]}$ __\n'
                                      f'**Спасибо, что пользуешься моими услугами!**')
            debug("!!!!!!!!!!!!!! Tis is donate !!!!!!!!!!!!!!!!!!!")
        raise events.StopPropagation


# ============================== Main  =============================
# Стартуем вебсервер для прослушки приходящих событий об успешных платежах
async def webserver_starter():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, PAYMENT_SUCCESS_LISTEN, PAYMENT_SUCCESS_LISTEN_PORT)
    await site.start()


async def init_db():
    # Создаем таблицу с данными по платежным сообщениям
    # Таблица будет создаваться только если ее нет
    await sql.create_payment_message_table(engine)

    # Забираем данные из таблицы по платежным сообщениям
    # Если бот перезапускался, то будем знать какие сообщения
    # нужно удалить из истории
    rows = await sql.get_all_payment_message(engine)
    # print("rows=" + str(rows))
    for row in rows:
        shared.set_order_data(row[0], row[1], row[2], row[3])

    # должно стать обычной практикой - при релизе руками создавать все новые таблицы
    # что бы избежать ошибок отсутствия нужных таблиц
    # проинициализировать таблицы, если это нужно
    await db_init_new_tables()


async def run_worker(thread, worker):
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    # worker.finished.connect(thread.quit)
    # worker.finished.connect(worker.deleteLater)
    # thread.finished.connect(thread.deleteLater)
    worker.minute_signal.connect(shared.inspector_scheduler)
    thread.start()


def main():
    # Подгружаем публичный ключ для проверки подписи данных об успешных платежах
    with open('config/key.pub', mode='rb') as public_file:
        key_data = public_file.read()
        global PUBKEY
        PUBKEY = rsa.PublicKey.load_pkcs1_openssl_pem(key_data)

    handlers.set_route(app, PAYMENT_TOKEN, COMMAND_TOKEN, PUBKEY, client, engine)

    # shared.create_subscribes(TARIFF_IMAGES)

    # Стартуем веб сервер с отдельным event loop
    debug("_____Running db init_____")
    loop_db = asyncio.get_event_loop()
    loop_db.run_until_complete(init_db())

    thread = QThread()
    worker = shared.Worker()
    worker.set_client(client)
    debug("_____Running worker_____")
    loop_worker = asyncio.get_event_loop()
    loop_worker.run_until_complete(run_worker(thread, worker))

    debug("_____Running web server_____")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(webserver_starter())

    debug("__Running telethon client__")
    # Старт клиента Телетон
    client.run_until_disconnected()


if __name__ == '__main__':
    if not IS_RUN_LOCAL:
        debug_init(file_name="bot.log")
    debug("__Ignition sequence start__")
    # print(sys.path)
    main()
    debug_deinit()
