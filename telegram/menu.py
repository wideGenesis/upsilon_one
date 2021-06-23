import importlib
import sys
from time import sleep
import csv
from datetime import datetime

import telethon

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
    shared.del_is_inspector_flow(event.input_sender.user_id)
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
            await client.send_message(event.input_sender, '👤 Profile')
            await callbacks.send_next_profiler_question(client, sender_id, 0)
    else:
        # Если юзер уже прошел профайлинг, то ему не надо показывать презу и опрос - сразу Main menu
        await tools_menu(event, client)
    # Сохраним данные о новом пользователе (функция сохранит и распечатает, только если пользователь ранее не числился)
    await sql.append_new_user(sender_id)


async def meta_menu(event, client):
    sender_id = event.original_update.message.sender_id
    shared.del_is_inspector_flow(event.input_sender.user_id)
    old_msg_id = await shared.get_old_msg_id(sender_id)
    if old_msg_id is not None:
        shared.pop_old_msg_id(sender_id)
    await client.send_message(event.input_sender, '.', buttons=buttons.keyboard_start)


async def tools_menu(event, client):
    sender_id = event.original_update.message.sender_id
    shared.del_is_inspector_flow(event.input_sender.user_id)
    try:
        await client.delete_messages(sender_id, event.message.id)
    except Exception:
        pass

    # Если клиент не до конца прошел профалинг - сбрасываем результат прохождения
    if not is_user_profile_done(sender_id):
        reset_user_profiler_data(sender_id)

    old_msg_id = await shared.get_old_msg_id(sender_id)
    if old_msg_id is not None:
        is_poll = await shared.is_old_msg_poll(sender_id)
        if is_poll:
            await shared.delete_old_message(client, sender_id)
            menu_msg = await client.send_message(event.input_sender, '📁 Main menu', buttons=buttons.keyboard_0)
            await shared.save_old_message(sender_id, menu_msg)
            shared.set_old_msg_poll(sender_id, False)
        else:
            try:
                await client.edit_message(event.input_sender, old_msg_id, '📁 Main menu',
                                          buttons=buttons.keyboard_0)
            except telethon.errors.rpcerrorlist.MessageNotModifiedError as e:
                debug(f'Double click for Main menu: {e}', ERROR)
    else:
        menu_msg = await client.send_message(event.input_sender, '📁 Main menu', buttons=buttons.keyboard_0)
        await shared.save_old_message(sender_id, menu_msg)


async def profile_menu(event, client, engine=None):
    keyboard_profile = [
        [Button.inline('🔋	  ' + 'Buy requests❗', b'requests_store')],
        [Button.inline('\U0001F91D	  ' + 'To invite a friend', b'invite_friends')],
        [Button.inline('🔃	  ' + 'Reset Risk Profile', b'risk_reset')],
        [Button.inline('\U0001F519    ' + 'Back to Main menu', b'main')]
    ]

    sender_id = event.input_sender
    shared.del_is_inspector_flow(sender_id.user_id)
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
            profile_score_str = "Total risk aversion"
        elif -9 < final_profile_score <= -4:
            profile_score_str = "Strong risk aversion"
        elif -4 < final_profile_score <= 1:
            profile_score_str = "Moderate risk aversion"
        elif 1 < final_profile_score < 6:
            profile_score_str = "Reasonable risk taking"
        elif 6 <= final_profile_score < 10:
            profile_score_str = "Confident risk taking"
        elif final_profile_score >= 10:
            profile_score_str = "Total risk acceptance"
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
                                                 f'Name: {user_profile[5]}\n\n'
                                                 f'Your level of risk: __{profile_score_str}__\n\n'
                                                 f'Paid requests: __{paid_amount}__ 🔋\n'
                                                 f'--------------------------------------------------------\n\n'
                                                 f'Bot users: __{count}__', buttons=keyboard_profile)
            await shared.save_old_message(sender_id.user_id, menu_msg)
            shared.set_old_msg_poll(sender_id.user_id, False)
        else:
            try:
                await client.edit_message(event.input_sender, old_msg_id,
                                          f'\U0001F464 : {user_profile[3]}\n'
                                          f'Name: {user_profile[5]}\n\n'
                                          f'Your level of risk: __{profile_score_str}__\n\n'
                                          f'Paid requests: __{paid_amount}__ 🔋\n'
                                          f'--------------------------------------------------------\n\n'
                                          f'Bot users: __{count}__', buttons=keyboard_profile)
            except telethon.errors.rpcerrorlist.MessageNotModifiedError as e:
                debug(f'Двойное нажатие кнопки Profile: {e}', ERROR)
    else:
        menu_msg = await client.send_message(event.input_sender,
                                             f'\U0001F464 : {user_profile[3]}\n'
                                             f'Name: {user_profile[5]}\n\n'
                                             f'Your level of risk: __{profile_score_str}__\n\n'
                                             f'Paid requests: __{paid_amount}__ 🔋\n'
                                             f'--------------------------------------------------------\n\n'
                                             f'Bot users: __{count}__', buttons=keyboard_profile)
        await shared.save_old_message(sender_id.user_id, menu_msg)


async def donate_menu(event, client):
    await client.send_message(event.input_sender, '# TODO')


async def information_menu(event, client, engine=engine):
    # Если клиент не до конца прошел профалинг - сбрасываем результат прохождения
    sender_id = event.input_sender.user_id
    shared.del_is_inspector_flow(sender_id)
    try:
        await client.delete_messages(sender_id, event.message.id)
    except Exception:
        pass
    if not is_user_profile_done(sender_id):
        reset_user_profiler_data(sender_id)

    old_msg_id = await shared.get_old_msg_id(sender_id)
    # await event.edit()
    if old_msg_id is not None:
        is_poll = await shared.is_old_msg_poll(sender_id)
        if is_poll:
            await shared.delete_old_message(client, sender_id)
            menu_msg = await client.send_message(event.input_sender, '🛎 Information', buttons=buttons.keyboard_info)
            await shared.save_old_message(sender_id, menu_msg)
            shared.set_old_msg_poll(sender_id, False)
        else:
            try:
                await client.edit_message(event.input_sender, old_msg_id, '🛎 Information',
                                          buttons=buttons.keyboard_info)
            except telethon.errors.rpcerrorlist.MessageNotModifiedError as e:
                debug(f'Двойное нажатие кнопки Information: {e}', ERROR)
    else:
        menu_msg = await client.send_message(event.input_sender, '🛎 Information', buttons=buttons.keyboard_info)
        await shared.save_old_message(sender_id, menu_msg)

