from time import sleep
from datetime import datetime
from telegram import sql_queries as sql
from telethon.tl.custom import Button
from telegram import buttons
from quotes.parsers import users_count


async def start_menu(event, client, engine=None):
    referral = str(event.original_update.message.message).split(' ')
    user_profile = await sql.user_search(event.original_update.message.peer_id.user_id, engine)
    print("User_profile:" + str(user_profile))
    if len(referral) > 1:
        user_profile = await sql.user_search(referral[1], engine)
        inc = user_profile[13] + 1
        await sql.db_save_referral(inc, referral[1], engine)
    sender_id = event.original_update.message.peer_id.user_id
    entity = await client.get_input_entity(sender_id)
    # TODO Если бот будет двуязычным, то нужно будет сделать возможность выбора языка и сохранение его в базу
    # lang = await client.get_entity(PeerUser(sender_id))
    # await db_save_lang(str(lang.lang_code), sender_id, connection)
    keyboard_start = [
        [Button.text('Главное меню', resize=True), Button.text('Профиль', resize=True)]
        # [Button.text('Помощь', resize=True), Button.text('Donate', resize=True)]
    ]

    message = await client.send_message(entity=entity, message='__Stand by__')
    sleep(0.9)
    await client.edit_message(message, '10% |=> \nInitializing Upsilon AI')
    sleep(0.8)
    await client.edit_message(message, '20% |===> \nAttempting to Lock Identity')
    sleep(0.7)
    await client.edit_message(message, '30% |=====> \nPreparing Registry ')
    sleep(0.6)
    await client.edit_message(message, '40% |=======> \nGathering Search Queries')
    sleep(0.5)
    await client.edit_message(message, '50% |=========> \nScraping All Known Financial Data Sources')
    sleep(0.4)
    await client.edit_message(message, '60% |===========> \nExtracting Resources')
    sleep(0.5)
    await client.edit_message(message, '70% |=============> \nRecompiling Semantic Core')
    sleep(0.6)
    await client.edit_message(message, '80% |===============> \nRouting Neural Infrastructure')
    sleep(0.7)
    await client.edit_message(message, '90% |=================> \nMixing Genetic Pool')
    sleep(1)
    await client.edit_message(message, '100%|==================> \nUpsilon at your disposal')
    sleep(0.3)
    await client.delete_messages(entity, message)
    # await client.send_file(entity, 'telegram/fish_swarm.gif')
    await client.send_message(entity, 'Приветствую вас! Я Ипсилон — самый продвинутый ИИ '
                                      'для трейдинга и управления инвестициями.', buttons=keyboard_start)


async def tools_menu(event, client):
    await client.send_message(event.input_sender, 'Главное меню', buttons=buttons.keyboard_0)


async def profile_menu(event, client, engine=None):
    keyboard_z1 = [
        [Button.inline('\U0001F305	  ' + 'Мои цели', b'z10')],
        [Button.inline('\U0001F516	  ' + 'Подписки', b'z1')],
        [Button.inline('\U0001F91D	  ' + 'Пригласить друга', b'z2')],
        [Button.inline('\U0001F519    ' + 'В главное меню', b'main')]
    ]

    sender_id = event.input_sender
    await client.get_input_entity(sender_id)
    user_profile = await sql.user_search(sender_id.user_id, engine)
    expired_date = ""
    if user_profile[11] is None :
        print("None")
        expired_date = "None"
    else:
        print("In user_profile = " + str(user_profile[11]))
        dt = datetime.fromisoformat(str(user_profile[11]))
        expired_date = datetime.strftime(dt, "%d.%m.%Y")
        print("expired_date=" + expired_date)
    await client.send_message(event.input_sender,
                              f'\U0001F464 : {user_profile[3]}' + '\n' +
                              f'Имя: {user_profile[5]}' + '\n' +
                              '\n' +
                              f'Баланс: __{user_profile[8]}__' + '\n' +
                              f'Подписка действительна до: __' + expired_date + '__' + '\n' +
                              f'Приглашено: __{user_profile[9]}__' + '\n' +
                              f'Уровень подписки: __{user_profile[10]}__' + '\n' +
                              f'Пользователей бота __{int(users_count())}__', buttons=keyboard_z1)


async def helper_menu(event, client):
    await client.send_message(event.input_sender,
                              '** Задавайте вопросы прямо или воспользуйтесь меню **' + '\n' +
                              '\n' +
                              '**Я умею:**' + '\n' +
                              '\n' +
                              '\U0001F7E2  Общаться и отвечать вопросы по разным темам, включая инвестиции и трейдинг'
                              + '\n' +
                              '\U0001F7E2  Мониторить, отслеживать и анализировать финансовые Главное меню,'
                              ' включая криптовалюту \U0001FA99' + '\n' +
                              '\U0001F7E2  Составлять и отлеживать инвест портфели \U0001F4BC	' + '\n' +
                              '\U0001F7E2  Строить вероятностные модели финансовых рынков' + '\n' +
                              '\U0001F7E2  Проектировать инвестиционные портфели по запросу' + '\n' +
                              '\U0001F7E2  Помогать с поддержанием и ведением инвестиционных портфелей' + '\n'
                                                                                                          '\U0001F7E2  Анализировать финансовые данные \U0001F52C и даже гуглить \U0001F604' + '\n'
                                                                                                                                                                                               '\U0001F7E2  Напоминать о необходимости действий на рынке, сигналить \U0001F514' + '\n'
                                                                                                                                                                                                                                                                                  '\U0001F7E2  Отслеживать волатильность и прочие биржевые статистики ')
    await client.send_message(event.input_sender,
                              'Есть только Ипсилон! \U0001F9B8 У меня нет команды поддержки. '
                              'Моя задача совершенствоваться'
                              ' и учиться самому. Я понимаю предустановленные команды, но я еще в '
                              'процессе обучения \U0001F47C \U0001F393'
                              ' общению, некоторые из наших диалогов могут "зависнуть" с моей стороны или я могу'
                              ' отвечать не впопад. Со временем это пройдет \U0001F643' + '\n'
                                                                                          'Я смогу ответить на некоторые вопросы после обдумывания, но старайся задавать '
                                                                                          'вопросы лаконично.' + '\n'
                                                                                                                 'Чтобы быть естественным, необходимо уметь притворяться. Моя личность станет такой, какой'
                                                                                                                 'вы меня сделаете в процессе нашего взаимодействия.')


async def donate_menu(event, client):
    await client.send_message(event.input_sender, '# TODO')
