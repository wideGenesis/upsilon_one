#!/usr/bin/env python3

import os
import sys
import yaml
import csv
import logging
import rsa
import asyncio

from sqlalchemy import create_engine
from alchemysession import AlchemySessionContainer

from telethon import events, TelegramClient
from telethon.tl.custom import Button
from telethon.tl.types import PeerUser

from aiohttp import web

from telegram import buttons
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
    # filename=os.path.abspath('logs/error.log'),
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)
logging.getLogger('telethon').setLevel(level=logging.INFO)

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


# ============================== Callbacks =======================
@client.on(events.CallbackQuery)
async def callback(event):
    await callbacks.callback_handler(event, client, img_path=IMAGES_OUT_PATH, yahoo_path=YAHOO_PATH,
                                     tariff_img_path=TARIFF_IMAGES, engine=engine)


# @client.on(events.CallbackQuery)
# async def callback(event):
# sender_id = event.original_update.user_id
# entity = await client.get_input_entity(sender_id)
#
# # ============================== Главное меню 1 уровень=============================
# if event.data == b'a1':
#     await client.send_message(event.input_sender, 'Анализ рынков', buttons=buttons.keyboard_a1)
#     await event.edit()
# elif event.data == b'a2':
#     await client.send_message(event.input_sender, 'Конструктор портфелей', buttons=buttons.keyboard_a2)
#     await event.edit()
# elif event.data == b'a3':
#     await client.send_message(event.input_sender, 'Калькуляторы', buttons=buttons.keyboard_a3)
#     await event.edit()
# elif event.data == b'a4':
#     await client.send_message(event.input_sender, 'Управление', buttons=buttons.keyboard_a4)
#     await event.edit()
# elif event.data == b'a5':
#     await client.send_message(event.input_sender, 'Инструкции', buttons=buttons.keyboard_a5)
#     await event.edit()
# elif event.data == b'a6':
#     await client.send_message(event.input_sender, 'Образование', buttons=buttons.keyboard_a6)
#     await event.edit()
# elif event.data == b'a7':
#     await client.send_message(event.input_sender, 'Налоги', buttons=buttons.keyboard_a7)
#     await event.edit()
# elif event.data == b'a8':
#     await client.send_message(event.input_sender, 'Агрегатор новостей', buttons=buttons.keyboard_a8)
#     await event.edit()
# elif event.data == b'main':
#     await client.send_message(event.input_sender, 'Главное меню', buttons=buttons.keyboard_0)
#     await event.edit()
#
# # ============================== Анализ рынков 2 уровень=============================
# elif event.data == b'a1a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(event.input_sender, 'Количество растущих/падающих акций и объёмы за сегодня')
#     filename = os.path.join(IMAGES_OUT_PATH, 'adv.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             await client.send_message(entity=entity, message=f'{row}')
#     await client.send_message(event.input_sender, 'Общая картина')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'sectors.png')
#     await client.send_message(event.input_sender, 'Волатильность и барометр жадности/страха')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'volatility.png')
#     await client.send_message(event.input_sender, 'Тепловая карта 1-day performance')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'treemap.png')
#     await client.edit_message(message, 'Анализ рынка США')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как интерпритировать графики выше? /instruction01',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(event.input_sender, 'Общая картина')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'crypto.png')
#     await client.send_message(event.input_sender, 'Тепловая карта 1-day performance')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'coins_treemap.png')
#     await client.edit_message(message, 'Рынок криптовалют')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как интерпритировать графики выше? /instruction01',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a3':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(event.input_sender, 'Общая картина')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'rtsi.png')
#     await client.edit_message(message, 'Рынок РФ')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как интерпритировать графики выше? /instruction01',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a4':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(entity=entity, message='Денежные потоки в миллионах USD')
#     await client.send_message(entity=entity, message='Денежные потоки SPY')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_SPY.png')
#     await client.send_message(entity=entity, message='Денежные потоки QQQ')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_QQQ.png')
#     await client.send_message(entity=entity, message='Денежные потоки VTI')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VTI.png')
#     await client.send_message(entity=entity, message='Денежные потоки VEA')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VEA.png')
#     await client.send_message(entity=entity, message='Денежные потоки VWO')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VWO.png')
#     await client.send_message(entity=entity, message='Денежные потоки LQD')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_LQD.png')
#     await client.send_message(entity=entity, message='Денежные потоки VXX')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VXX.png')
#     await client.send_message(entity=entity, message='Денежные потоки SHY')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_SHY.png')
#     await client.send_message(entity=entity, message='Денежные потоки TLT')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_TLT.png')
#     await client.edit_message(message, 'Ежедневные денежные потоки основных ETF за месяц')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как интерпритировать денежные потоки? /instruction02',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a5':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(event.input_sender, 'Общая картина 1-day performance')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'global_treemap.png')
#     await client.send_message(event.input_sender, 'Общая картина YTD performance')
#     await client.send_message(event.input_sender, 'Общая картина bubble map')
#     await client.edit_message(message, 'Мировые рынки в картах')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как ? /instruction02',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a6':
#     await client.send_message(event.input_sender, 'Основные макро индикаторы', buttons=buttons.keyboard_core_macro)
#     await event.edit()
# elif event.data == b'a1a-1':
#     await client.send_message(event.input_sender, 'Анализ рынков', buttons=buttons.keyboard_a1)
#     await event.edit()
#
# # ============================== Конструктор стратегий =============================
# elif event.data == b'a2a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Твой профиль риска')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Зачем нужно знать свой профиль риска? /instruction03',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Оценка/аудит портфеля')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Зачем проводить аудит своего портфеля? /instruction04',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a3':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, '"Парковочный" портфель без риска')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать парковочный портфель? /instruction05',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a4':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Всепогодный портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать всепогодный портфель? /instruction06',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a5':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Сбалансированный портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать сбалансированный портфель? /instruction07',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a6':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Агрессивный портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать агрессивный портфель? /instruction08',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a7':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Крипто портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать крипто портфель? /instruction09',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a8':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Трейдинг/Дневные стратегии')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Подходит ли вам трейдинг? /instruction10',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a-1':
#     await client.send_message(event.input_sender, 'Конструктор стратегий', buttons=buttons.keyboard_a2)
#     await event.edit()
#
# # ============================== Калькуляторы =============================
# elif event.data == b'a3a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Рассчет количества акций для портфеля')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Конвертация весов в количество? /instruction11',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Симуляция 10 летней доходности')
#     await event.edit()
#     await client.send_message(event.input_sender,
#                               'Что ожидать от текущего портфеля в ближайшую декаду? /instruction12',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a3':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Рассчет оптимального размера взносов')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Почему взносы необходимы? /instruction13',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a4':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Рассчет безопасного размера вывода средств')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Сколько можно выводить средств? /instruction14',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a5':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Сложный процент')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Сложный процент в действии. /instruction15',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a-1':
#     await client.send_message(event.input_sender, 'Калькуляторы', buttons=buttons.keyboard_a3)
#     await event.edit()
#
# # ============================== Управление =============================
# elif event.data == b'a4a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Маркетплейс управляющих')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Все об управлени активами. /instruction16',
#                               buttons=buttons.keyboard_a4_back)
# elif event.data == b'a4a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Стать управляющим')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Стать управляющим',
#                               buttons=buttons.keyboard_a4_back)
# elif event.data == b'a4a-1':
#     await client.send_message(event.input_sender, 'Управление', buttons=buttons.keyboard_a4)
#     await event.edit()
#
# # ============================== Инструкции =============================
# elif event.data == b'a5a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Как ... /instruction01')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как ... /instruction01',
#                               buttons=buttons.keyboard_a5_back)
# elif event.data == b'a5a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Что ... /instruction02')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Что ... /instruction02',
#                               buttons=buttons.keyboard_a5_back)
# elif event.data == b'a5a-1':
#     await client.send_message(event.input_sender, 'Инструкции', buttons=buttons.keyboard_a5)
#     await event.edit()
#
# # ============================== Образовательные программы =============================
# elif event.data == b'a6a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Основы инвестирования')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Основы инвестирования /instruction20',
#                               buttons=buttons.keyboard_a6_back)
# elif event.data == b'a6a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Как собрать свой первый портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как собрать свой первый портфель /instruction21',
#                               buttons=buttons.keyboard_a6_back)
# elif event.data == b'a6a3':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Профессиональные решения')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Профессиональные решения /instruction22',
#                               buttons=buttons.keyboard_a6_back)
# elif event.data == b'a6a-1':
#     await client.send_message(event.input_sender, 'Образование', buttons=buttons.keyboard_a6)
#     await event.edit()
#
# # ============================== Налоги =============================
# elif event.data == b'a7a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Оптимизация налогов')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Оптимизация налогов /instruction30',
#                               buttons=buttons.keyboard_a7_back)
# elif event.data == b'a7a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Подготовка налоговых деклараций')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Подготовка налоговых деклараций /instruction30',
#                               buttons=buttons.keyboard_a7_back)
# elif event.data == b'a7a-1':
#     await client.send_message(event.input_sender, 'Налоги', buttons=buttons.keyboard_a7)
#     await event.edit()
#
# # ============================== Агрегатор новостей =============================
# elif event.data == b'a8a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Поставщики новостей')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Поставщики новостей',
#                               buttons=buttons.keyboard_a8_back)
# elif event.data == b'a8a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Тикеры')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Тикеры',
#                               buttons=buttons.keyboard_a8_back)
# elif event.data == b'a8a-1':
#     await client.send_message(event.input_sender, 'Агрегатор новостей', buttons=buttons.keyboard_a8)
#     await event.edit()
#
# # elif event.data == b'a4a1':
# #     message = await client.send_message(entity=entity, message='Loading...')
# #     await client.send_file(entity, IMAGES_OUT_PATH + 'us_index.png')
# #     await client.edit_message(message, 'Ипсилон AI US Index')
# #     await event.edit()
# # elif event.data == b'a4a2':
# #     message = await client.send_message(entity=entity, message='Loading...')
# #     await client.send_file(entity, IMAGES_OUT_PATH + 'world_index.png')
# #     await client.edit_message(message, 'Ипсилон AI WORLD Index')
# #     await event.edit()
#
# # ============================== Основные макро данные =============================
# elif event.data == b'cm1':
#     await client.send_message(entity=entity, message='Interest Rates')
#     await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
#     filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             if row[0] == 'Interest Rate':
#                 new_row = ',  '.join(row)
#                 await client.send_message(entity=entity, message=f'{new_row}')
#     await event.edit()
#     await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
# elif event.data == b'cm2':
#     await client.send_message(entity=entity, message='Interest Rates')
#     await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
#     filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             if row[0] == 'Inflation Rate':
#                 new_row = ',  '.join(row)
#                 await client.send_message(entity=entity, message=f'{new_row}')
#     await event.edit()
#     await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
# elif event.data == b'cm3':
#     await client.send_message(entity=entity, message='Interest Rates')
#     await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
#     filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             if row[0] == 'Unemployment Rate':
#                 new_row = ',  '.join(row)
#                 await client.send_message(entity=entity, message=f'{new_row}')
#     await event.edit()
#     await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
# elif event.data == b'cm4':
#     await client.send_message(entity=entity, message='Interest Rates')
#     await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
#     filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             if row[0] == 'Composite PMI':
#                 new_row = ',  '.join(row)
#                 await client.send_message(entity=entity, message=f'{new_row}')
#     await event.edit()
#     await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
# elif event.data == b'cm-1':
#     await client.send_message(event.input_sender, 'Назад', buttons=buttons.keyboard_core_macro_back)
#     await event.edit()
# elif event.data == b'cm-2':
#     await client.send_message(event.input_sender, 'Назад', buttons=buttons.keyboard_a1)
#     await event.edit()
# elif event.data == b'z2':
#     await client.send_message(event.input_sender,
#                               'Вы можете попросить друга запустить бота и получить бесплатную'
#                               ' подписку. '
#                               'Проще всего это сделать через групповые чаты' + '\n' +
#                               f'[https://t.me/UpsilonBot?start={sender_id}]'
#                               f'(https://t.me/UpsilonBot?start={sender_id})')
#     # TODO Изменить на оригинал
#     await event.edit()


# ============================== Subscriptions =============================
# elif event.data == b'z1':
#     await client.send_message(event.input_sender, 'Уровень подписок', buttons=buttons.keyboard_core_subscriptions)
#     await event.edit()
# elif event.data == b'kcs0':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + 'tariff_compare.jpg')
#     await event.edit()
# elif event.data == b'kcs1':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + 'tariff_start.jpg')
#     await client.send_message(event.input_sender, 'Тут описание тарифа Старт',
#                               buttons=buttons.keyboard_subscription_start)
#     await event.edit()
# elif event.data == b'kcs2':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + '/tariff_base.png')
#     await client.send_message(event.input_sender, 'Тут описание тарифа Базовый',
#                               buttons=buttons.keyboard_subscription_base)
# elif event.data == b'kcs3':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + '/tariff_advanced.png')
#     await client.send_message(event.input_sender, 'Тут описание тарифа Продвинутый',
#                               buttons=buttons.keyboard_subscription_advanced)
# elif event.data == b'kcs4':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + '/tariff_professional.jpg')
#     await client.send_message(event.input_sender, 'Тут описание тарифа Профессиональный',
#                               buttons=buttons.keyboard_subscription_professional)
# elif event.data == b'kcs-1':
#     await menu.profile_menu(event, client, engine)
# #   TODO добавить описание подписок
# #   TODO добавить таблицу сравнения подписок
# elif event.data == b'kss1' or event.data == b'kss2' or event.data == b'kss3' or event.data == b'kss4':
#     global PAYMENT_AGGREGATOR
#     if PAYMENT_AGGREGATOR is None:
#         PAYMENT_AGGREGATOR = PaymentAgregator()
#         PAYMENT_AGGREGATOR.creator('Free Kassa')
#     aggregator_status = PAYMENT_AGGREGATOR.get_status()
#     global PAYMENT_AGGREGATOR_TIMER
#     if PAYMENT_AGGREGATOR_TIMER is not None:
#         delta = time.time() - PAYMENT_AGGREGATOR_TIMER
#         if delta >= 10:
#             aggregator_status = PAYMENT_AGGREGATOR.get_status()
#         else:
#             time.sleep(10 - delta)
#             aggregator_status = PAYMENT_AGGREGATOR.get_status()
#     else:
#         PAYMENT_AGGREGATOR_TIMER = time.time()
#         aggregator_status = PAYMENT_AGGREGATOR.get_status()
#     # print(aggregator_status)
#     if aggregator_status == 'error':
#         # print("Error description:" + PAYMENT_AGGREGATOR.get_last_error())
#         await client.send_message(event.input_sender, 'Упс. Что-то пошло не так.',
#                                   buttons=buttons.keyboard_subscription_start)
#         await event.edit()
#     else:
#         # print("user_id=" + str(sender_id.user_id))
#         order_id = str(uuid.uuid4()).replace('-', '')
#         print("OrderId:" + order_id)
#         summa = ""
#         kbd_label = ""
#         if event.data == b'kss1':
#             summa = "15.00"
#             kbd_label = "Оплатить ($15)"
#         elif event.data == b'kss2':
#             summa = "25.00"
#             kbd_label = "Оплатить ($25)"
#         elif event.data == b'kss3':
#             summa = "30.00"
#             kbd_label = "Оплатить ($30)"
#         elif event.data == b'kss2':
#             summa = "40.00"
#             kbd_label = "Оплатить ($40)"
#
#         print("Summa:" + summa)
#         payment_link = PAYMENT_AGGREGATOR.get_payment_link(order_id, summa)
#         print(payment_link)
#         keyboard_subscr_start_inst = [
#             [
#                 Button.url('\U0001F3E6  ' + kbd_label, payment_link)
#             ]
#         ]
#
#         paymsg = await client.send_message(event.input_sender,
#                                            'Для оплаты тарифа Start нажмите кнопку Оплатить\n'
#                                            '(Инструкция по оплате [тут](https://telegra.ph/Rrrtt-10-13)! )',
#                                            link_preview=True,
#                                            buttons=keyboard_subscr_start_inst)
#         await event.edit()
#         sender = event.input_sender
#         msg_id = utils.get_message_id(paymsg)
#         global ORDER_MAP
#         ORDER_MAP[order_id] = (sender_id, msg_id)
#         dt = datetime.now()
#         dt_int = datetime2int(dt)
#         await sql.insert_into_payment_message(order_id, sender_id, msg_id, dt_int, engine)


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
