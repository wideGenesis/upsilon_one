
# @client.on(events.NewMessage(pattern='/start'))
# async def start(event):
#     referral = str(event.original_update.message.message).split(' ')
#     if len(referral) > 1:
#         user_profile = await user_search(referral[1])
#         inc = user_profile[13] + 1
#         await db_save_referral(inc, referral[1])
#     sender_id = event.original_update.message.peer_id.user_id
#     entity = await client.get_input_entity(sender_id)
#     # TODO Если бот будет двуязычным, то нужно будет сделать возможность выбора языка и сохранение его в базу
#     # lang = await client.get_entity(PeerUser(sender_id))
#     # await db_save_lang(str(lang.lang_code), sender_id)
#     keyboard_start = [
#         [Button.text('Главное меню', resize=True), Button.text('Профиль', resize=True)]
#         # [Button.text('Помощь', resize=True), Button.text('Donate', resize=True)]
#     ]
#
#     message = await client.send_message(entity=entity, message='__Stand by__')
#     time.sleep(0.9)
#     await client.edit_message(message, '10% |=> \nInitializing Upsilon AI')
#     time.sleep(0.8)
#     await client.edit_message(message, '20% |===> \nAttempting to Lock Identity')
#     time.sleep(0.7)
#     await client.edit_message(message, '30% |=====> \nPreparing Registry ')
#     time.sleep(0.6)
#     await client.edit_message(message, '40% |=======> \nGathering Search Queries')
#     time.sleep(0.5)
#     await client.edit_message(message, '50% |=========> \nScraping All Known Financial Data Sources')
#     time.sleep(0.4)
#     await client.edit_message(message, '60% |===========> \nExtracting Resources')
#     time.sleep(0.5)
#     await client.edit_message(message, '70% |=============> \nRecompiling Semantic Core')
#     time.sleep(0.6)
#     await client.edit_message(message, '80% |===============> \nRouting Neural Infrastructure')
#     time.sleep(0.7)
#     await client.edit_message(message, '90% |=================> \nMixing Genetic Pool')
#     time.sleep(1)
#     await client.edit_message(message, '100%|==================> \nUpsilon at your disposal')
#     time.sleep(0.3)
#     await client.delete_messages(entity, message)
#     # await client.send_file(entity, 'telegram/fish_swarm.gif')
#     await client.send_message(entity, 'Приветствую вас! Я Ипсилон — самый продвинутый ИИ '
#                                       'для трейдинга и управления инвестициями.', buttons=keyboard_start)
# @client.on(events.NewMessage(pattern='Главное меню'))
# async def tools(event):
#     await client.send_message(event.input_sender, 'Главное меню', buttons=buttons.keyboard_0)
# @client.on(events.NewMessage(pattern='Профиль'))
# async def profile(event):
#     keyboard_z1 = [
#         [Button.inline('\U0001F516	  ' + 'Подписки', b'z1')],
#         [Button.inline('\U0001F91D	  ' + 'Пригласить друга', b'z2')]
#     ]
#     sender_id = event.input_sender
#     await client.get_input_entity(sender_id)
#     user_profile = await user_search(sender_id.user_id)
#     await client.send_message(event.input_sender,
#                               f'\U0001F464 : {user_profile[3]}' + '\n' +
#                               f'Имя: {user_profile[5]}' + '\n' +
#                               '\n' +
#                               f'баланс: {user_profile[8]}' + '\n' +
#                               f'Подписка действительна до: {user_profile[11]}' + '\n' +
#                               f'Приглашено: {user_profile[9]}' + '\n' +
#                               f'Уровень подписки: {user_profile[10]}', buttons=keyboard_z1)
# @client.on(events.NewMessage(pattern='Помощь'))
# async def helper(event):
#     await client.send_message(event.input_sender,
#                               '** Задавайте вопросы прямо или воспользуйтесь меню **' + '\n' +
#                               '\n' +
#                               '**Я умею:**' + '\n' +
#                               '\n' +
#                               '\U0001F7E2  Общаться и отвечать вопросы по разным темам, включая инвестиции и трейдинг'
#                               + '\n' +
#                               '\U0001F7E2  Мониторить, отслеживать и анализировать финансовые Главное меню,'
#                               ' включая криптовалюту \U0001FA99' + '\n' +
#                               '\U0001F7E2  Составлять и отлеживать инвест портфели \U0001F4BC	' + '\n' +
#                               '\U0001F7E2  Строить вероятностные модели финансовых рынков' + '\n' +
#                               '\U0001F7E2  Проектировать инвестиционные портфели по запросу' + '\n' +
#                               '\U0001F7E2  Помогать с поддержанием и ведением инвестиционных портфелей' + '\n'
#                               '\U0001F7E2  Анализировать финансовые данные \U0001F52C и даже гуглить \U0001F604' + '\n'
#                               '\U0001F7E2  Напоминать о необходимости действий на рынке, сигналить \U0001F514' + '\n'
#                               '\U0001F7E2  Отслеживать волатильность и прочие биржевые статистики ')
#     await client.send_message(event.input_sender,
#                               'Есть только Ипсилон! \U0001F9B8 У меня нет команды поддержки. '
#                               'Моя задача совершенствоваться'
#                               ' и учиться самому. Я понимаю предустановленные команды, но я еще в '
#                               'процессе обучения \U0001F47C \U0001F393'
#                               ' общению, некоторые из наших диалогов могут "зависнуть" с моей стороны или я могу'
#                               ' отвечать не впопад. Со временем это пройдет \U0001F643' + '\n'
#                               'Я смогу ответить на некоторые вопросы после обдумывания, но старайся задавать '
#                               'вопросы лаконично.' + '\n'
#                               'Чтобы быть естественным, необходимо уметь притворяться. Моя личность станет такой, какой'
#                               'вы меня сделаете в процессе нашего взаимодействия.')
#
#
# @client.on(events.NewMessage(pattern='Donate'))
# async def premium(event):
#     await client.send_message(event.input_sender, BTC + '\n' +
#                               ETH)



# Не имеет смысла не будучи админом канала
# @client.on(events.NewMessage(pattern='/join_to'))
# async def join_to(event):
#     parse = str(event.text).split('|')
#     try:
#         channel = await client.get_entity('https://t.me/' + str(parse[1]))
#     except ValueError as e:
#         logging.exception(e, 'Cant get channel entity')
#     try:
#         if int(event.input_sender.user_id) == int(OWNER):
#             await client(JoinChannelRequest(channel))
#         else:
#             await client.send_message(event.input_sender, 'Order dismissed!')
#     except ValueError as e:
#         logging.exception(e, 'Some error from join_to()' + '\n' + 'Cant join channel entity')
#     time.sleep(10)
#     try:
#         chat = await event.get_input_chat()
#         print(chat, '1dgggdg')
#         participants = await client.get_participants(chat)
#     except AttributeError as e:
#         logging.exception(e, 'Some error from join_to()')
#     for user in participants:
#         if user.id is not None:
#             entity = await client.get_entity(PeerUser(user.id))
#             print('Channel dump complete!')
#     time.sleep(10)
#     await client(LeaveChannelRequest(chat))

# Имеет мысл только из под аккаунта, из под бота не работает
# async for dialog in client.iter_dialogs():
#     print(dialog.name, 'has ID', dialog.id)

# from telethon import Button
#
# markup = client.build_reply_markup(Button.inline('hi'))
# # later
# await client.send_message(chat, 'click me', buttons=markup)
# https://tl.telethon.dev/?q=ReplyInlineMarkup
# https://tl.telethon.dev/?q=ReplyKeyboardMarkup


# async def dump_all_participants(channel):
#     """Записывает json-файл с информацией о всех участниках канала/чата"""
#     offset_user = 0  # номер участника, с которого начинается считывание
#     limit_user = 100  # максимальное число записей, передаваемых за один раз
#
#     all_participants = []  # список всех участников канала
#     filter_user = ChannelParticipantsSearch('')
#
#     while True:
#         participants = await client(GetParticipantsRequest(channel,
#                                                            filter_user, offset_user, limit_user, hash=0))
#         if not participants.users:
#             break
#         all_participants.extend(participants.users)
#         offset_user += len(participants.users)
#
#     all_users_details = []  # список словарей с интересующими параметрами участников канала
#
#     for participant in all_participants:
#         all_users_details.append({"id": participant.id,
#                                   "first_name": participant.first_name,
#                                   "last_name": participant.last_name,
#                                   "user": participant.username,
#                                   "phone": participant.phone,
#                                   "is_bot": participant.bot})
#
#     with open('channel_users.json', 'w', encoding='utf8') as outfile:
#         json.dump(all_users_details, outfile, ensure_ascii=False)
#
#
# async def main():
#     url = input("Введите ссылку на канал или чат: ")
#     channel = await client.get_entity(url)
#     await dump_all_participants(channel)

# https://telethonn.readthedocs.io/en/latest/extra/examples/chats-and-channels.html
# from telethon.tl.functions.channels import GetParticipantsRequest
# from telethon.tl.types import ChannelParticipantsSearch
# from time import sleep
#
# offset = 0
# limit = 100
# all_participants = []
#
# while True:
#     participants = client(GetParticipantsRequest(
#         channel, ChannelParticipantsSearch(''), offset, limit,
#         hash=0
#     ))
#     if not participants.users:
#         break
#     all_participants.extend(participants.users)
#     offset += len(participants.users)
