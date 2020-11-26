#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import yaml
import csv
import logging
import random
import time
import uuid
import base64
import rsa
import asyncio
import dialogflow_v2 as dialogflow

from sqlalchemy import create_engine
from alchemysession import AlchemySessionContainer

from telethon import events, TelegramClient
from telethon.tl.custom import Button
from telethon.tl.types import PeerUser

from aiohttp import web
from payments.payagregator import PaymentAgregator


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
    level=logging.INFO)
logging.getLogger('telethon').setLevel(level=logging.INFO)

# ============================== Credentials and GLOBALS ======================

PAYMENT_TOKEN = conf['TELEGRAM']['PAYMENT_TOKEN']
PAYMENT_SUCCESS_LISTEN = conf['TELEGRAM']['PAYMENT_SUCCESS_LISTEN']
PAYMENT_SUCCESS_LISTEN_PORT = conf['TELEGRAM']['PAYMENT_SUCCESS_LISTEN_PORT']
ORDER_MAP = {}
PUBKEY = None
PAYMENT_AGGREGATOR = None
app = web.Application()

YAHOO_PATH = conf['PATHS']['YAHOO_PATH']
IMAGES_OUT_PATH = conf['PATHS']['IMAGES_OUT_PATH']
TARIFF_IMAGES = conf['TELEGRAM']['TARIFF_IMAGES']
BTC = conf['CREDENTIALS']['BTC']
ETH = conf['CREDENTIALS']['ETH']
API_KEY = conf['TELEGRAM']['API_KEY']
API_HASH = conf['TELEGRAM']['API_HASH']
UPSILON = conf['TELEGRAM']['UPSILON']
OWNER = conf['TELEGRAM']['OWNER']
SERVICE_CHAT = conf['TELEGRAM']['SERVICE_CHAT']

# ============================== SQL Connect ======================

SQL_DB_NAME = conf['SQL']['DB_NAME']
SQL_USER = conf['SQL']['DB_USER']
SQL_PASSWORD = conf['SQL']['DB_PASSWORD']
SQL_URI = 'mysql+pymysql://{}:{}@localhost/{}?charset=utf8'.format(SQL_USER, SQL_PASSWORD, SQL_DB_NAME)

engine = create_engine(SQL_URI, pool_recycle=3600)
container = AlchemySessionContainer(engine=engine)
alchemy_session = container.new_session('default')
connection = engine.raw_connection()


# ============================== Payment request handler ======================
# process only requests with correct payment token
async def handle(request):
    if request.match_info.get("token") == PAYMENT_TOKEN:
        request_json = await request.json()
        # print("JSON:" + str(request_json))
        order_id = str(request_json['order_id'])
        summ = str(request_json['summ'])
        data = ":" + order_id + ":" + summ + ":"
        sign = base64.b64decode(str(request_json['sign']))

        if PUBKEY is None:
            return web.Response(status=403)

        try:
            rsa.verify(data.encode(), sign, PUBKEY)
        except:
            print("Verification failed")
            return web.Response(status=403)

        global ORDER_MAP
        value = ORDER_MAP.get(order_id)
        if value is not None:
            print("Send message \"payment is ok\"")
            sender, entity, message = value
            await client.delete_messages(entity, message)
            tarif_str = ""
            if summ == "15":
                tarif_str = '__Тариф: Старт__\n'
            elif summ == "25":
                tarif_str = '__Тариф: Базовый__\n'
            await client.send_message(sender,
                                      'Оплата прошла успешно:\n'
                                      + tarif_str
                                      + '__Ордер: ' + order_id + '__\n'
                                      + '__Сумма: ' + summ + '__\n'
                                      + '**Спасибо, что пользуетесь моими услугами!**')
            ORDER_MAP.pop(order_id)
            return web.Response(status=200)
        else:
            print("Global SenderID is None")
            return web.Response(status=403)

    else:
        return web.Response(status=403)


app.router.add_post("/{token}/", handle)

# ============================== Environment Setup ======================
# ============================== Init ===================================
print('Before start')
client = TelegramClient(alchemy_session, API_KEY, API_HASH).start(bot_token=UPSILON)
print(client)


# ============================== Init ===================================
# ============================== Dialogflow =============================


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client_d = dialogflow.SessionsClient()
    session = session_client_d.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client_d.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text


# ============================== Dialogflow =============================
# ============================== Commands ===============================


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    referral = str(event.original_update.message.message).split(' ')
    if len(referral) > 1:
        user_profile = await user_search(referral[1])
        inc = user_profile[13] + 1
        await db_save_referral(inc, referral[1])
    else:
        pass
    sender_id = event.original_update.message.peer_id.user_id
    entity = await client.get_input_entity(sender_id)
    lang = await client.get_entity(PeerUser(sender_id))
    await db_save_lang(str(lang.lang_code), sender_id)
    keyboard_start = [
        [Button.text('Главное меню', resize=True), Button.text('Профиль', resize=True)]
        # [Button.text('Помощь', resize=True), Button.text('Donate', resize=True)]
    ]

    message = await client.send_message(entity=entity, message='__Stand by__')
    time.sleep(0.9)
    await client.edit_message(message, '10% |=> \nInitializing Upsilon AI')
    time.sleep(0.8)
    await client.edit_message(message, '20% |===> \nAttempting to Lock Identity')
    time.sleep(0.7)
    await client.edit_message(message, '30% |=====> \nPreparing Registry ')
    time.sleep(0.6)
    await client.edit_message(message, '40% |=======> \nGathering Search Queries')
    time.sleep(0.5)
    await client.edit_message(message, '50% |=========> \nScraping All Known Financial Data Sources')
    time.sleep(0.4)
    await client.edit_message(message, '60% |===========> \nExtracting Resources')
    time.sleep(0.5)
    await client.edit_message(message, '70% |=============> \nRecompiling Semantic Core')
    time.sleep(0.6)
    await client.edit_message(message, '80% |===============> \nRouting Neural Infrastructure')
    time.sleep(0.7)
    await client.edit_message(message, '90% |=================> \nMixing Genetic Pool')
    time.sleep(0.5)
    await client.edit_message(message, '100%|==================> \nUpsilon at your disposal')
    time.sleep(0.3)
    await client.delete_messages(entity, message)
    # await client.send_file(entity, 'telegram/fish_swarm.gif')
    await client.send_message(entity, 'Приветствую вас! Я Ипсилон — самый продвинутый ИИ '
                                      'для трейдинга и управления инвестициями.', buttons=keyboard_start)


@client.on(events.NewMessage(pattern='Главное меню'))
async def tools(event):
    await client.send_message(event.input_sender, 'Главное меню', buttons=keyboard_0)


@client.on(events.NewMessage(pattern='Профиль'))
async def profile(event):
    keyboard_z1 = [
        [Button.inline('\U0001F516	  ' + 'Подписки', b'z1')],
        [Button.inline('\U0001F91D	  ' + 'Пригласить друга', b'z2')]
    ]
    sender_id = event.input_sender
    await client.get_input_entity(sender_id)
    user_profile = await user_search(sender_id.user_id)
    await client.send_message(event.input_sender,
                              f'\U0001F464 : {user_profile[4]}' + '\n' +
                              f'Имя: {user_profile[6]}' + '\n' +
                              '\n' +
                              f'баланс: {user_profile[7]}' + '\n' +
                              f'Подписка действительна до: {user_profile[8]}' + '\n' +
                              f'Приглашено: {user_profile[12]}' + '\n' +
                              f'Уровень подписки: {user_profile[13]}', buttons=keyboard_z1)


@client.on(events.NewMessage(pattern='Помощь'))
async def helper(event):
    await client.send_message(event.input_sender,
                              '**Задавайте вопросы прямо или воспользуйтесь меню**' + '\n' +
                              '\n' +
                              '**Я умею:**' + '\n' +
                              '\n' +
                              '\U0001F7E2  Общаться и отвечать вопросы по разным темам, включая инвестиции и трейдинг'
                              + '\n' +
                              '\U0001F7E2  Мониторить, отслеживать и анализировать финансовые Главное меню,'
                              ' включая криптовалюту \U0001FA99' + '\n' +
                              '\U0001F7E2  Составлять и отлеживать инвест портфели \U0001F4BC	' + '\n' +
                              '\U0001F7E2  Строить вероятностные модели финансовых рынков' + '\n' +
                              '\U0001F7E2  Проектировать инвестиционные портфели по запросу' + '\n' +
                              '\U0001F7E2  Помогать с поддержанием и ведением инвестиционных портфелей' + '\n'
                              '\U0001F7E2  Анализировать финансовые данные \U0001F52C и даже гуглить \U0001F604' + '\n'
                              '\U0001F7E2  Напоминать о необходимости действий на рынке, сигналить \U0001F514' + '\n'
                              '\U0001F7E2  Отслеживать волатильность и прочие биржевые статистики ')
    await client.send_message(event.input_sender,
                              'Есть только Ипсилон! \U0001F9B8 У меня нет команды поддержки. '
                              'Моя задача совершенствоваться'
                              ' и учиться самому. Я понимаю предустановленные команды, но я еще в '
                              'процессе обучения \U0001F47C \U0001F393'
                              ' общению, некоторые из наших диалогов могут "зависнуть" с моей стороны или я могу'
                              ' отвечать не впопад. Со временем это пройдет \U0001F643' + '\n'
                              'Я смогу ответить на некоторые вопросы после обдумывания, но старайся задавать '
                              'вопросы лаконично.' + '\n'
                              'Чтобы быть естественным, необходимо уметь притворяться. Моя личность станет такой, какой'
                              'вы меня сделаете в процессе нашего взаимодействия.')


@client.on(events.NewMessage(pattern='Donate'))
async def premium(event):
    await client.send_message(event.input_sender, BTC + '\n' +
                              ETH)


@client.on(events.NewMessage(pattern='/to'))  # TODO Сделакть блокирующую функцию для ДФ
async def send_to(event):
    parse = str(event.text).split('_')
    try:
        sender_id = event.input_sender
    except ValueError as e:
        sender_id = await event.get_input_sender()
        logging.exception(e, 'Making network request to find the input sender')
    try:
        if int(sender_id.user_id) == int(OWNER):
            entity = await client.get_entity(int(parse[1]))
            await client.send_message(entity, parse[2])
        else:
            await client.send_message(sender_id, 'Order dismissed!')
    except ValueError as e:
        logging.exception(e, 'Some errors from send_to()')


@client.on(events.NewMessage(pattern='/publish_to'))
async def publish_to(event):
    parse = str(event.text).split('|')
    try:
        channel = await client.get_entity('https://t.me/' + str(parse[1]))
    except ValueError as e:
        logging.exception(e, 'Can\'t get channel entity')
    try:
        if int(event.input_sender.user_id) == int(OWNER):
            await client.send_message(channel, parse[2])
        else:
            await client.send_message(event.input_sender, 'Order dismissed!')
    except ValueError as e:
        logging.exception(e, 'Some errors from publish_to()')


@client.on(events.NewMessage())
async def dialog_flow(event):
    no_match = ['\U0001F9D0', '\U0001F633', 'Ясно', 'Мы должны подумать над этим']
    fallback = random.choice(no_match)
    try:
        sender_id = event.input_sender
    except ValueError as e:
        sender_id = await event.get_input_sender()
        logging.exception(e, 'Making network request to find the input sender')
    if not any(value in event.text for value in
               ('/start', '/help', '/publish_to', '/to', 'Главное меню', 'Профиль', 'Помощь', 'Donate')):
        user_message = event.text
        project_id = 'common-bot-1'
        try:
            dialogflow_answer = detect_intent_texts(project_id, sender_id.user_id, user_message, 'ru-RU')
            await client.send_message(sender_id, dialogflow_answer)
            await client.send_message(-1001262211476, str(sender_id.user_id) +
                                      '  \n' + str(event.text) +
                                      '  \n' + dialogflow_answer)
            # TODO Внимание! изменить айди чата при деплое
        except ValueError as e:
            logging.exception(e, 'Dialogflow response failure')
            await client.send_message(sender_id, fallback)


# ============================== Commands ===============================
# ============================== Service Commands =======================


@client.on(events.ChatAction)
async def get_participants_from_chat(event):
    if event.user_joined or event.user_added:
        # print(event.action_message.to_id, '1XXXXXXXXXX')
        # print(event.action_message.to_id.chat_id, '3XXXXXXXXXX')
        # entity = await client.get_entity(event.action_message.to_id)
        # chat = await event.get_input_chat()
        # print(chat, '1dgggdg')
        try:
            participants = await client.get_participants(event.action_message.to_id)
        except AttributeError as e:
            logging.exception(e,
                              'NoneType object has no attribute to_id ' + '\n' + 'Probably bot was added to some chat')
        for user in participants:
            if user.id is not None:
                entity = await client.get_entity(PeerUser(user.id))
                print('Dump complete!')
                # print(user.access_hash, user.id, user.username, user.first_name, user.last_name, entity)
                # TODO Добавить в модели поля bot=True, scam=False


# ============================== Service Commands =======================
# ============================== CallbackQuery ==========================


keyboard_0 = [
    [
        Button.inline('\U0001F52C   ' + 'Анализ рынков', b'a1')
    ],
    [
        Button.inline('\U0001F9EC   ' + 'Конструктор стратегий', b'a2')
    ],
    [
        Button.inline('\U0001F321  ' + 'Калькуляторы', b'a3')
    ],
    [
        Button.inline('\U0001F9BE  ' + 'Управление', b'a4')
    ],
    [
        Button.inline('\U0001F691  ' + 'Инструкции', b'a5')
    ],
    [
        Button.inline('\U0001F393  ' + 'Образование', b'a6')
    ],
    [
        Button.inline('\U0001F92C  ' + 'Налоги', b'a7')
    ],
    [
        Button.inline('\U0001F5C3  ' + 'Агрегатор новостей', b'a8')
    ]
]

keyboard_a1 = [
    [
        Button.inline('\U0001F5FD  ' + 'Рынок США', b'a1a1')
    ],
    [
        Button.inline('\U0001F513  ' + 'Рынок криптовалют', b'a1a2')
    ],
    [
        Button.inline('\U0001F43B  ' + 'Рынок РФ', b'a1a3')
    ],
    [
        Button.inline('\U0001F504  ' + 'ETF потоки', b'a1a4')
    ],
    [
        Button.inline('\U0001F30D  ' + 'Мировые рынки в картах', b'a1a5')
    ],
    [
        Button.inline('\U0001F9ED   ' + 'Основные макро индикаторы', b'a1a6')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a1_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a1a-1')
    ]
]

keyboard_a2 = [
    [
        Button.inline('\U0001F4BC   ' + 'Твой профиль риска', b'a2a1')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Оценка/аудит портфеля', b'a2a2')
    ],
    [
        Button.inline('\U0001F4BC  ' + '"Парковочный" портфель без риска', b'a2a3')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Всепогодный портфель', b'a2a4')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Сбалансированный портфель', b'a2a5')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Агрессивный портфель', b'a2a6')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Крипто портфель', b'a2a7')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Трейдинг/Дневные стратегии', b'a2a8')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a2_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a2a-1')
    ]
]
keyboard_a3 = [
    [
        Button.inline('\U0001F50E  ' + 'Рассчет количества акций для портфеля', b'a3a1')
    ],
    [
        Button.inline('\U0001F50E  ' + 'Симуляция 10 летней доходности', b'a3a2')
    ],
    [
        Button.inline('\U0001F50E  ' + 'Рассчет оптимального размера взносов', b'a3a3')
    ],
    [
        Button.inline('\U0001F50E  ' + 'Рассчет безопасного размера вывода средств', b'a3a4')
    ],
    [
        Button.inline('\U0001F50E  ' + 'Сложный процент', b'a3a5')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a3_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a3a-1')
    ]
]
keyboard_a4 = [
    [
        Button.inline('\U0001F4A1 ' + 'Маркетплейс управляющих', b'a4a1')
    ],
    [
        Button.inline('\U0001F6E1   ' + 'Стать управляющим', b'a4a2')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a4_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a4a-1')
    ]
]

keyboard_a5 = [
    [
        Button.inline('\U0001F50D   ' + 'Как ... /instruction01', b'a5a1')
    ],
    [
        Button.inline('\U0001F50D   ' + 'Что ... /instruction02', b'a5a2')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a5_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a5a-1')
    ]
]

keyboard_a6 = [
    [
        Button.inline('\U0001F476   ' + 'Основы инвестирования', b'a6a1')
    ],
    [
        Button.inline('\U0001F468  ' + 'Как собрать свой первый портфель', b'a6a2')
    ],
    [
        Button.inline('\U0001F9D4  ' + 'Профессиональные решения', b'a6a3')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a6_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a6a-1')
    ]
]

keyboard_a7 = [
    [
        Button.inline('\U0001F5DC  ' + 'Оптимизация налогов', b'a7a1')
    ],
    [
        Button.inline('\U0001F46E  ' + 'Подготовка налоговых деклараций', b'a7a2')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a7_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a7a-1')
    ]
]

keyboard_a8 = [
    [
        Button.inline('\U0001F5DE  ' + 'Поставщики новостей', b'a9a1')
    ],
    [
        Button.inline('\U0001F4B1   ' + 'Тикеры', b'a9a2')
    ]
]

keyboard_a8_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a8a-1')
    ]
]

keyboard_core_macro = [
    [
        Button.inline('\U0001F3E6  ' + 'Interest Rates', b'cm1')
    ],
    [
        Button.inline('\U0001F321	  ' + 'Inflation Rates', b'cm2')
    ],
    [
        Button.inline('\U0001F525  ' + 'Unemployment Rates', b'cm3')
    ],
    [
        Button.inline('\U0001F3E2  ' + 'Composite PMI', b'cm4')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-2')
    ]
]

keyboard_core_macro_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-1')
    ]
]

# ============================== Кнопки подписок =============================
keyboard_core_subscriptions = [
    [
        Button.inline('\U0001F3E6  ' + 'Старт', b'kcs1')
    ],
    [
        Button.inline('\U0001F321	  ' + 'Базовый', b'kcs2')
    ],
    [
        Button.inline('\U0001F525  ' + 'Продвинутый', b'kcs3')
    ],
    [
        Button.inline('\U0001F3E2  ' + 'Профессиональный', b'kcs4')
    ]
]

keyboard_subscription_start = [
    [
        Button.inline('\U0001F3E6  ' + '$15', b'kss1')
    ]
]
keyboard_subscription_base = [
    [
        Button.inline('\U0001F3E6  ' + '$25', b'kss2')
    ]
]
keyboard_subscription_advanced = [
    [
        Button.inline('\U0001F3E6  ' + '$30', b'kss3')
    ]
]
keyboard_subscription_professional = [
    [
        Button.inline('\U0001F3E6  ' + '$40', b'kss4')
    ]
]
# TODO поменять иконки кнопок


@client.on(events.CallbackQuery)
async def callback(event):
    sender_id = event.original_update.user_id
    entity = await client.get_input_entity(sender_id)

    # ============================== Главное меню 1 уровень=============================
    if event.data == b'a1':
        await client.send_message(event.input_sender, 'Анализ рынков', buttons=keyboard_a1)
        await event.edit()
    elif event.data == b'a2':
        await client.send_message(event.input_sender, 'Конструктор портфелей', buttons=keyboard_a2)
        await event.edit()
    elif event.data == b'a3':
        await client.send_message(event.input_sender, 'Калькуляторы', buttons=keyboard_a3)
        await event.edit()
    elif event.data == b'a4':
        await client.send_message(event.input_sender, 'Управление', buttons=keyboard_a4)
        await event.edit()
    elif event.data == b'a5':
        await client.send_message(event.input_sender, 'Инструкции', buttons=keyboard_a5)
        await event.edit()
    elif event.data == b'a6':
        await client.send_message(event.input_sender, 'Образование', buttons=keyboard_a6)
        await event.edit()
    elif event.data == b'a7':
        await client.send_message(event.input_sender, 'Налоги', buttons=keyboard_a7)
        await event.edit()
    elif event.data == b'a8':
        await client.send_message(event.input_sender, 'Агрегатор новостей', buttons=keyboard_a8)
        await event.edit()
    elif event.data == b'main':
        await client.send_message(event.input_sender, 'Главное меню', buttons=keyboard_0)
        await event.edit()

    # ============================== Анализ рынков 2 уровень=============================
    elif event.data == b'a1a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(event.input_sender, 'Количество растущих/падающих акций и объёмы за сегодня')
        filename = os.path.join(IMAGES_OUT_PATH, 'adv.csv')
        with open(filename, newline='') as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                await client.send_message(entity=entity, message=f'{row}')
        await client.send_message(event.input_sender, 'Общая картина')
        await client.send_file(entity, IMAGES_OUT_PATH + 'sectors.png')
        await client.send_message(event.input_sender, 'Волатильность и барометр жадности/страха')
        await client.send_file(entity, IMAGES_OUT_PATH + 'volatility.png')
        await client.send_message(event.input_sender, 'Тепловая карта 1-day performance')
        await client.send_file(entity, IMAGES_OUT_PATH + 'treemap.png')
        await client.edit_message(message, 'Анализ рынка США')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать графики выше? /instruction01',
                                  buttons=keyboard_a1_back)
    elif event.data == b'a1a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(event.input_sender, 'Общая картина')
        await client.send_file(entity, IMAGES_OUT_PATH + 'crypto.png')
        await client.send_message(event.input_sender, 'Тепловая карта 1-day performance')
        await client.send_file(entity, IMAGES_OUT_PATH + 'coins_treemap.png')
        await client.edit_message(message, 'Рынок криптовалют')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать графики выше? /instruction01',
                                  buttons=keyboard_a1_back)
    elif event.data == b'a1a3':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(event.input_sender, 'Общая картина')
        await client.send_file(entity, IMAGES_OUT_PATH + 'rtsi.png')
        await client.edit_message(message, 'Рынок РФ')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать графики выше? /instruction01',
                                  buttons=keyboard_a1_back)
    elif event.data == b'a1a4':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(entity=entity, message='Денежные потоки в миллионах USD')
        await client.send_message(entity=entity, message='Денежные потоки SPY')
        await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_SPY.png')
        await client.send_message(entity=entity, message='Денежные потоки QQQ')
        await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_QQQ.png')
        await client.send_message(entity=entity, message='Денежные потоки VTI')
        await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VTI.png')
        await client.send_message(entity=entity, message='Денежные потоки VEA')
        await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VEA.png')
        await client.send_message(entity=entity, message='Денежные потоки VWO')
        await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VWO.png')
        await client.send_message(entity=entity, message='Денежные потоки LQD')
        await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_LQD.png')
        await client.send_message(entity=entity, message='Денежные потоки VXX')
        await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VXX.png')
        await client.send_message(entity=entity, message='Денежные потоки SHY')
        await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_SHY.png')
        await client.send_message(entity=entity, message='Денежные потоки TLT')
        await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_TLT.png')
        await client.edit_message(message, 'Ежедневные денежные потоки основных ETF за месяц')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать денежные потоки? /instruction02',
                                  buttons=keyboard_a1_back)
    elif event.data == b'a1a5':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(event.input_sender, 'Общая картина 1-day performance')
        await client.send_file(entity, IMAGES_OUT_PATH + 'global_treemap.png')
        await client.send_message(event.input_sender, 'Общая картина YTD performance')
        await client.send_message(event.input_sender, 'Общая картина bubble map')
        await client.edit_message(message, 'Мировые рынки в картах')
        await event.edit()
        await client.send_message(event.input_sender, 'Как ? /instruction02',
                                  buttons=keyboard_a1_back)
    elif event.data == b'a1a6':
        await client.send_message(event.input_sender, 'Основные макро индикаторы', buttons=keyboard_core_macro)
        await event.edit()
    elif event.data == b'a1a-1':
        await client.send_message(event.input_sender, 'Анализ рынков', buttons=keyboard_a1)
        await event.edit()

    # ============================== Конструктор стратегий =============================
    elif event.data == b'a2a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Твой профиль риска')
        await event.edit()
        await client.send_message(event.input_sender, 'Зачем нужно знать свой профиль риска? /instruction03',
                                  buttons=keyboard_a2_back)
    elif event.data == b'a2a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Оценка/аудит портфеля')
        await event.edit()
        await client.send_message(event.input_sender, 'Зачем проводить аудит своего портфеля? /instruction04',
                                  buttons=keyboard_a2_back)
    elif event.data == b'a2a3':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, '"Парковочный" портфель без риска')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать парковочный портфель? /instruction05',
                                  buttons=keyboard_a2_back)
    elif event.data == b'a2a4':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Всепогодный портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать всепогодный портфель? /instruction06',
                                  buttons=keyboard_a2_back)
    elif event.data == b'a2a5':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Сбалансированный портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать сбалансированный портфель? /instruction07',
                                  buttons=keyboard_a2_back)
    elif event.data == b'a2a6':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Агрессивный портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать агрессивный портфель? /instruction08',
                                  buttons=keyboard_a2_back)
    elif event.data == b'a2a7':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Крипто портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать крипто портфель? /instruction09',
                                  buttons=keyboard_a2_back)
    elif event.data == b'a2a8':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Трейдинг/Дневные стратегии')
        await event.edit()
        await client.send_message(event.input_sender, 'Подходит ли вам трейдинг? /instruction10',
                                  buttons=keyboard_a2_back)
    elif event.data == b'a2a-1':
        await client.send_message(event.input_sender, 'Конструктор стратегий', buttons=keyboard_a2)
        await event.edit()

    # ============================== Калькуляторы =============================
    elif event.data == b'a3a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Рассчет количества акций для портфеля')
        await event.edit()
        await client.send_message(event.input_sender, 'Конвертация весов в количество? /instruction11',
                                  buttons=keyboard_a3_back)
    elif event.data == b'a3a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Симуляция 10 летней доходности')
        await event.edit()
        await client.send_message(event.input_sender,
                                  'Что ожидать от текущего портфеля в ближайшую декаду? /instruction12',
                                  buttons=keyboard_a3_back)
    elif event.data == b'a3a3':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Рассчет оптимального размера взносов')
        await event.edit()
        await client.send_message(event.input_sender, 'Почему взносы необходимы? /instruction13',
                                  buttons=keyboard_a3_back)
    elif event.data == b'a3a4':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Рассчет безопасного размера вывода средств')
        await event.edit()
        await client.send_message(event.input_sender, 'Сколько можно выводить средств? /instruction14',
                                  buttons=keyboard_a3_back)
    elif event.data == b'a3a5':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Сложный процент')
        await event.edit()
        await client.send_message(event.input_sender, 'Сложный процент в действии. /instruction15',
                                  buttons=keyboard_a3_back)
    elif event.data == b'a3a-1':
        await client.send_message(event.input_sender, 'Калькуляторы', buttons=keyboard_a3)
        await event.edit()

    # ============================== Управление =============================
    elif event.data == b'a4a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Маркетплейс управляющих')
        await event.edit()
        await client.send_message(event.input_sender, 'Все об управлени активами. /instruction16',
                                  buttons=keyboard_a4_back)
    elif event.data == b'a4a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Стать управляющим')
        await event.edit()
        await client.send_message(event.input_sender, 'Стать управляющим',
                                  buttons=keyboard_a4_back)
    elif event.data == b'a4a-1':
        await client.send_message(event.input_sender, 'Управление', buttons=keyboard_a4)
        await event.edit()

    # ============================== Инструкции =============================
    elif event.data == b'a5a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Как ... /instruction01')
        await event.edit()
        await client.send_message(event.input_sender, 'Как ... /instruction01',
                                  buttons=keyboard_a5_back)
    elif event.data == b'a5a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Что ... /instruction02')
        await event.edit()
        await client.send_message(event.input_sender, 'Что ... /instruction02',
                                  buttons=keyboard_a5_back)
    elif event.data == b'a5a-1':
        await client.send_message(event.input_sender, 'Инструкции', buttons=keyboard_a5)
        await event.edit()

    # ============================== Образовательные программы =============================
    elif event.data == b'a6a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Основы инвестирования')
        await event.edit()
        await client.send_message(event.input_sender, 'Основы инвестирования /instruction20',
                                  buttons=keyboard_a6_back)
    elif event.data == b'a6a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Как собрать свой первый портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Как собрать свой первый портфель /instruction21',
                                  buttons=keyboard_a6_back)
    elif event.data == b'a6a3':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Профессиональные решения')
        await event.edit()
        await client.send_message(event.input_sender, 'Профессиональные решения /instruction22',
                                  buttons=keyboard_a6_back)
    elif event.data == b'a6a-1':
        await client.send_message(event.input_sender, 'Образование', buttons=keyboard_a6)
        await event.edit()

    # ============================== Налоги =============================
    elif event.data == b'a7a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Оптимизация налогов')
        await event.edit()
        await client.send_message(event.input_sender, 'Оптимизация налогов /instruction30',
                                  buttons=keyboard_a7_back)
    elif event.data == b'a7a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Подготовка налоговых деклараций')
        await event.edit()
        await client.send_message(event.input_sender, 'Подготовка налоговых деклараций /instruction30',
                                  buttons=keyboard_a7_back)
    elif event.data == b'a7a-1':
        await client.send_message(event.input_sender, 'Налоги', buttons=keyboard_a7)
        await event.edit()

    # ============================== Агрегатор новостей =============================
    elif event.data == b'a8a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Поставщики новостей')
        await event.edit()
        await client.send_message(event.input_sender, 'Поставщики новостей',
                                  buttons=keyboard_a8_back)
    elif event.data == b'a8a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Тикеры')
        await event.edit()
        await client.send_message(event.input_sender, 'Тикеры',
                                  buttons=keyboard_a8_back)
    elif event.data == b'a8a-1':
        await client.send_message(event.input_sender, 'Агрегатор новостей', buttons=keyboard_a8)
        await event.edit()

    # elif event.data == b'a4a1':
    #     message = await client.send_message(entity=entity, message='Loading...')
    #     await client.send_file(entity, IMAGES_OUT_PATH + 'us_index.png')
    #     await client.edit_message(message, 'Ипсилон AI US Index')
    #     await event.edit()
    # elif event.data == b'a4a2':
    #     message = await client.send_message(entity=entity, message='Loading...')
    #     await client.send_file(entity, IMAGES_OUT_PATH + 'world_index.png')
    #     await client.edit_message(message, 'Ипсилон AI WORLD Index')
    #     await event.edit()

    # ============================== Основные макро данные =============================
    elif event.data == b'cm1':
        await client.send_message(entity=entity, message='Interest Rates')
        await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
        filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
        with open(filename, newline='') as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                if row[0] == 'Interest Rate':
                    new_row = ',  '.join(row)
                    await client.send_message(entity=entity, message=f'{new_row}')
        await event.edit()
        await client.send_message(event.input_sender, '________________________', buttons=keyboard_core_macro)
    elif event.data == b'cm2':
        await client.send_message(entity=entity, message='Interest Rates')
        await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
        filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
        with open(filename, newline='') as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                if row[0] == 'Inflation Rate':
                    new_row = ',  '.join(row)
                    await client.send_message(entity=entity, message=f'{new_row}')
        await event.edit()
        await client.send_message(event.input_sender, '________________________', buttons=keyboard_core_macro)
    elif event.data == b'cm3':
        await client.send_message(entity=entity, message='Interest Rates')
        await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
        filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
        with open(filename, newline='') as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                if row[0] == 'Unemployment Rate':
                    new_row = ',  '.join(row)
                    await client.send_message(entity=entity, message=f'{new_row}')
        await event.edit()
        await client.send_message(event.input_sender, '________________________', buttons=keyboard_core_macro)
    elif event.data == b'cm4':
        await client.send_message(entity=entity, message='Interest Rates')
        await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
        filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
        with open(filename, newline='') as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                if row[0] == 'Composite PMI':
                    new_row = ',  '.join(row)
                    await client.send_message(entity=entity, message=f'{new_row}')
        await event.edit()
        await client.send_message(event.input_sender, '________________________', buttons=keyboard_core_macro)
    elif event.data == b'cm-1':
        await client.send_message(event.input_sender, 'Назад', buttons=keyboard_core_macro_back)
        await event.edit()
    elif event.data == b'cm-2':
        await client.send_message(event.input_sender, 'Назад', buttons=keyboard_a1)
        await event.edit()

    # ============================== Subscriptions =============================
    elif event.data == b'z1':
        await client.send_message(event.input_sender, 'Уровень подписок', buttons=keyboard_core_subscriptions)
        await event.edit()
    elif event.data == b'kcs1':
        await client.send_file(event.input_sender, TARIFF_IMAGES + 'tariff_start.jpg')
        await client.send_message(event.input_sender, 'Тут описание тарифа Старт', buttons=keyboard_subscription_start)
        await event.edit()
    elif event.data == b'kcs2':
        await client.send_file(event.input_sender, TARIFF_IMAGES + '/tariff_base.png')
        await client.send_message(event.input_sender, 'Тут описание тарифа Базовый',
                                  buttons=keyboard_subscription_base)
    elif event.data == b'kcs3':
        await client.send_file(event.input_sender, TARIFF_IMAGES + '/tariff_advanced.png')
        await client.send_message(event.input_sender, 'Тут описание тарифа Продвинутый',
                                  buttons=keyboard_subscription_advanced)
    elif event.data == b'kcs4':
        await client.send_file(event.input_sender, TARIFF_IMAGES + '/tariff_professional.jpg')
        await client.send_message(event.input_sender, 'Тут описание тарифа Профессиональный',
                                  buttons=keyboard_subscription_professional)
    #   TODO добавить описание подписок
    #   TODO добавить таблицу сравнения подписок
    #   TODO добавить кнопку "Назад"
    elif event.data == b'kss1' or event.data == b'kss2' or event.data == b'kss3' or event.data == b'kss4':
        global PAYMENT_AGGREGATOR
        if PAYMENT_AGGREGATOR is None:
            PAYMENT_AGGREGATOR = PaymentAgregator()
            PAYMENT_AGGREGATOR.creator('Free Kassa')
        agregator_status = PAYMENT_AGGREGATOR.get_status()
        # print(agregator_status)
        if agregator_status == 'error':
            # print("Error description:" + PAYMENT_AGGREGATOR.get_last_error())
            await client.send_message(event.input_sender, 'Упс. Что-то пошло не так.',
                                      buttons=keyboard_subscription_start)
            await event.edit()
        else:
            # print("user_id=" + str(sender_id.user_id))
            order_id = uuid.uuid4().__str__().replace('-', '')
            print("OrderId:" + order_id)
            summ = ""
            kbd_label = ""
            if event.data == b'kss1':
                summ = "15.00"
                kbd_label = "Оплатить ($15)"
            elif event.data == b'kss2':
                summ = "25.00"
                kbd_label = "Оплатить ($25)"
            elif event.data == b'kss3':
                summ = "30.00"
                kbd_label = "Оплатить ($30)"
            elif event.data == b'kss2':
                summ = "40.00"
                kbd_label = "Оплатить ($40)"

            print("Summ:" + summ)
            payment_link = PAYMENT_AGGREGATOR.get_payment_link(order_id, summ)
            print(payment_link)
            keyboard_subscr_start_inst = [
                [
                    Button.url('\U0001F3E6  ' + kbd_label, payment_link)
                ]
            ]

            paymsg = await client.send_message(event.input_sender,
                                               'Для оплаты тарифа Start нажмите кнопку Оплатить\n'
                                               '(Инструкция по оплате [тут](https://telegra.ph/Rrrtt-10-13)! )',
                                               link_preview=True,
                                               buttons=keyboard_subscr_start_inst)
            await event.edit()
            sender = event.input_sender
            global ORDER_MAP
            ORDER_MAP[order_id] = (sender, entity, paymsg)

    # ============================== END Subscriptions  =============================

    elif event.data == b'z2':
        await client.send_message(event.input_sender,
                                  'Вы можете попросить друга запустить бота и получить бесплатную'
                                  ' подписку. '
                                  'Проще всего это сделать через групповые чаты' + '\n' +
                                  f'[https://t.me/UpsilonBot?start={sender_id}]'
                                  f'(https://t.me/UpsilonBot?start={sender_id})')
        # TODO Изменить на оригинал
        await event.edit()


# ============================== CallbackQuery ==========================

# models.Category.objects.filter(is_visible=True).all()}


async def user_search(identifier):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM django_telethon_session_telethonentity WHERE identifier = %s", [identifier])
        row = cursor.fetchone()
    return row


async def db_save_lang(value, identifier):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE django_telethon_session_telethonentity SET profile_lang = %s WHERE identifier = %s",
                       [value, identifier])


async def db_save_referral(value, identifier):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE django_telethon_session_telethonentity SET referral = %s WHERE identifier = %s",
                       [value, identifier])


# Стартуем вебсервер для прослушки приходящих событий об успешных платежах
async def webserver_starter():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, PAYMENT_SUCCESS_LISTEN, PAYMENT_SUCCESS_LISTEN_PORT)
    await site.start()
    print("Web Server was started!")


def main():
    # Подгружаем публичный ключ для проверки подписи данных об успешных платежах
    with open('/home/gene/projects/upsilon/config/key.pub', mode='rb') as public_file:
        key_data = public_file.read()
        global PUBKEY
        PUBKEY = rsa.PublicKey.load_pkcs1_openssl_pem(key_data)

    # Стартуем веб сервер с отдельным event loop
    print("__Try start web server__")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(webserver_starter())
    print("__Try start tlethon client__")

    # Старт клиента Телетон
    client.run_until_disconnected()

    # if not os.path.exists(results_path):
    #     os.makedirs(results_path)


if __name__ == '__main__':
    print("Starting sequence")
    print(sys.path)
    main()

