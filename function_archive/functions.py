



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
