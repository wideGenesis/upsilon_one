# -*- coding: utf-8 -*-
import asyncio
import requests
from time import sleep
import json

from telethon import events, TelegramClient, types, functions
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from aiohttp import web
import sqlalchemy
from project_shared import *

# my_sqlalchemy_engine = sqlalchemy.create_engine('mysql+pymysql://gb_telethon1:7edz7a66567@mysql100.1gb.ru/gb_telethon1')
my_sqlalchemy_engine = sqlalchemy.create_engine('mysql+pymysql://gkeeper:Sa30qNiczNUYE9vv@localhost/gkeeper')
container = AlchemySessionContainer(engine=my_sqlalchemy_engine)
session = container.new_session('gkeeper_session')

PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# Use your own values from my.telegram.org
api_id = 3290429
api_hash = '27a5c1544b7b363ae304fae996d05830'
command_token = '32a28c178a861575753c4733f62567cd'
spammer_token = '9e098ea3706511eb94d2d8c497581578'


WEB_LISTEN_HOST = "0.0.0.0"
WEB_LISTEN_PORT = 8443
app = web.Application()

client = TelegramClient(session, api_id, api_hash).start()


# process only requests with correct bot token
async def handle(request):
    if request.match_info.get("token") == command_token:
        res_ack = {'result': 'ACK'}
        res_nack = {'result': 'NACK'}
        debug(f'Received cmd token!')
        request_json = await request.json()
        debug(f'request_json:{request_json}')
        action = str(request_json['action'])
        value = str(request_json['value'])
        if action == "join_to":
            debug(f'Action = join_to')
            channel = request_json.get("id", None)
            try:
                if value == 'simple_chat':
                    res = await client(JoinChannelRequest(channel))
                    debug(f'res={res.stringify()}')
                elif value == 'private_chat':
                    res = await client(ImportChatInviteRequest(channel))
                    debug(f'res={res.stringify()}')
            except Exception as e:
                debug(e, ERROR)
                return web.json_response(res_nack)
            return web.json_response(res_ack)
        if action == "leave_channel":
            debug(f'Action = leave_channel')
            channel = request_json.get("value", None)
            try:
                await client(LeaveChannelRequest(channel))
            except Exception as e:
                debug(e, ERROR)
                return web.json_response(res_nack)
            return web.json_response(res_ack)


app.router.add_post("/{token}/", handle)


@client.on(events.ChatAction())
async def handler(event):
    # Welcome every new user
    if event.user_joined:
        debug("Join user event received")
        await client.get_dialogs()
        user_id = event.user_id
        username = event.user.username
        if user_id is not None and username is not None:
            host = '127.0.0.1'
            port = 8448
            debug(f"Joined user id: {user_id}")
            debug("Try send joined command")
            with requests.Session() as session:
                url = f'http://{host}:{port}/{spammer_token}/'
                data = {'action': "new_user", 'user_id': user_id, 'username': username}
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                try:
                    request_result = session.post(url, data=json.dumps(data), headers=headers)
                except Exception as e:
                    debug(e, ERROR)
                    entity = await client.get_entity('defoer')
                    await client.send_message(entity, str(e))
                    count = 2
                    while request_result.status_code != requests.codes.ok:
                        debug(f"Error. Try one more: {count}")
                        sleep(10)
                        request_result = session.post(url, data=json.dumps(data), headers=headers)
                        count += 1
                        if count == 100:
                            break
                if request_result.status_code == requests.codes.ok:
                    parsed_json = json.loads(request_result.text)
                    is_ack = parsed_json.get("result", None)
                    if is_ack == "NACK" or is_ack is None:
                        dt = datetime.datetime.now()
                        entity = await client.get_entity('defoer')
                        await client.send_message(entity, f'[{dt.strftime("%H:%M:%S")}]: Spammer bot NACK answer!')
                    debug(parsed_json)


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
    debug("__Try start tlethon client__")
    client.run_until_disconnected()


if __name__ == '__main__':
    if not IS_RUN_LOCAL:
        debug_init(file_name="gatekeeper.log")
    debug("*************** S T A R T ***************")
    main()
