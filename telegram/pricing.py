import datetime
from typing import Tuple, Dict, Union

from telegram import sql_queries as sql
from telegram import shared
from project_shared import *


async def calc_save_balance(user_id, summ):
    # Расчитываем на сколько запросов пополнить баланс
    debug(f'user_id:{user_id} summ:{summ}')
    price = 0.15
    if 0.0 < summ <= 20.0:
        price = 0.15
    elif 20.0 < summ <= 50.0:
        price = 0.14
    elif 50.0 < summ <= 100.0:
        price = 0.12
    elif 100.0 < summ <= 150.0:
        price = 0.1
    elif 150.0 < summ <= 200.0:
        price = 0.08
    elif 200.0 < summ <= 300.0:
        price = 0.06
    elif summ > 300.0:
        price = 0.04

    paid_amount = round(summ/price)
    await sql.increment_paid_request_amount(user_id, paid_amount)


async def check_request_amount(user_id, client, decrement_amount=1) -> Dict[str, Union[bool, int]]:
    result = {"result": True, 'Free': 0, 'Paid': 0}
    if str(user_id) in OWNERS:
        debug(f'Welcome owner ;-)')
        return result
    paid_amount, free_amount = await sql.get_request_amount(user_id)
    income_datetime = await sql.get_income_datetime(user_id)
    now = datetime.datetime.now()
    is_new_user = True if (now - income_datetime).days < 3 else False
    if is_new_user:
        if paid_amount == 0:
            last_request_datetime = await sql.get_last_request_datetime(user_id)
            td = (now - last_request_datetime).seconds if last_request_datetime is not None else 500
            if td > 300:
                await sql.set_last_request_datetime(user_id)
                result = {"result": True, 'Free': 0, 'Paid': 0}
                return result
            else:
                debug("New user: Timeout 5 min!!")
                await client.send_message(user_id, f'😔\n '
                                                   f'Сожалею, но новым пользователям можно делать запросы нечаще '
                                                   f'чем раз в 5 мин\n'
                                                   f'Осталось {300-td}сек')
                result = {"result": False, 'Free': 0, 'Paid': 0}
                return result
        else:
            if (free_amount + paid_amount) < decrement_amount:
                debug("User: Not enough balance!!")
                await client.send_message(user_id, f'😔\n '
                                                   f'Сожалею, но для дальнейшего получения платных данных, '
                                                   f'тебе необходимо пополнить баланс!!')
                result = {"result": False, 'Free': 0, 'Paid': 0}
                return result
            if free_amount > 0:
                if free_amount >= decrement_amount:
                    await sql.decrement_free_request_amount(user_id, decrement_amount)
                    result = {"result": True, 'Free': decrement_amount, 'Paid': 0}
                    return result
                else:
                    await sql.decrement_free_request_amount(user_id, free_amount)
                    result['Free'] = free_amount
                    decrement_amount -= free_amount

            if paid_amount > 0:
                await sql.decrement_paid_request_amount(user_id, decrement_amount)
                result['result'] = True
                result['Paid'] = decrement_amount
                return result
    else:
        if (free_amount + paid_amount) < decrement_amount:
            debug("User: Not enough balance!!")
            await client.send_message(user_id, f'😔\n '
                                               f'Сожалею, но для дальнейшего получения платных данных, '
                                               f'тебе необходимо пополнить баланс!!')
            result = {"result": False, 'Free': 0, 'Paid': 0}
            return result
        if free_amount > 0:
            if free_amount >= decrement_amount:
                await sql.decrement_free_request_amount(user_id, decrement_amount)
                result = {"result": True, 'Free': decrement_amount, 'Paid': 0}
                return result
            else:
                await sql.decrement_free_request_amount(user_id, free_amount)
                result['Free'] = free_amount
                decrement_amount -= free_amount

        if paid_amount > 0:
            await sql.decrement_paid_request_amount(user_id, decrement_amount)
            result['result'] = True
            result['Paid'] = decrement_amount
            return result

