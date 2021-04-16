import datetime
import sys
from typing import Any
from telethon import utils
from project_shared import *
from telethon import functions, types

ORDER_MAP = {}
OLD_MESSAGE_MAP = {}
ANSWERS_MAP = [
    # Ваша цель:
    #   Общее благосостояние", b'1'           --  1
    #   Большие покупки - дом, машина", b'2'  --  0
    #   Учеба детей, свадьба", b'3'           --  -1
    #   Пенсия", b'4'                         --  -1
    #   Пассивный доход", b'5'                --  0
    {b'1': 1, b'2': 0, b'3': -1, b'4': -1, b'5': 0},
    # Что из перечисленного описывает вашу ситуацию:"
    #   Я резидент СНГ, мой брокер из СНГ', b'1'   -- 0
    #   Я резидент СНГ, мой брокер из ЕС', b'2'    -- 0
    #   Я резидент СНГ, мой брокер из США', b'3'   -- 0
    #   Я резидент ЕС, мой брокер из США', b'4'    -- 0
    #   Я резидент ЕС, мой брокер из ЕС', b'5'     -- 0
    #   Я резидент США, мой брокер из США', b'6'   -- 0
    #   У меня нет брокерского счета и я резидент СНГ', b'7'
    {b'1': 0, b'2': 0, b'3': 0, b'4': 0, b'5': 0, b'6': 0, b'7': 0},
    # Если у тебя есть брокерский счет, можешь ли ты покупать ETF-фонды"
    #   Да', b'1'      -- 0
    #   Нет', b'2'     -- 0
    #   Незнаю', b'3'  -- 0
    {b'1': 0, b'2': 0, b'3': 0},
    # Нуждаетесь ли вы в средствах выделенных для инвестиций?"
    #   Да,эти средства могут понадобиться', b'1'  -- -1
    #   Нет, это свободные средства', b'2'         -- 1
    {b'1': -1, b'2': 1},
    # Планируете ли Вы выводить деньги с брокерского счета?"
    #   Да, регулярно', b'1'       -- -1
    #   Иногда, по случаю', b'2'   -- 0
    #   Нет', b'3'                 -- 1
    {b'1': -1, b'2': 0, b'3': 1},
    # Будете ли Вы делать дополнительные вложения?"
    #   Да, регулярно', b'1'                        -- 2
    #   Иногда, по случаю', b'2'                    -- 1
    #   Дополнительных вложений не планирую', b'3'  -- 0
    {b'1': 2, b'2': 1, b'3': 0},
    # Срок вложений
    #   Меньше года', b'1'   -- -2
    #   1-3 года', b'2'      -- -1
    #   3-5 лет', b'3'       -- 0
    #   5-10 лет', b'4'      -- 1
    #   Более 10 лет', b'5'  -- 2
    {b'1': -2, b'2': -1, b'3': 0, b'4': 1, b'5': 2},
    # Как часто Вы будете заниматься портфелем?"
    #   Ежедневно', b'1'   -- -1
    #   Ежемесячно', b'2'  -- 1
    #   Когда нужно', b'3' -- 1
    #   По случаю', b'4'   -- 1
    {b'1': -1, b'2': 1, b'3': 1, b'4': 1},
    # Какую доходность ожидаете?
    #   Выше уровня инфляции', b'1'   -- -2
    #   10%', b'2'                    -- -1
    #   10-15%', b'3'                 -- 0
    #   15-20%', b'4'                 -- 1
    #   Более 20%', b'5'              -- 2
    {b'1': -2, b'2': -1, b'3': 0, b'4': 1, b'5': 2},
    # Потеря какой части вашего вклада будет катастрофической?
    #   От -5% до -10%', b'1'  -- -2
    #   От -10% до -20%', b'2' -- -1
    #   От -20% до -35%', b'3' -- 0
    #   От -35% до -50%', b'4' -- 1
    #   До -75', b'5'          -- 2
    {b'1': -2, b'2': -1, b'3': 0, b'4': 1, b'5': 2},
    # Убыток в 20% от размера вашего вклада это:"
    #   Ничего страшного', b'1'   -- 1
    #   Терпимо', b'2'            -- 0
    #   Не приемлемо', b'3'       -- -1
    {b'1': 1, b'2': 0, b'3': -1},
    # Ваши действия во время просадки на рынке в 15%:
    #   Не знаю', b'1'                         -- -1
    #   Ничего не сделаю', b'2'                -- 1
    #   Продам все', b'3'                      -- -2
    #   Продам часть', b'4'                    -- -1
    #   Продам убыточные', b'5'                -- 0
    #   Продам прибыльные', b'6'               -- -1
    #   Докуплю', b'7'                         -- 2
    #   Что-то продам и что-то докуплю', b'8'  -- 1
    {b'1': -1, b'2': 1, b'3': -2, b'4': -1, b'5': 0, b'6': -1, b'7': 2, b'8': 1},
    # Вы предпочти бы акции:
    #   С доходностью в 20% годовых, но ранее эти акции падали на -50%', b'1'   -- 1
    #   С доходностью в 15% годовых, но ранее эти акции падали на -20%', b'2'   -- 0
    #   С доходностью в 150% годовых, но ранее эти акции падали на -70%', b'3'  -- 2
    #   С доходностью в 10% годовых, но ранее эти акции падали на -10%', b'4'   -- -1
    {b'1': 1, b'2': 0, b'3': 2, b'4': -1},
    # Вы предпочитаете:
    #   Гарантированные 50% от вашей суммы через 3 года', b'1'           -- -1
    #   35% - 80% через  5лет, но без гарантий, но не менее 35%', b'2'   -- 1
    {b'1': -1, b'2': 1}
    ]

IS_OLD_MSG_POLL_MAP = {}

INSPECTOR_TICKER_MAP = {}
INSPECTOR_PORTFOLIO_MAP = {}


def datetime2int(dt):
    return int(dt.strftime("%Y%m%d%H%M%S"))


def int2datetime(dt_int):
    return datetime.strptime(str(dt_int), "%Y%m%d%H%M%S")


async def save_old_message(user_id, msg):
    msg_id = utils.get_message_id(msg)
    global OLD_MESSAGE_MAP
    OLD_MESSAGE_MAP[user_id] = msg_id


async def delete_old_message(client, user_id):
    global OLD_MESSAGE_MAP
    old_msg_id = OLD_MESSAGE_MAP.get(user_id, None)
    if old_msg_id is not None:
        await client.delete_messages(user_id, old_msg_id)
        OLD_MESSAGE_MAP.pop(user_id)


def pop_old_msg_id(user_id):
    global OLD_MESSAGE_MAP
    if user_id in OLD_MESSAGE_MAP:
        OLD_MESSAGE_MAP.pop(user_id)


async def get_old_msg_id(user_id):
    old_msg_id = OLD_MESSAGE_MAP.get(user_id, None)
    return old_msg_id


def get_prifiler_score(qnumber, answer_number):
    global ANSWERS_MAP
    return ANSWERS_MAP[qnumber][answer_number]


async def is_old_msg_poll(user_id):
    global IS_OLD_MSG_POLL_MAP
    is_poll = IS_OLD_MSG_POLL_MAP.get(user_id, False)
    return is_poll


def set_old_msg_poll(user_id, val):
    global IS_OLD_MSG_POLL_MAP
    IS_OLD_MSG_POLL_MAP[user_id] = val


def pop_old_msg_poll(user_id):
    global IS_OLD_MSG_POLL_MAP
    if user_id in IS_OLD_MSG_POLL_MAP:
        IS_OLD_MSG_POLL_MAP.pop(user_id)


def get_order_data(order_id):
    global ORDER_MAP
    if order_id in ORDER_MAP:
        return ORDER_MAP.get(order_id)


def print_order_map():
    global ORDER_MAP
    debug(f'ORDER_MAP={ORDER_MAP}')


def pop_old_order(order_id):
    global ORDER_MAP
    if order_id in ORDER_MAP:
        ORDER_MAP.pop(order_id)


def set_inspector_ticker(user_id, ticker, size):
    global INSPECTOR_TICKER_MAP
    INSPECTOR_TICKER_MAP[user_id] = (ticker, size)


def get_inspector_ticker(user_id):
    global INSPECTOR_TICKER_MAP
    return INSPECTOR_TICKER_MAP.get(user_id, None)


def update_inspector_portfolio(user_id, ticker, size):
    global INSPECTOR_PORTFOLIO_MAP

    if user_id in INSPECTOR_PORTFOLIO_MAP:
        INSPECTOR_PORTFOLIO_MAP[user_id][ticker] = size
    else:
        portfolio = {ticker: size}
        INSPECTOR_PORTFOLIO_MAP[user_id] = portfolio


def get_inspector_portfolio(user_id):
    global INSPECTOR_PORTFOLIO_MAP
    return INSPECTOR_PORTFOLIO_MAP.get(user_id, None)


def clear_inspectors_data_by_user(user_id):
    global INSPECTOR_TICKER_MAP
    if user_id in INSPECTOR_TICKER_MAP:
        INSPECTOR_TICKER_MAP.pop(user_id)
    global INSPECTOR_PORTFOLIO_MAP
    if user_id in INSPECTOR_PORTFOLIO_MAP:
        INSPECTOR_PORTFOLIO_MAP.pop(user_id)


class Subscribe(object):
    def __init__(self, name="", level="Free", cost=0.0, describe="", duration=30.0, img_path=""):
        self.name = name
        self.level = level
        self.cost = cost
        self.describe = describe
        self.duration = duration
        self.img_path = img_path

    def get_name(self) -> str:
        return self.name

    def get_level(self) -> str:
        return self.level

    def get_cost(self) -> float:
        return self.cost

    def get_describe(self) -> str:
        return self.describe

    def get_duration(self) -> float:
        return self.duration

    def get_img_path(self) -> str:
        return self.img_path

    def __str__(self) -> str:
        return "Name: " + self.name + '\n' \
               + "Cost: " + str(self.cost) + '\n' \
               + "Duration: " + str(self.duration) + '\n' \
               + "Describe: " + self.describe + '\n' \
               + "Image path: " + self.img_path + '\n'


TARIFF_START_ID = 0
TARIFF_BASE_ID = 1
TARIFF_ADVANCED_ID = 2
TARIFF_PROFESSIONAL_ID = 3
TARIFF_COMPARE_ID = 4

SUBSCRIBES = {}


def create_subscribes(tariff_img_path):
    # Тариф Старт
    imgpath = tariff_img_path + '/tariff_start.jpg'
    tstart = Subscribe(name="Старт",
                       level="Start",
                       cost=15.00,
                       describe="Тут большое описание тарифа Старт. В нем доступны такие то функции. и т.д. и т.п.",
                       img_path=imgpath)
    # Тариф Базовый
    imgpath = tariff_img_path + '/tariff_base.png'
    tbase = Subscribe(name="Базовый",
                      level="Base",
                      cost=25.00,
                      describe="Тут большое описание тарифа Базовый. В нем доступны такие то функции. и т.д. и т.п.",
                      img_path=imgpath)
    # Тариф Продвинутый
    imgpath = tariff_img_path + '/tariff_advanced.png'
    tadv = Subscribe(name="Продвинутый",
                     level="Advanced",
                     cost=30.00,
                     describe="Тут большое описание тарифа Продвинутый. В нем доступны такие то функции. и т.д. и т.п.",
                     img_path=imgpath)
    # Тариф Профессиональный
    imgpath = tariff_img_path + '/tariff_professional.jpg'
    tprof = Subscribe(name="Профессиональный",
                      level="Professional",
                      cost=40.00,
                      describe="Тут большое описание тарифа Профессиональный. В нем доступны такие то функции. и т.д. "
                               "и т.п.",
                      img_path=imgpath)

    SUBSCRIBES[TARIFF_START_ID] = tstart
    SUBSCRIBES[TARIFF_BASE_ID] = tbase
    SUBSCRIBES[TARIFF_ADVANCED_ID] = tadv
    SUBSCRIBES[TARIFF_PROFESSIONAL_ID] = tprof

    # Таблица сравнения тарифов
    imgpath = tariff_img_path + '/tariff_compare.jpg'
    tcompare = Subscribe(name="Сравнение тарифов",
                         cost=0.0,
                         describe="Тут можно текстом описать чемже отличаются тарифы ",
                         img_path=imgpath)
    SUBSCRIBES[TARIFF_COMPARE_ID] = tprof
