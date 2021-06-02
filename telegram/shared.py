import asyncio
import datetime
import json
import sys
import requests
from time import sleep
from typing import Any
from telethon import utils
from project_shared import *
from telethon import functions, types
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from telegram import sql_queries as sql_q


class Worker(QObject):
    minute_signal = pyqtSignal()
    client = None

    def set_client(self, client):
        self.client = client

    def run(self):
        start_thread_time = datetime.datetime.now()
        debug(f'start_thread_time={start_thread_time}')
        i = 0
        while True:
            sleep(1)
            i += 1
            if i % 60 == 0:
                inspector_scheduler()
            if i % 600 == 0:
                print_shared_maps()


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
IN_INSPECTOR_FLOW_MAP = {}
INSPECTOR_FLOW_START_TIME = {}


# Оставляю как пример как шедулером засылать команды боту
# def schedule_send_command(cmd, recursion_count=0):
#     debug(f"schedule_send_command: cmd={cmd} recursion_count={recursion_count}")
#     if recursion_count == RECURSION_DEPTH:
#         debug(f"Can't schedule_send_command!!!", ERROR)
#         return -1
#     with requests.Session() as session:
#         url = f"http://127.0.0.1:8445/{COMMAND_TOKEN}/"
#         data = {'action': cmd, 'value': ''}
#         headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#         try:
#             request_result = session.post(url, data=json.dumps(data), headers=headers)
#         except Exception as e:
#             debug(f'Exception: {e}', WARNING)
#             sleep(0.9)
#             errCode = schedule_send_command(cmd=cmd, recursion_count=recursion_count + 1)
#             return errCode
#         if request_result.status_code == requests.codes.ok:
#             parsed_json = json.loads(request_result.text)
#             debug(parsed_json)
#             return 0


def print_shared_maps():
    global INSPECTOR_FLOW_START_TIME
    global INSPECTOR_TICKER_MAP
    global INSPECTOR_PORTFOLIO_MAP
    global OLD_MESSAGE_MAP
    global IS_OLD_MSG_POLL_MAP
    debug(f"OLD_MESSAGE_MAP = {OLD_MESSAGE_MAP}")
    debug(f"IS_OLD_MSG_POLL_MAP = {IS_OLD_MSG_POLL_MAP}")
    debug(f"INSPECTOR_FLOW_START_TIME = {INSPECTOR_FLOW_START_TIME}")
    debug(f"INSPECTOR_TICKER_MAP = {INSPECTOR_TICKER_MAP}")
    debug(f"INSPECTOR_PORTFOLIO_MAP = {INSPECTOR_PORTFOLIO_MAP}")


def inspector_scheduler():
    global INSPECTOR_FLOW_START_TIME
    global INSPECTOR_TICKER_MAP
    global INSPECTOR_PORTFOLIO_MAP
    now = datetime.datetime.now()
    need_clear = []
    for k in INSPECTOR_FLOW_START_TIME:
        td = (now - INSPECTOR_FLOW_START_TIME[k]).seconds
        if td >= 1800:
            if k in INSPECTOR_PORTFOLIO_MAP:
                INSPECTOR_PORTFOLIO_MAP.pop(k)
            if k in INSPECTOR_TICKER_MAP:
                INSPECTOR_TICKER_MAP.pop(k)
            need_clear.append(k)
    for user in need_clear:
        INSPECTOR_FLOW_START_TIME.pop(user)


def get_inspector_time(user_id):
    global INSPECTOR_FLOW_START_TIME
    return INSPECTOR_FLOW_START_TIME.get(user_id, None)


def set_inspector_time(user_id):
    global INSPECTOR_FLOW_START_TIME
    INSPECTOR_FLOW_START_TIME[user_id] = datetime.datetime.now()


def del_inspector_time(user_id):
    global INSPECTOR_FLOW_START_TIME
    if user_id in INSPECTOR_FLOW_START_TIME:
        INSPECTOR_FLOW_START_TIME.pop(user_id)


def datetime2int(dt):
    return int(dt.strftime("%Y%m%d%H%M%S"))


def int2datetime(dt_int):
    return datetime.datetime.strptime(str(dt_int), "%Y%m%d%H%M%S")


async def save_old_message(user_id, msg):
    msg_id = utils.get_message_id(msg)
    global OLD_MESSAGE_MAP
    OLD_MESSAGE_MAP[user_id] = msg_id


async def delete_old_message(client, user_id):
    global OLD_MESSAGE_MAP
    is_message_deleted = False
    old_msg_id = OLD_MESSAGE_MAP.get(user_id, None)
    if old_msg_id is not None:
        OLD_MESSAGE_MAP.pop(user_id)
        try:
            await client.delete_messages(user_id, old_msg_id)
            is_message_deleted = True
        except Exception as e:
            debug(e, ERROR)
            return is_message_deleted
        return is_message_deleted


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


def set_inspector_ticker(user_id, ticker, size):
    global INSPECTOR_TICKER_MAP
    INSPECTOR_TICKER_MAP[user_id] = (ticker, size)


def get_inspector_ticker(user_id):
    global INSPECTOR_TICKER_MAP
    return INSPECTOR_TICKER_MAP.get(user_id, None)


def update_inspector_portfolio(user_id, ticker, size) -> bool:
    global INSPECTOR_PORTFOLIO_MAP
    if user_id in INSPECTOR_PORTFOLIO_MAP:
        INSPECTOR_PORTFOLIO_MAP[user_id][ticker] = size
        return False
    else:
        portfolio = {ticker: size}
        INSPECTOR_PORTFOLIO_MAP[user_id] = portfolio
        return True


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


def get_is_inspector_flow(user_id):
    global IN_INSPECTOR_FLOW_MAP
    return IN_INSPECTOR_FLOW_MAP.get(user_id, False)


def set_is_inspector_flow(user_id, value):
    global IN_INSPECTOR_FLOW_MAP
    IN_INSPECTOR_FLOW_MAP[user_id] = value


def del_is_inspector_flow(user_id):
    global IN_INSPECTOR_FLOW_MAP
    if user_id in IN_INSPECTOR_FLOW_MAP:
        IN_INSPECTOR_FLOW_MAP.pop(user_id)
