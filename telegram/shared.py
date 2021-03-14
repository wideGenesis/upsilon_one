import datetime
import sys
from typing import Any
from telethon import utils
from project_shared import *
from telethon import functions, types

ORDER_MAP = {}
OLD_MESSAGE_MAP = {}
ANSWERS_MAP = [{b'1': 1, b'2': 0, b'3': -1, b'4': -1, b'5': 0},
               {b'1': 0, b'2': 0, b'3': 0, b'4': 0, b'5': 0, b'6': 0, b'7': 0},
               {b'1': 0, b'2': 0, b'3': 0},
               {b'1': -1, b'2': 1},
               {b'1': -1, b'2': 0, b'3': 1},
               {b'1': 2, b'2': 1, b'3': 0},
               {b'1': -2, b'2': -1, b'3': 0, b'4': 1, b'5': 2},
               {b'1': -1, b'2': 1, b'3': 1, b'4': 1},
               {b'1': -2, b'2': -1, b'3': 0, b'4': 1, b'5': 2},
               {b'1': -2, b'2': -1, b'3': 0, b'4': 1, b'5': 2},
               {b'1': 1, b'2': 0, b'3': -1},
               {b'1': -1, b'2': 1, b'3': -2, b'4': -1, b'5': 0, b'6': -1, b'7': 2, b'8': 1},
               {b'1': 1, b'2': 0, b'3': 2, b'4': -1},
               {b'1': 0, b'2': 0, b'3': 0}
               ]

IS_OLD_MSG_POLL_MAP = {}


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
