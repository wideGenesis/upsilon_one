# -*- coding: utf-8 -*-
import asyncio
import requests
from time import sleep
import json

from telethon import events, TelegramClient, types, functions
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, InputPeerUser
from aiohttp import web
import sqlalchemy
from project_shared import *
from spam_sender.sql_queries import *

my_sqlalchemy_engine = sqlalchemy.create_engine(
    'mysql+pymysql://gb_telethon2:J-KnpTx-Qz6V@mysql102.1gb.ru/gb_telethon2')
# my_sqlalchemy_engine = sqlalchemy.create_engine('mysql+pymysql://gb_telethon1:7edz7a66567@mysql100.1gb.ru/gb_telethon1')
container = AlchemySessionContainer(engine=my_sqlalchemy_engine)
session = container.new_session('spm_session')

PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# Use your own values from my.telegram.org
api_id = 3730224
api_hash = 'ee430fe3f8307871277d27059b09f3e7'
command_token = '9e098ea3706511eb94d2d8c497581578'

WEB_LISTEN_HOST = "0.0.0.0"
WEB_LISTEN_PORT = 8441
app = web.Application()

client = TelegramClient(session, api_id, api_hash).start()

user_table_name = "new_users"


async def handle(request):
    if request.match_info.get("token") == command_token:
        res_ack = {'result': 'ACK'}
        res_nack = {'result': 'NACK'}
        debug(f'Received cmd token!')
        request_json = await request.json()
        debug(f'request_json:{request_json}')
        action = str(request_json['action'])
        new_user_id = int(request_json['user_id'])
        new_username = str(request_json['username'])
        if action == "new_user":
            debug(f'Action = new_user')
            try:
                if new_user_id is not None:
                    debug(f'Add new user')
                    # _______Создаем таблицу новых юзеров, если ее нет
                    if not is_table_exist(table_name=user_table_name, engine=my_sqlalchemy_engine):
                        create_newusers_table(table_name=user_table_name, engine=my_sqlalchemy_engine)
                    # _______Добавляем пользователя если его еще нет
                    if not user_lookup(new_user_id, engine=my_sqlalchemy_engine):
                        dt = datetime.datetime.now()
                        append_dt = dt.timestamp()
                        insert_new_user(new_user_id, new_username, append_dt, engine=my_sqlalchemy_engine)
                    # _______Выберем всех пользователей которым можно разослать сообщения
                    new_users = select_users(engine=my_sqlalchemy_engine)
                    # _______Идем по юзерам и если он добавился в чат более 12 часов назад - шлем ему мессагу
                    for k, v in new_users.items():
                        dt = datetime.datetime.now()
                        now_dt = dt.timestamp()
                        username, append_dt = v
                        delta_t = int(now_dt) - int(append_dt)
                        debug(f'User[{k}] username[{username}] now_dt[{now_dt}] v[{append_dt}] delta_t[{delta_t}]')
                        if delta_t > 25: #43200:
                            await client.get_dialogs()
                            entity = await client.get_entity(username)
                            res = await send_to_message(entity)
                            if res:
                                set_wstatus(k, now_dt, engine=my_sqlalchemy_engine)
                else:
                    return web.json_response(res_nack)
            except Exception as e:
                debug(e, ERROR)
                return web.json_response(res_nack)
            return web.json_response(res_ack)


app.router.add_post("/{token}/", handle)

msg = "Простите я случайно, не тому пользователю написал"
# msg = "Привет Макс, я наш новый бот спаммер. Буду вот так вот всех заспамливать! " \
#       "\n Не сообщай о спаме про меня, пожалуйста!" \
#       "\n Я успешно заработал, с теми пользователями у которых есть username." \
#       "\n Нужно написать тексты! " \
#       "\n Настроить временной интервал, чтобы не сразу писать пользователю как только он пришел в чат! " \
#       "\n Клонировать меня для рассылки негатива." \
#       "\n Запустить в продашкн :-)"


async def send_to_message(toid):
    try:
        await client.send_message(toid, msg)
        return True
    except Exception as e:
        debug(e, ERROR)
        return False


async def webserver_starter():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEB_LISTEN_HOST, WEB_LISTEN_PORT)
    await site.start()
    debug("Web Server was started!")


def main():
    debug("__Try start web server__")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(webserver_starter())
    debug("__Try start telethon client__")
    client.run_until_disconnected()


if __name__ == '__main__':
    debug("***Start***")
    main()