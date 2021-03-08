# -*- coding: utf-8 -*-
import asyncio
import requests
from time import sleep
import json

from telethon import events, TelegramClient, types, functions
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, InputPeerUser, DocumentAttributeVideo
from aiohttp import web
import sqlalchemy
from project_shared import *
from spam_sender.sql_queries import *
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import schedule
import threading


my_sqlalchemy_engine = sqlalchemy.create_engine('mysql+pymysql://spammer:m4sQvpkrva7CnfcI@localhost/spammer')
# my_sqlalchemy_engine = sqlalchemy.create_engine('mysql+pymysql://gb_telethon1:7edz7a66567@mysql100.1gb.ru/gb_telethon1')
container = AlchemySessionContainer(engine=my_sqlalchemy_engine)
session = container.new_session('spm_session')

PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# Use your own values from my.telegram.org
# api_id = 3730224   # Nik Kin
# api_hash = 'ee430fe3f8307871277d27059b09f3e7' # Nik Kin

api_id = 2534378  # Elena Fomichova
api_hash = 'a27d1afab5bd054770968466f8f87018'  # Elena Fomichova

command_token = '9e098ea3706511eb94d2d8c497581578'

WEB_LISTEN_HOST = "0.0.0.0"
# WEB_LISTEN_PORT = 8446  # Nik Kin
WEB_LISTEN_PORT = 8447  # Elena Fomichova
app = web.Application()

client = TelegramClient(session, api_id, api_hash).start()

user_table_name = "new_users"
spammer_token = '9e098ea3706511eb94d2d8c497581578'

scount = 0


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
                else:
                    return web.json_response(res_nack)
            except Exception as e:
                debug(e, ERROR)
                return web.json_response(res_nack)
            return web.json_response(res_ack)
        if action == "check_user":
            res = await schedule_send(7200) # спустя 2 часа будет отпавлять мессаги
            if res:
                return web.json_response(res_ack)
            else:
                return web.json_response(res_nack)



app.router.add_post("/{token}/", handle)

msg = "Здравствуйте! " \
      "Прошу прощения, что сразу не выслали @UpsilonBot " \
      "Это наш бесплатный бот для всех новых пользователей.  " \
      "\n" \
      "@UpsilonBot - это сканер акций и менеджер портфелей. Мастхев для каждого инвестора! " \
      "Прежде, чем задавать вопросы в чате, изучите бота! Он умеет отвечать на основные вопросы, " \
      "делать анализ по акциям и собирать инвест портфели."


# Printing upload progress
async def progresscallback(current, total):
    prgs = f'Uploaded {current} out of {total} bytes: {round((current / total)*100, 2)}%'
    debug(prgs)


async def send_to_message(toid):
    debug(f' ----- Try send messages -----')
    try:
        filepath = PROJECT_HOME_DIR + '/spam_sender/for_send/'
        filename1 = filepath + 'start.mp4'
        filename2 = filepath + 'amzn.mp4'
        filename3 = filepath + 'allweather.mp4'

        metadata1 = None
        metadata2 = None
        metadata3 = None
        try:
            metadata1 = extractMetadata(createParser(filename1))
            metadata2 = extractMetadata(createParser(filename2))
            metadata3 = extractMetadata(createParser(filename3))
        except Exception as e:
            debug(f"Metadata extraction error: {e}", ERROR)

        debug(f'%%%% {filename1} %%%%')
        for line in metadata1.exportPlaintext():
            debug(line)

        debug(f'%%%% {filename2} %%%%')
        for line in metadata2.exportPlaintext():
            debug(line)

        debug(f'%%%% {filename3} %%%%')
        for line in metadata3.exportPlaintext():
            debug(line)

        await client.send_message(toid, msg)

        await client.send_file(toid, "http://www.watchlister.ru/start.mp4", video_note=True,
                               attributes=(DocumentAttributeVideo(
                                      (0, metadata1.get('duration').seconds)[metadata1.has('duration')],
                                      (0, metadata1.get('width'))[metadata1.has('width')],
                                      (0, metadata1.get('height'))[metadata1.has('height')]
                                  ),))
        await client.send_file(toid, "http://www.watchlister.ru/amzn.mp4", video_note=True,
                               attributes=(DocumentAttributeVideo(
                                      (0, metadata2.get('duration').seconds)[metadata2.has('duration')],
                                      (0, metadata2.get('width'))[metadata2.has('width')],
                                      (0, metadata2.get('height'))[metadata2.has('height')]
                                  ),))
        await client.send_file(toid, "http://www.watchlister.ru/allweather.mp4", video_note=True,
                               attributes=(DocumentAttributeVideo(
                                      (0, metadata3.get('duration').seconds)[metadata3.has('duration')],
                                      (0, metadata3.get('width'))[metadata3.has('width')],
                                      (0, metadata3.get('height'))[metadata3.has('height')]
                                  ),))
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


async def schedule_send(send_interval):
    debug("Check users")
    # _______Выберем всех пользователей которым можно разослать сообщения
    new_users = select_users(engine=my_sqlalchemy_engine)
    if len(new_users) == 0:
        return True
    # _______Идем по юзерам и если он добавился в чат более 12 часов назад - шлем ему мессагу
    for k, v in new_users.items():
        dt = datetime.datetime.now()
        now_dt = dt.timestamp()
        username, append_dt = v
        delta_t = int(now_dt) - int(append_dt)
        debug(f'User[{k}] username[{username}] now_dt[{now_dt}] v[{append_dt}] delta_t[{delta_t}]')
        if delta_t > send_interval:
            sleep(120)
            debug(f"delta_t > send_interval [{delta_t} > {send_interval}] -- "
                  f"Try send messages for username[{username}]")
            await client.get_dialogs()
            entity = await client.get_entity(username)
            res = await send_to_message(entity)
            if res:
                global scount
                scount += 1
                set_wstatus(k, now_dt, engine=my_sqlalchemy_engine)
                debug(f">>>>>>>>>>>> s c o u n t = {scount} <<<<<<<<<<<<<<<<<<<<")
            else:
                return False
    return True


def send_check_signal():
    # pass
    now = datetime.datetime.now()
    if 5 <= now.hour <= 18:
        debug(f"NOW: {str(now)} -- It's time to send ;-)")
        with requests.Session() as sess:
            url = f'http://{WEB_LISTEN_HOST}:{WEB_LISTEN_PORT}/{spammer_token}/'
            data = {'action': "check_user", 'user_id': '1', 'username': ''}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            request_result = None
            try:
                request_result = sess.post(url, data=json.dumps(data), headers=headers)
            except Exception as e:
                debug(e, ERROR)
            if request_result.status_code == requests.codes.ok:
                parsed_json = json.loads(request_result.text)
                debug(parsed_json)
    else:
        debug(f"NOT NOW {str(now)} -- No time to send ;-(")


def run_my_scheduler():
    debug("&&&&&&&  Run scheduler &&&&&&&")
    schedule.every(1).minutes.do(lambda: send_check_signal())  # 28800
    while True:
        schedule.run_pending()
        sleep(20)


def main():
    debug("__Try start web server__")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(webserver_starter())
    debug("__Try start scheduler__")
    threading.Thread(target=run_my_scheduler).start()
    debug("__Try start telethon client__")
    client.run_until_disconnected()


if __name__ == '__main__':
    if not IS_RUN_LOCAL:
        debug_init(file_name="spam_sender.log")
    debug("*************** S T A R T ***************")
    main()
