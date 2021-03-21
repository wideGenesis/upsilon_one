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
from sqlalchemy import create_engine
from alchemysession import AlchemySessionContainer
from telethon import events, TelegramClient
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


# ============================== Environment Setup ======================
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
    await menu.tools_menu(event, client)


@client.on(events.NewMessage(pattern='menu|Menu|Меню|меню'))
async def meta_tools(event):
    await menu.meta_menu(event, client)


@client.on(events.NewMessage(pattern='Профиль|профиль|Profile|profile|👤 Профиль|\U0001F464 Профиль'))
async def profile(event):
    await menu.profile_menu(event, client, engine=engine)


@client.on(events.NewMessage(pattern='Помощь|инструкции|Инструкции|помощь|help|Help|/help'))
async def helper(event):
    await menu.information_menu(event, client, engine=engine)


@client.on(events.NewMessage(pattern='Информация|инфомация|инфо|Инфо|🛎 Информация|\U0001F6CE Информация'))
async def information(event):
    await menu.information_menu(event, client, engine=engine)


# ============================== Commands ===============================
@client.on(events.NewMessage(pattern='портфель|портфели|Портфель|Портфели|portfolio|portfolios'))
async def portfolios(event):
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


@client.on(events.NewMessage(pattern='/q|[$#@]'))
async def quotes_to(event):
    await handlers.quotes_to_handler(event, client, limit=0)


@client.on(events.NewMessage(pattern='news'))
async def news_to(event):
    await handlers.news_to_handler(event, client, limit=0)


@client.on(events.NewMessage(pattern='/donate'))
async def news_to(event):
    await handlers.donate_handler(event, client)


# ============================== Callbacks =======================
@client.on(events.CallbackQuery)
async def callback(event):
    await callbacks.callback_handler(event, client, img_path=IMAGES_OUT_PATH, yahoo_path=YAHOO_PATH,
                                     engine=engine)


@client.on(events.Raw)
async def handler(update):
    try:
        await callbacks.polls_handler(update, client)
    except:
        return


# ============================== Instructions ===============================
@client.on(events.NewMessage(pattern='/goals'))
async def goals(event):
    await handlers.goals_handler(event, client)


@client.on(events.NewMessage(pattern='/skills'))
async def skills(event):
    await handlers.skills_handler(event, client)


@client.on(events.NewMessage(pattern='^/(instruction[0-9][0-9]|mindepo)$'))
async def instructions(event):
    await handlers.instructions_handler(event, client)


# @client.on(events.NewMessage(pattern='^/chart_(parking|allweather|balanced|aggressive|leveraged|elastic|yolo)$'))
# async def instructions(event):
#     await handlers.portfolio_candle_chart_handler(event, client)


@client.on(events.NewMessage(pattern='Анкета регистрации управляющего'))
async def instructions(event):
    await handlers.managers_form_handler(event, client)


@client.on(events.NewMessage(pattern='/(support|adv|bug)'))
async def support(event):
    await handlers.support_handler(event, client)


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
        shared.ORDER_MAP[row[0]] = (row[1], row[2], row[3])


def main():
    # Подгружаем публичный ключ для проверки подписи данных об успешных платежах
    with open('config/key.pub', mode='rb') as public_file:
        key_data = public_file.read()
        global PUBKEY
        PUBKEY = rsa.PublicKey.load_pkcs1_openssl_pem(key_data)

    handlers.set_route(app, PAYMENT_TOKEN, COMMAND_TOKEN, PUBKEY, client, engine)

    shared.create_subscribes(TARIFF_IMAGES)

    # Стартуем веб сервер с отдельным event loop
    debug("_____Running db init_____")
    loop_db = asyncio.get_event_loop()
    loop_db.run_until_complete(init_db())

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
