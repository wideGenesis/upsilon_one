import datetime
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


async def check_request_amount(user_id, client) -> bool:
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
                return True
            else:
                await client.send_message(user_id, f'Чувак!\n '
                                                   f'Новым пользователям можноделать запросы нечаще чем раз в 5 мин\n'
                                                   f'Осталось {300-td}сек')
                return False
        else:
            if free_amount > 0:
                await sql.decrement_free_request_amount(user_id, 1)
                return True
            if paid_amount > 0:
                await sql.decrement_paid_request_amount(user_id, 1)
                return True
            else:
                await client.send_message(user_id, f'Чувак!\n '
                                                   f'Для дальнейшего получения платных данных, '
                                                   f'тебе необходимо пополнить баланс!!')
                return False
    else:
        if free_amount > 0:
            await sql.decrement_free_request_amount(user_id, 1)
            return True
        if paid_amount > 0:
            await sql.decrement_paid_request_amount(user_id, 1)
            return True
        else:
            await client.send_message(user_id, f'Чувак!\n '
                                               f'Для дальнейшего получения платных данных, '
                                               f'тебе необходимо пополнить баланс!!')
            return False

