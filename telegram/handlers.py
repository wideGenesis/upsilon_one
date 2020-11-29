import base64
import rsa
import random
from aiohttp import web
from upsilon_bot import PAYMENT_TOKEN, PUBKEY, ORDER_MAP, client, engine
from telegram import sql_queries as sql
from telegram import ai


# ============================== Payment request handler ======================
# process only requests with correct payment token
async def success_payment_handler(request):
    if request.match_info.get("token") == PAYMENT_TOKEN:
        request_json = await request.json()
        # print("JSON:" + str(request_json))
        order_id = str(request_json['order_id'])
        summa = str(request_json['summa'])
        data = ":" + order_id + ":" + summa + ":"
        sign = base64.b64decode(str(request_json['sign']))

        if PUBKEY is None:
            return web.Response(status=403)

        try:
            rsa.verify(data.encode(), sign, PUBKEY)
        except:
            print("Verification failed")
            return web.Response(status=403)

        value = ORDER_MAP.get(order_id)
        if value is not None:
            print("Send message \"payment is ok\"")
            sender_id, message_id = value
            await client.delete_messages(sender_id, message_id)
            tariff_str = ""
            if summa == "15":
                tariff_str = '__Тариф: Старт__\n'
            elif summa == "25":
                tariff_str = '__Тариф: Базовый__\n'
            await client.send_message(sender_id,
                                      'Оплата прошла успешно:\n'
                                      + tariff_str
                                      + '__Ордер: ' + order_id + '__\n'
                                      + '__Сумма: ' + summa + '__\n'
                                      + '**Спасибо, что пользуетесь моими услугами!**')
            ORDER_MAP.pop(order_id)
            await sql.delete_from_payment_message(order_id, engine)
            return web.Response(status=200)
        else:
            print("Global SenderID is None")
            return web.Response(status=403)

    else:
        return web.Response(status=403)


def set_route(app):
    app.router.add_post("/{token}/", success_payment_handler)


# ============================== Commands ===============================

async def send_to_handler(event, client_, owner=None):
    parse = str(event.text).split('|')
    try:
        sender_id = event.input_sender
    except ValueError as e:
        sender_id = await event.get_input_sender()
    try:
        if int(sender_id.user_id) == int(owner):
            entity = await client_.get_entity(int(parse[1]))
            await client_.send_message(entity, parse[2])
        else:
            await client_.send_message(sender_id, 'Order dismissed!')
    except ValueError as e:
        print(e, 'Some errors from send_to()')


async def publish_to_handler(event, client_, owner=None):
    parse = str(event.text).split('|')
    try:
        channel = await client_.get_entity('https://t.me/' + str(parse[1]))
    except ValueError as e:
        print(e, 'Can\'t get channel entity')
    try:
        if int(event.input_sender.user_id) == int(owner):
            await client_.send_message(channel, parse[2])
        else:
            await client_.send_message(event.input_sender, 'Order dismissed!')
    except ValueError as e:
        print(e, 'Some errors from publish_to()')


async def dialog_flow_handler(event, client_):
    no_match = ['\U0001F9D0', '\U0001F633', 'Ясно', 'Мы должны подумать над этим']
    fallback = random.choice(no_match)
    try:
        sender_id = event.input_sender
    except ValueError as e:
        sender_id = await event.get_input_sender()
    if not any(value in event.text for value in
               ('/start', '/help', '/publish_to', '/to', 'Главное меню', 'Профиль', 'Помощь', 'Donate')):
        user_message = event.text
        project_id = 'common-bot-1'
        try:
            dialogflow_answer = ai.detect_intent_texts(project_id, sender_id.user_id, user_message, 'ru-RU')
            await client_.send_message(sender_id, dialogflow_answer)
            await client_.send_message(-1001262211476, str(sender_id.user_id) +
                                       '  \n' + str(event.text) +
                                       '  \n' + dialogflow_answer)
            # TODO Внимание! изменить айди чата при деплое
        except ValueError as e:
            print(e, 'Dialogflow response failure')
            await client_.send_message(sender_id, fallback)

# @client.on(events.ChatAction)
# async def get_participants_from_chat(event):
#     if event.user_joined or event.user_added:
#         # print(event.action_message.to_id, '1XXXXXXXXXX')
#         # print(event.action_message.to_id.chat_id, '3XXXXXXXXXX')
#         # entity = await client.get_entity(event.action_message.to_id)
#         # chat = await event.get_input_chat()
#         # print(chat, '1dgggdg')
#         try:
#             participants = await client.get_participants(event.action_message.to_id)
#         except AttributeError as e:
#             logging.exception(e,
#                               'NoneType object has no attribute to_id ' + '\n' + 'Probably bot was added to some chat')
#         for user in participants:
#             if user.id is not None:
#                 entity = await client.get_entity(PeerUser(user.id))
#                 print('Dump complete!')
#                 # print(user.access_hash, user.id, user.username, user.first_name, user.last_name, entity)
#                 # TODO Добавить в модели поля bot=True, scam=False
