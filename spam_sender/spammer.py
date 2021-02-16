# -*- coding: utf-8 -*-
import asyncio
import requests
from time import sleep
import json

from telethon import events, TelegramClient, types, functions
from aiohttp import web
import sqlalchemy
from project_shared import *
from sql_queries import *

my_sqlalchemy_engine = sqlalchemy.create_engine(
    'mysql+pymysql://gb_telethon2:J-KnpTx-Qz6V@mysql102.1gb.ru/gb_telethon2')
container = AlchemySessionContainer(engine=my_sqlalchemy_engine)
session = container.new_session('spm_session')

PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# Use your own values from my.telegram.org
api_id = 3290429
api_hash = '27a5c1544b7b363ae304fae996d05830'
command_token = '9e098ea3706511eb94d2d8c497581578'

WEB_LISTEN_HOST = "0.0.0.0"
WEB_LISTEN_PORT = 8441
app = web.Application()

client = TelegramClient(session, api_id, api_hash).start()

user_table_name = "new_user"


async def handle(request):
    if request.match_info.get("token") == command_token:
        res_ack = {'result': 'ACK'}
        res_nack = {'result': 'NACK'}
        debug(f'Received cmd token!')
        request_json = await request.json()
        debug(f'request_json:{request_json}')
        action = str(request_json['action'])
        value = str(request_json['value'])
        if action == "new_user":
            debug(f'Action = new_user')
            new_user_id = request_json.get("value", None)
            try:
                if value is not None:
                    debug(f'Add new user')
                    # _______Создаем таблицу новых юзеров, если ее нет
                    if not is_table_exist(table_name=user_table_name, engine=my_sqlalchemy_engine):
                        create_newusers_table(table_name=user_table_name, engine=my_sqlalchemy_engine)
                    # _______Добавляем пользователя если его еще нет
                    if not user_lookup(new_user_id, engine=my_sqlalchemy_engine):
                        append_dt = timedelta.total_seconds()
                        insert_new_user(new_user_id, append_dt, engine=my_sqlalchemy_engine)
                    # _______Выберем всех пользователей которым можно разослать сообщения
                    new_users = select_users(engine=my_sqlalchemy_engine)
                    # _______Идем по юзерам и если он добавился в чат более 12 часов назад - шлем ему мессагу
                    for k, v in new_users.items():
                        now_dt = timedelta.total_seconds()
                        if (now_dt - v) > 43200:
                            res = await send_to_message(k)
                            if res:
                                set_wstatus(k, now_dt, engine=my_sqlalchemy_engine)
                else:
                    return web.json_response(res_nack)
            except Exception as e:
                debug(e, ERROR)
                return web.json_response(res_nack)
            return web.json_response(res_ack)


app.router.add_post("/{token}/", handle)

msg = "Тестовое сообщение бота спамера"


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
