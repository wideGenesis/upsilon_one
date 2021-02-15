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
from project_shared import *
from tcp_client_server.libserver import *

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


@client.on(events.NewMessage(pattern='Главное меню'))
async def tools(event):
    await menu.tools_menu(event, client)


@client.on(events.NewMessage(pattern='Профиль'))
async def profile(event):
    await menu.profile_menu(event, client, engine=engine)


@client.on(events.NewMessage(pattern='Помощь'))
async def helper(event):
    await menu.helper_menu(event, client)


@client.on(events.NewMessage(pattern='Donate'))
async def donate(event):
    await menu.donate_menu(event, client)


# ============================== Commands ===============================
@client.on(events.NewMessage(pattern='/to'))  # TODO Сделать блокирующую функцию для ДФ
async def send_to(event):
    await handlers.send_to_handler(event, client, owner=OWNER)


@client.on(events.NewMessage(pattern='/publish_to'))
async def publish_to(event):
    await handlers.publish_to_handler(event, client, owner=OWNER)


@client.on(events.NewMessage())
async def dialog_flow(event):
    await handlers.dialog_flow_handler(event, client)


@client.on(events.NewMessage(pattern='/q'))
async def quotes_to(event):
    await handlers.quotes_to_handler(event, client, limit=0)


@client.on(events.NewMessage(pattern='/n'))
async def news_to(event):
    await handlers.news_to_handler(event, client, limit=0)


# ============================== Callbacks =======================
@client.on(events.CallbackQuery)
async def callback(event):
    await callbacks.callback_handler(event, client, img_path=IMAGES_OUT_PATH, yahoo_path=YAHOO_PATH,
                                     engine=engine)


# ============================== Instructions ===============================
@client.on(events.NewMessage(pattern='/about'))
async def about(event):
    await handlers.about_handler(event, client)


@client.on(events.NewMessage(pattern='/goals'))
async def goals(event):
    await handlers.goals_handler(event, client)


@client.on(events.NewMessage(pattern='/skills'))
async def skills(event):
    await handlers.skills_handler(event, client)


@client.on(events.NewMessage(pattern='/future'))
async def future(event):
    await handlers.future_handler(event, client)


@client.on(events.NewMessage(pattern='^/(instruction[0-9][0-9]|mindepo)$'))
async def instructions(event):
    await handlers.instructions_handler(event, client)


@client.on(events.NewMessage(pattern='^/chart_(parking|allweather|balanced|aggressive|leveraged|elastic|yolo)$'))
async def instructions(event):
    await handlers.portfolio_candle_chart_handler(event, client)


@client.on(events.NewMessage(pattern='Анкета регистрации управляющего'))
async def instructions(event):
    await handlers.managers_form_handler(event, client)


# ============================== Main  =============================
# Стартуем вебсервер для прослушки приходящих событий об успешных платежах
async def webserver_starter():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, PAYMENT_SUCCESS_LISTEN, PAYMENT_SUCCESS_LISTEN_PORT)
    await site.start()


async def accept_wrapper(sock, sel):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


async def tcpserver_starter(clnt):
    sel = selectors.DefaultSelector()
    host = ''
    port = 50638
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((host, port))
    lsock.listen()
    debug(f'TCP Server listening on ({host}, {port})')
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            tcp_events = sel.select(timeout=None)
            for key, mask in tcp_events:
                if key.data is None:
                    await accept_wrapper(key.fileobj, sel)
                else:
                    message = key.data
                    try:
                        action, value = message.process_events(mask)
                        is_ack = False
                        if action == 'send_to':
                            debug('Need to send something!!')
                            if value == 'sac_pies':
                                await handlers.send_sac_pie(clnt)
                            is_ack = True
                        elif action == 'create':
                            debug('Need create anything')
                            is_ack = True
                        message.process_answer(mask, is_ack)

                    except Exception:
                        debug(f'main: error: exception for {message.addr}:\n{traceback.format_exc()}')
                        message.close()
    except KeyboardInterrupt:
        debug("caught keyboard interrupt, exiting")
    finally:
        sel.close()


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

    handlers.set_route(app, PAYMENT_TOKEN, PUBKEY, client, engine)

    shared.create_subscribes(TARIFF_IMAGES)

    # Стартуем веб сервер с отдельным event loop
    debug("_____Running db init_____")
    loop_db = asyncio.get_event_loop()
    loop_db.run_until_complete(init_db())

    debug("_____Running web server_____")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(webserver_starter())

    debug("_____Running TCP server_____")
    loop_tcp = asyncio.get_event_loop()
    loop_tcp.run_until_complete(tcpserver_starter(client))

    debug("__Running telethon client__")
    # Старт клиента Телетон
    client.run_until_disconnected()


if __name__ == '__main__':
    # debug_init(file_name="bot.log")
    debug("__Ignition sequence start__")
    # print(sys.path)
    main()
    debug_deinit()

