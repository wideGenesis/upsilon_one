import importlib
import sys
from time import sleep
import csv
from datetime import datetime
from telegram import sql_queries as sql
from telethon.tl.custom import Button
from telegram import buttons, buttons
from quotes.parsers import users_count
from project_shared import *
from telegram import shared
from telegram import instructions as ins
from messages.message import *
from telegram import callbacks

pics = f'{PROJECT_HOME_DIR}/html/'


async def start_menu(event, client, engine=None):
    referral = str(event.original_update.message.message).split(' ')
    user_profile = await sql.user_search(event.original_update.message.peer_id.user_id, engine)
    debug("User_profile:" + str(user_profile))
    if len(referral) > 1:
        user_profile = await sql.user_search(referral[1], engine)
        inc = user_profile[13] + 1
        await sql.db_save_referral(inc, referral[1], engine)
    sender_id = event.original_update.message.peer_id.user_id
    entity = await client.get_input_entity(sender_id)
    old_msg_id = await shared.get_old_msg_id(sender_id)
    if old_msg_id is not None:
        shared.pop_old_msg_id(sender_id)

    # Если клиент не до конца прошел профалинг - сбрасываем результат прохождения,
    # сразу стартовать с профайла
    if not is_user_profile_done(sender_id):
        # а вообще дошел ли юзер до профайла, если доходил, то не надо показывать презу
        if not user_profiler_map_lookup(sender_id):
            reset_user_profiler_data(sender_id)
            await client.send_message(entity, ins.hello_1, file=f'{PROJECT_HOME_DIR}/html/hello_1.jpg',
                                      buttons=buttons.keyboard_forw2)
        else:
            #  Если не дошел до профайла даже, то презу показать надо
            await client.send_message(event.input_sender, '👤 Профиль')
            await callbacks.send_next_profiler_question(client, sender_id, 0)
    else:
        # Если юзер уже прошел профайлинг, то ему не надо показывать презу и опрос - сразу главное меню
        await tools_menu(event, client)
    # Сохраним данные о новом пользователе (функция сохранит и распечатает, только если пользователь ранее не числился)
    await sql.append_new_user(sender_id)


async def meta_menu(event, client):
    sender_id = event.original_update.message.sender_id
    old_msg_id = await shared.get_old_msg_id(sender_id)
    if old_msg_id is not None:
        shared.pop_old_msg_id(sender_id)
    await client.send_message(event.input_sender, '.', buttons=buttons.keyboard_start)


async def tools_menu(event, client):
    sender_id = event.original_update.message.sender_id
    await client.delete_messages(sender_id, event.message.id)

    # Если клиент не до конца прошел профалинг - сбрасываем результат прохождения
    if not is_user_profile_done(sender_id):
        reset_user_profiler_data(sender_id)

    old_msg_id = await shared.get_old_msg_id(sender_id)
    if old_msg_id is not None:
        is_poll = await shared.is_old_msg_poll(sender_id)
        if is_poll:
            await shared.delete_old_message(client, sender_id)
            menu_msg = await client.send_message(event.input_sender, '📁 Главное меню', buttons=buttons.keyboard_0)
            await shared.save_old_message(sender_id, menu_msg)
            shared.set_old_msg_poll(sender_id, False)
        else:
            menu_msg = await client.edit_message(event.input_sender, old_msg_id, '📁 Главное меню',
                                                 buttons=buttons.keyboard_0)
    else:
        menu_msg = await client.send_message(event.input_sender, '📁 Главное меню', buttons=buttons.keyboard_0)
        await shared.save_old_message(sender_id, menu_msg)


async def profile_menu(event, client, engine=None):
    keyboard_profile = [
        [Button.inline('💎	  ' + 'Купить запросы', b'requests_store')],
        [Button.inline('\U0001F91D	  ' + 'Пригласить друга', b'invite_friends')],
        [Button.inline('\U0000267B	  ' + 'Сбросить профиль риска', b'risk_reset')],
        [Button.inline('\U0001F519    ' + 'В главное меню', b'main')]
    ]

    sender_id = event.input_sender
    m_id = getattr(event, "message", None)
    if m_id is not None:
        await client.delete_messages(sender_id.user_id, event.message.id)

    # Если клиент не до конца прошел профалинг - сбрасываем результат прохождения
    if not is_user_profile_done(sender_id.user_id):
        reset_user_profiler_data(sender_id.user_id)

    await client.get_input_entity(sender_id)
    user_profile = await sql.user_search(sender_id.user_id, engine)
    count = int
    filename = f'{PROJECT_HOME_DIR}/{RESULTS_PATH}users.csv'
    with open(filename, newline='') as f:
        data = csv.reader(f, delimiter=',')
        for row in data:
            count = str(row).strip("['']")
    profile_score_str = ""
    final_profile_score = get_final_score(sender_id.user_id)
    if isinstance(final_profile_score, int):
        if final_profile_score <= -9:
            profile_score_str = "Полное отвержение риска"
        elif -9 < final_profile_score <= -4:
            profile_score_str = "Сильное отвержение риска"
        elif -4 < final_profile_score <= 1:
            profile_score_str = "Умеренное принятие риска"
        elif 1 < final_profile_score < 6:
            profile_score_str = "Разумное принятие риска"
        elif 6 <= final_profile_score < 10:
            profile_score_str = "Уверенное принятие риска"
        elif final_profile_score >= 10:
            profile_score_str = "Полное принятие риска"
    else:
        profile_score_str = final_profile_score

    paid_amount, _ = await sql.get_request_amount(sender_id.user_id)

    old_msg_id = await shared.get_old_msg_id(sender_id.user_id)
    if old_msg_id is not None:
        is_poll = await shared.is_old_msg_poll(sender_id.user_id)
        if is_poll:
            await shared.delete_old_message(client, sender_id.user_id)
            menu_msg = await client.send_message(event.input_sender,
                                                 f'\U0001F464 : {user_profile[3]}\n'
                                                 f'Имя: {user_profile[5]}\n\n'
                                                 f'Результат риск профайла: __{profile_score_str}__\n'
                                                 f'Баланс: __{paid_amount} запросов__\n'
                                                 f'Пользователей бота: __{count}__', buttons=keyboard_profile)
            await shared.save_old_message(sender_id.user_id, menu_msg)
            shared.set_old_msg_poll(sender_id.user_id, False)
        else:
            await client.edit_message(event.input_sender, old_msg_id,
                                      f'\U0001F464 : {user_profile[3]}\n'
                                      f'Имя: {user_profile[5]}\n\n'
                                      f'Результат риск профайла: __{profile_score_str}__\n'
                                      f'Баланс: __{paid_amount} запросов__\n'
                                      f'Пользователей бота: __{count}__', buttons=keyboard_profile)
    else:
        menu_msg = await client.send_message(event.input_sender,
                                             f'\U0001F464 : {user_profile[3]}\n'
                                             f'Имя: {user_profile[5]}\n\n'
                                             f'Результат риск профайла: __{profile_score_str}__\n'
                                             f'Баланс: __{paid_amount} запросов__\n'
                                             f'Пользователей бота: __{count}__', buttons=keyboard_profile)
        await shared.save_old_message(sender_id.user_id, menu_msg)


async def donate_menu(event, client):
    await client.send_message(event.input_sender, '# TODO')


async def information_menu(event, client, engine=engine):
    # Если клиент не до конца прошел профалинг - сбрасываем результат прохождения
    sender_id = event.input_sender.user_id
    await client.delete_messages(sender_id, event.message.id)
    if not is_user_profile_done(sender_id):
        reset_user_profiler_data(sender_id)

    old_msg_id = await shared.get_old_msg_id(sender_id)
    # await event.edit()
    if old_msg_id is not None:
        is_poll = await shared.is_old_msg_poll(sender_id)
        if is_poll:
            await shared.delete_old_message(client, sender_id)
            menu_msg = await client.send_message(event.input_sender, '🛎 Информация', buttons=buttons.keyboard_info)
            await shared.save_old_message(sender_id, menu_msg)
            shared.set_old_msg_poll(sender_id, False)
        else:
            await client.edit_message(event.input_sender, old_msg_id, '🛎 Информация', buttons=buttons.keyboard_info)
    else:
        menu_msg = await client.send_message(event.input_sender, '🛎 Информация', buttons=buttons.keyboard_info)
        await shared.save_old_message(sender_id, menu_msg)

