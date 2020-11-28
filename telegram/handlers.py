import base64
import rsa
from aiohttp import web
from upsilon_bot import PAYMENT_TOKEN, PUBKEY, ORDER_MAP, client, engine
from telegram import sql_queries as sql


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
