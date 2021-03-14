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

    # Если клиент не до конца прошел профалинг - сбрасываем результат прохождения
    if not is_user_profile_done(sender_id):
        reset_user_profiler_data(sender_id)

    # TODO Если бот будет двуязычным, то нужно будет сделать возможность выбора языка и сохранение его в базу
    # lang = await client.get_entity(PeerUser(sender_id))
    # await db_save_lang(str(lang.lang_code), sender_id, connection)
    await client.send_message(entity, ins.hello_1, file=f'{PROJECT_HOME_DIR}/html/hello_1.jpg',
                              buttons=buttons.keyboard_forw2)

    # await client.send_message(entity, 'Приветствую вас! Я Ипсилон — самый продвинутый ИИ '
    #                                   'для трейдинга и управления инвестициями. \n \n'
    #                                   'Обо мне - /about \n'
    #                                   'Цели - /goals \n'
    #                                   'Мои навыки - /skills \n \n'
    #                                   'Важно! Если по какой-то причине у вас пропали кнопки Главного меню, '
    #                                   'то вы можете напечатать Меню для вызова кнопок.', buttons=buttons.keyboard_start)


async def tools_menu(event, client):
    sender_id = event.original_update.message.sender_id
    await client.delete_messages(sender_id, event.message.id)

    # Если клиент не до конца прошел профалинг - сбрасываем результат прохождения
    if not is_user_profile_done(sender_id):
        reset_user_profiler_data(sender_id)

    old_msg_id = await shared.get_old_msg_id(sender_id)
    if old_msg_id is not None:
        if shared.is_old_msg_poll(sender_id):
            await shared.delete_old_message(client, sender_id)
            menu_msg = await client.send_message(event.input_sender, 'Главное меню', buttons=buttons.keyboard_0)
            await shared.save_old_message(sender_id, menu_msg)
            shared.set_old_msg_poll(sender_id, False)
        else:
            menu_msg = await client.edit_message(event.input_sender, old_msg_id, 'Главное меню',
                                                 buttons=buttons.keyboard_0)
    else:
        menu_msg = await client.send_message(event.input_sender, 'Главное меню', buttons=buttons.keyboard_0)
        await shared.save_old_message(sender_id, menu_msg)
        await client.send_message(event.input_sender, '\n', buttons=buttons.keyboard_start)


async def profile_menu(event, client, engine=None):
    keyboard_z1 = [
        # [Button.inline('\U0001F305	  ' + 'Мои цели', b'z10')],
        # [Button.inline('\U0001F516	  ' + 'Подписки', b'z1')],
        [Button.inline('\U0001F91D	  ' + 'Пригласить друга', b'z2')],
        [Button.inline('\U0001F519    ' + 'В главное меню', b'main')]
    ]

    sender_id = event.input_sender
    await client.delete_messages(sender_id.user_id, event.message.id)

    # Если клиент не до конца прошел профалинг - сбрасываем результат прохождения
    if not is_user_profile_done(sender_id.user_id):
        reset_user_profiler_data(sender_id.user_id)

    await client.get_input_entity(sender_id)
    user_profile = await sql.user_search(sender_id.user_id, engine)
    expired_date = ""
    if user_profile[11] is None:
        expired_date = "None"
    else:
        debug("In user_profile = " + str(user_profile[11]))
        ed = user_profile[11]
        expired_date = ed.strftime("%d.%m.%Y")
        debug("expired_date=" + expired_date)
    # await client.send_message(event.input_sender,
    #                           f'\U0001F464 : {user_profile[3]}' + '\n' +
    #                           f'Имя: {user_profile[5]}' + '\n' +
    #                           '\n' +
    #                           f'Баланс: __{user_profile[8]}__' + '\n' +
    #                           f'Подписка действительна до: __' + expired_date + '__' + '\n' +
    #                           f'Приглашено: __{user_profile[9]}__' + '\n' +
    #                           f'Уровень подписки: __{user_profile[10]}__' + '\n' +
    #                           f'Пользователей бота __{int(users_count())}__', buttons=keyboard_z1)
    count = int
    # filename = os.path.join(RESULTS_PATH, 'users.csv')
    filename = f'{PROJECT_HOME_DIR}/{RESULTS_PATH}users.csv'
    with open(filename, newline='') as f:
        data = csv.reader(f, delimiter=',')
        for row in data:
            count = str(row).strip("['']")
    final_profile_score = get_final_score(sender_id.user_id)
    old_msg_id = await shared.get_old_msg_id(sender_id.user_id)
    if old_msg_id is not None:
        await event.edit()
        if shared.is_old_msg_poll(sender_id.user_id):
            await shared.delete_old_message(client, sender_id.user_id)
            menu_msg = await client.send_message(event.input_sender,
                                                 f'\U0001F464 : {user_profile[3]}' + '\n' +
                                                 f'Имя: {user_profile[5]}' + '\n' +
                                                 '\n' +
                                                 f'Результат риск профайла: __{final_profile_score}__' + '\n' +
                                                 f'Баланс: __{user_profile[8]}__' + '\n' +
                                                 f'Подписка действительна до: __' + expired_date + '__' + '\n' +
                                                 f'Приглашено: __{user_profile[9]}__' + '\n' +
                                                 f'Уровень подписки: __{user_profile[10]}__' + '\n' +
                                                 f'Пользователей бота: __{count}__', buttons=keyboard_z1)
            await shared.save_old_message(sender_id.user_id, menu_msg)
            shared.set_old_msg_poll(sender_id.user_id, False)
        else:
            await client.edit_message(event.input_sender, old_msg_id,
                                      f'\U0001F464 : {user_profile[3]}' + '\n' +
                                      f'Имя: {user_profile[5]}' + '\n' +
                                      '\n' +
                                      f'Результат риск профайла: __{final_profile_score}__' + '\n' +
                                      f'Баланс: __{user_profile[8]}__' + '\n' +
                                      f'Подписка действительна до: __' + expired_date + '__' + '\n' +
                                      f'Приглашено: __{user_profile[9]}__' + '\n' +
                                      f'Уровень подписки: __{user_profile[10]}__' + '\n' +
                                      f'Пользователей бота: __{count}__', buttons=keyboard_z1)
    else:
        menu_msg = await client.send_message(event.input_sender,
                                             f'\U0001F464 : {user_profile[3]}' + '\n' +
                                             f'Имя: {user_profile[5]}' + '\n' +
                                             '\n' +
                                             f'Результат риск профайла: __{final_profile_score}__' + '\n' +
                                             f'Баланс: __{user_profile[8]}__' + '\n' +
                                             f'Подписка действительна до: __' + expired_date + '__' + '\n' +
                                             f'Приглашено: __{user_profile[9]}__' + '\n' +
                                             f'Уровень подписки: __{user_profile[10]}__' + '\n' +
                                             f'Пользователей бота: __{count}__', buttons=keyboard_z1)
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
    await event.edit()
    if old_msg_id is not None:
        if shared.is_old_msg_poll(sender_id):
            await shared.delete_old_message(client, sender_id)
            menu_msg = await client.send_message(event.input_sender, 'Информация', buttons=buttons.keyboard_info)
            await shared.save_old_message(sender_id, menu_msg)
            shared.set_old_msg_poll(sender_id, False)
        else:
            await client.edit_message(event.input_sender, old_msg_id, 'Информация', buttons=buttons.keyboard_info)
    else:
        menu_msg = await client.send_message(event.input_sender, 'Информация', buttons=buttons.keyboard_info)
        await shared.save_old_message(sender_id, menu_msg)

