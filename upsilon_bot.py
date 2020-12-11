#!/usr/bin/env python3

import os
import sys
import yaml
import logging
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

# ============================== Environment Setup ======================
PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PYTHON_PATH)
ABS_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

conf = yaml.safe_load(open('config/settings.yaml'))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/Common Bot 1-43c490d227df.json"
os.environ["PYTHONUNBUFFERED"] = "1"

# ============================== Logging Setup ======================
logging.basicConfig(
    filemode='w',
    filename=os.path.abspath('logs/bot.log'),
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)
logging.getLogger('telethon').setLevel(level=logging.WARNING)

# ============================== Credentials and GLOBALS ======================

PAYMENT_TOKEN = conf['TELEGRAM']['PAYMENT_TOKEN']
PAYMENT_SUCCESS_LISTEN = conf['TELEGRAM']['PAYMENT_SUCCESS_LISTEN']
PAYMENT_SUCCESS_LISTEN_PORT = conf['TELEGRAM']['PAYMENT_SUCCESS_LISTEN_PORT']
PUBKEY = None

YAHOO_PATH = conf['PATHS']['YAHOO_PATH']
IMAGES_OUT_PATH = conf['PATHS']['IMAGES_OUT_PATH']
TARIFF_IMAGES = conf['TELEGRAM']['TARIFF_IMAGES']
BTC = conf['CREDENTIALS']['BTC']
ETH = conf['CREDENTIALS']['ETH']
API_KEY = conf['TELEGRAM']['API_KEY']
API_HASH = conf['TELEGRAM']['API_HASH']
UPSILON = conf['TELEGRAM']['UPSILON']
OWNER = conf['TELEGRAM']['OWNER']  # TODO Сделать пару владельцев для коммуникации
SERVICE_CHAT = conf['TELEGRAM']['SERVICE_CHAT']

# ============================== SQL Connect ======================

SQL_DB_NAME = conf['SQL']['DB_NAME']
SQL_USER = conf['SQL']['DB_USER']
SQL_PASSWORD = conf['SQL']['DB_PASSWORD']
SQL_URI = 'mysql+pymysql://{}:{}@localhost/{}'.format(SQL_USER, SQL_PASSWORD, SQL_DB_NAME)

engine = create_engine(SQL_URI, pool_recycle=3600)
container = AlchemySessionContainer(engine=engine)
alchemy_session = container.new_session('default')

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

    handlers.set_route(app, PAYMENT_TOKEN, PUBKEY, client, engine)

    shared.create_subscribes(TARIFF_IMAGES)

    # Стартуем веб сервер с отдельным event loop
    print("_____Running db init_____", '\n')
    loop_db = asyncio.get_event_loop()
    loop_db.run_until_complete(init_db())
    print("_____Running web server_____", '\n')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(webserver_starter())
    print("__Running telethon client__", '\n')

    # Старт клиента Телетон
    client.run_until_disconnected()


if __name__ == '__main__':
    print("__Ignition sequence start__", '\n')
    # print(sys.path)
    main()
