
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



# @client.on(events.CallbackQuery)
# async def callback(event):
# sender_id = event.original_update.user_id
# entity = await client.get_input_entity(sender_id)
#
# # ============================== Главное меню 1 уровень=============================
# if event.data == b'a1':
#     await client.send_message(event.input_sender, 'Анализ рынков', buttons=buttons.keyboard_a1)
#     await event.edit()
# elif event.data == b'a2':
#     await client.send_message(event.input_sender, 'Конструктор портфелей', buttons=buttons.keyboard_a2)
#     await event.edit()
# elif event.data == b'a3':
#     await client.send_message(event.input_sender, 'Калькуляторы', buttons=buttons.keyboard_a3)
#     await event.edit()
# elif event.data == b'a4':
#     await client.send_message(event.input_sender, 'Управление', buttons=buttons.keyboard_a4)
#     await event.edit()
# elif event.data == b'a5':
#     await client.send_message(event.input_sender, 'Инструкции', buttons=buttons.keyboard_a5)
#     await event.edit()
# elif event.data == b'a6':
#     await client.send_message(event.input_sender, 'Образование', buttons=buttons.keyboard_a6)
#     await event.edit()
# elif event.data == b'a7':
#     await client.send_message(event.input_sender, 'Налоги', buttons=buttons.keyboard_a7)
#     await event.edit()
# elif event.data == b'a8':
#     await client.send_message(event.input_sender, 'Агрегатор новостей', buttons=buttons.keyboard_a8)
#     await event.edit()
# elif event.data == b'main':
#     await client.send_message(event.input_sender, 'Главное меню', buttons=buttons.keyboard_0)
#     await event.edit()
#
# # ============================== Анализ рынков 2 уровень=============================
# elif event.data == b'a1a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(event.input_sender, 'Количество растущих/падающих акций и объёмы за сегодня')
#     filename = os.path.join(IMAGES_OUT_PATH, 'adv.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             await client.send_message(entity=entity, message=f'{row}')
#     await client.send_message(event.input_sender, 'Общая картина')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'sectors.png')
#     await client.send_message(event.input_sender, 'Волатильность и барометр жадности/страха')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'volatility.png')
#     await client.send_message(event.input_sender, 'Тепловая карта 1-day performance')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'treemap.png')
#     await client.edit_message(message, 'Анализ рынка США')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как интерпретировать графики выше? /instruction01',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(event.input_sender, 'Общая картина')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'crypto.png')
#     await client.send_message(event.input_sender, 'Тепловая карта 1-day performance')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'coins_treemap.png')
#     await client.edit_message(message, 'Рынок криптовалют')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как интерпретировать графики выше? /instruction01',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a3':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(event.input_sender, 'Общая картина')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'rtsi.png')
#     await client.edit_message(message, 'Рынок РФ')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как интерпретировать графики выше? /instruction01',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a4':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(entity=entity, message='Денежные потоки в миллионах USD')
#     await client.send_message(entity=entity, message='Денежные потоки SPY')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_SPY.png')
#     await client.send_message(entity=entity, message='Денежные потоки QQQ')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_QQQ.png')
#     await client.send_message(entity=entity, message='Денежные потоки VTI')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VTI.png')
#     await client.send_message(entity=entity, message='Денежные потоки VEA')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VEA.png')
#     await client.send_message(entity=entity, message='Денежные потоки VWO')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VWO.png')
#     await client.send_message(entity=entity, message='Денежные потоки LQD')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_LQD.png')
#     await client.send_message(entity=entity, message='Денежные потоки VXX')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_VXX.png')
#     await client.send_message(entity=entity, message='Денежные потоки SHY')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_SHY.png')
#     await client.send_message(entity=entity, message='Денежные потоки TLT')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'inflows_TLT.png')
#     await client.edit_message(message, 'Ежедневные денежные потоки основных ETF за месяц')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как интерпретировать денежные потоки? /instruction02',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a5':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.send_message(event.input_sender, 'Общая картина 1-day performance')
#     await client.send_file(entity, IMAGES_OUT_PATH + 'global_treemap.png')
#     await client.send_message(event.input_sender, 'Общая картина YTD performance')
#     await client.send_message(event.input_sender, 'Общая картина bubble map')
#     await client.edit_message(message, 'Мировые рынки в картах')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как ? /instruction02',
#                               buttons=buttons.keyboard_a1_back)
# elif event.data == b'a1a6':
#     await client.send_message(event.input_sender, 'Основные макро индикаторы', buttons=buttons.keyboard_core_macro)
#     await event.edit()
# elif event.data == b'a1a-1':
#     await client.send_message(event.input_sender, 'Анализ рынков', buttons=buttons.keyboard_a1)
#     await event.edit()
#
# # ============================== Конструктор стратегий =============================
# elif event.data == b'a2a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Твой профиль риска')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Зачем нужно знать свой профиль риска? /instruction03',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Оценка/аудит портфеля')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Зачем проводить аудит своего портфеля? /instruction04',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a3':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, '"Парковочный" портфель без риска')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать парковочный портфель? /instruction05',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a4':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Всепогодный портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать всепогодный портфель? /instruction06',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a5':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Сбалансированный портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать сбалансированный портфель? /instruction07',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a6':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Агрессивный портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать агрессивный портфель? /instruction08',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a7':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Крипто портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Кому и когда покупать крипто портфель? /instruction09',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a8':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Трейдинг/Дневные стратегии')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Подходит ли вам трейдинг? /instruction10',
#                               buttons=buttons.keyboard_a2_back)
# elif event.data == b'a2a-1':
#     await client.send_message(event.input_sender, 'Конструктор стратегий', buttons=buttons.keyboard_a2)
#     await event.edit()
#
# # ============================== Калькуляторы =============================
# elif event.data == b'a3a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Рассчет количества акций для портфеля')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Конвертация весов в количество? /instruction11',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Симуляция 10 летней доходности')
#     await event.edit()
#     await client.send_message(event.input_sender,
#                               'Что ожидать от текущего портфеля в ближайшую декаду? /instruction12',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a3':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Рассчет оптимального размера взносов')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Почему взносы необходимы? /instruction13',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a4':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Рассчет безопасного размера вывода средств')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Сколько можно выводить средств? /instruction14',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a5':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Сложный процент')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Сложный процент в действии. /instruction15',
#                               buttons=buttons.keyboard_a3_back)
# elif event.data == b'a3a-1':
#     await client.send_message(event.input_sender, 'Калькуляторы', buttons=buttons.keyboard_a3)
#     await event.edit()
#
# # ============================== Управление =============================
# elif event.data == b'a4a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Маркетплейс управляющих')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Все об управлени активами. /instruction16',
#                               buttons=buttons.keyboard_a4_back)
# elif event.data == b'a4a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Стать управляющим')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Стать управляющим',
#                               buttons=buttons.keyboard_a4_back)
# elif event.data == b'a4a-1':
#     await client.send_message(event.input_sender, 'Управление', buttons=buttons.keyboard_a4)
#     await event.edit()
#
# # ============================== Инструкции =============================
# elif event.data == b'a5a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Как ... /instruction01')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как ... /instruction01',
#                               buttons=buttons.keyboard_a5_back)
# elif event.data == b'a5a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Что ... /instruction02')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Что ... /instruction02',
#                               buttons=buttons.keyboard_a5_back)
# elif event.data == b'a5a-1':
#     await client.send_message(event.input_sender, 'Инструкции', buttons=buttons.keyboard_a5)
#     await event.edit()
#
# # ============================== Образовательные программы =============================
# elif event.data == b'a6a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Основы инвестирования')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Основы инвестирования /instruction20',
#                               buttons=buttons.keyboard_a6_back)
# elif event.data == b'a6a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Как собрать свой первый портфель')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Как собрать свой первый портфель /instruction21',
#                               buttons=buttons.keyboard_a6_back)
# elif event.data == b'a6a3':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Профессиональные решения')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Профессиональные решения /instruction22',
#                               buttons=buttons.keyboard_a6_back)
# elif event.data == b'a6a-1':
#     await client.send_message(event.input_sender, 'Образование', buttons=buttons.keyboard_a6)
#     await event.edit()
#
# # ============================== Налоги =============================
# elif event.data == b'a7a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Оптимизация налогов')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Оптимизация налогов /instruction30',
#                               buttons=buttons.keyboard_a7_back)
# elif event.data == b'a7a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Подготовка налоговых деклараций')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Подготовка налоговых деклараций /instruction30',
#                               buttons=buttons.keyboard_a7_back)
# elif event.data == b'a7a-1':
#     await client.send_message(event.input_sender, 'Налоги', buttons=buttons.keyboard_a7)
#     await event.edit()
#
# # ============================== Агрегатор новостей =============================
# elif event.data == b'a8a1':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Поставщики новостей')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Поставщики новостей',
#                               buttons=buttons.keyboard_a8_back)
# elif event.data == b'a8a2':
#     message = await client.send_message(entity=entity, message='Загрузка...')
#     await client.edit_message(message, 'Тикеры')
#     await event.edit()
#     await client.send_message(event.input_sender, 'Тикеры',
#                               buttons=buttons.keyboard_a8_back)
# elif event.data == b'a8a-1':
#     await client.send_message(event.input_sender, 'Агрегатор новостей', buttons=buttons.keyboard_a8)
#     await event.edit()
#
# # elif event.data == b'a4a1':
# #     message = await client.send_message(entity=entity, message='Loading...')
# #     await client.send_file(entity, IMAGES_OUT_PATH + 'us_index.png')
# #     await client.edit_message(message, 'Ипсилон AI US Index')
# #     await event.edit()
# # elif event.data == b'a4a2':
# #     message = await client.send_message(entity=entity, message='Loading...')
# #     await client.send_file(entity, IMAGES_OUT_PATH + 'world_index.png')
# #     await client.edit_message(message, 'Ипсилон AI WORLD Index')
# #     await event.edit()
#
# # ============================== Основные макро данные =============================
# elif event.data == b'cm1':
#     await client.send_message(entity=entity, message='Interest Rates')
#     await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
#     filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             if row[0] == 'Interest Rate':
#                 new_row = ',  '.join(row)
#                 await client.send_message(entity=entity, message=f'{new_row}')
#     await event.edit()
#     await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
# elif event.data == b'cm2':
#     await client.send_message(entity=entity, message='Interest Rates')
#     await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
#     filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             if row[0] == 'Inflation Rate':
#                 new_row = ',  '.join(row)
#                 await client.send_message(entity=entity, message=f'{new_row}')
#     await event.edit()
#     await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
# elif event.data == b'cm3':
#     await client.send_message(entity=entity, message='Interest Rates')
#     await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
#     filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             if row[0] == 'Unemployment Rate':
#                 new_row = ',  '.join(row)
#                 await client.send_message(entity=entity, message=f'{new_row}')
#     await event.edit()
#     await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
# elif event.data == b'cm4':
#     await client.send_message(entity=entity, message='Interest Rates')
#     await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
#     filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
#     with open(filename, newline='') as f:
#         data = csv.reader(f, delimiter=',')
#         for row in data:
#             if row[0] == 'Composite PMI':
#                 new_row = ',  '.join(row)
#                 await client.send_message(entity=entity, message=f'{new_row}')
#     await event.edit()
#     await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
# elif event.data == b'cm-1':
#     await client.send_message(event.input_sender, 'Назад', buttons=buttons.keyboard_core_macro_back)
#     await event.edit()
# elif event.data == b'cm-2':
#     await client.send_message(event.input_sender, 'Назад', buttons=buttons.keyboard_a1)
#     await event.edit()
# elif event.data == b'z2':
#     await client.send_message(event.input_sender,
#                               'Вы можете попросить друга запустить бота и получить бесплатную'
#                               ' подписку. '
#                               'Проще всего это сделать через групповые чаты' + '\n' +
#                               f'[https://t.me/UpsilonBot?start={sender_id}]'
#                               f'(https://t.me/UpsilonBot?start={sender_id})')
#     # TODO Изменить на оригинал
#     await event.edit()


# ============================== Subscriptions =============================
# elif event.data == b'z1':
#     await client.send_message(event.input_sender, 'Уровень подписок', buttons=buttons.keyboard_core_subscriptions)
#     await event.edit()
# elif event.data == b'kcs0':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + 'tariff_compare.jpg')
#     await event.edit()
# elif event.data == b'kcs1':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + 'tariff_start.jpg')
#     await client.send_message(event.input_sender, 'Тут описание тарифа Старт',
#                               buttons=buttons.keyboard_subscription_start)
#     await event.edit()
# elif event.data == b'kcs2':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + '/tariff_base.png')
#     await client.send_message(event.input_sender, 'Тут описание тарифа Базовый',
#                               buttons=buttons.keyboard_subscription_base)
# elif event.data == b'kcs3':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + '/tariff_advanced.png')
#     await client.send_message(event.input_sender, 'Тут описание тарифа Продвинутый',
#                               buttons=buttons.keyboard_subscription_advanced)
# elif event.data == b'kcs4':
#     await client.send_file(event.input_sender, TARIFF_IMAGES + '/tariff_professional.jpg')
#     await client.send_message(event.input_sender, 'Тут описание тарифа Профессиональный',
#                               buttons=buttons.keyboard_subscription_professional)
# elif event.data == b'kcs-1':
#     await menu.profile_menu(event, client, engine)
# #   TODO добавить описание подписок
# #   TODO добавить таблицу сравнения подписок
# elif event.data == b'kss1' or event.data == b'kss2' or event.data == b'kss3' or event.data == b'kss4':
#     global PAYMENT_AGGREGATOR
#     if PAYMENT_AGGREGATOR is None:
#         PAYMENT_AGGREGATOR = PaymentAgregator()
#         PAYMENT_AGGREGATOR.creator('Free Kassa')
#     aggregator_status = PAYMENT_AGGREGATOR.get_status()
#     global PAYMENT_AGGREGATOR_TIMER
#     if PAYMENT_AGGREGATOR_TIMER is not None:
#         delta = time.time() - PAYMENT_AGGREGATOR_TIMER
#         if delta >= 10:
#             aggregator_status = PAYMENT_AGGREGATOR.get_status()
#         else:
#             time.sleep(10 - delta)
#             aggregator_status = PAYMENT_AGGREGATOR.get_status()
#     else:
#         PAYMENT_AGGREGATOR_TIMER = time.time()
#         aggregator_status = PAYMENT_AGGREGATOR.get_status()
#     # print(aggregator_status)
#     if aggregator_status == 'error':
#         # print("Error description:" + PAYMENT_AGGREGATOR.get_last_error())
#         await client.send_message(event.input_sender, 'Упс. Что-то пошло не так.',
#                                   buttons=buttons.keyboard_subscription_start)
#         await event.edit()
#     else:
#         # print("user_id=" + str(sender_id.user_id))
#         order_id = str(uuid.uuid4()).replace('-', '')
#         print("OrderId:" + order_id)
#         summa = ""
#         kbd_label = ""
#         if event.data == b'kss1':
#             summa = "15.00"
#             kbd_label = "Оплатить ($15)"
#         elif event.data == b'kss2':
#             summa = "25.00"
#             kbd_label = "Оплатить ($25)"
#         elif event.data == b'kss3':
#             summa = "30.00"
#             kbd_label = "Оплатить ($30)"
#         elif event.data == b'kss2':
#             summa = "40.00"
#             kbd_label = "Оплатить ($40)"
#
#         print("Summa:" + summa)
#         payment_link = PAYMENT_AGGREGATOR.get_payment_link(order_id, summa)
#         print(payment_link)
#         keyboard_subscr_start_inst = [
#             [
#                 Button.url('\U0001F3E6  ' + kbd_label, payment_link)
#             ]
#         ]
#
#         paymsg = await client.send_message(event.input_sender,
#                                            'Для оплаты тарифа Start нажмите кнопку Оплатить\n'
#                                            '(Инструкция по оплате [тут](https://telegra.ph/Rrrtt-10-13)! )',
#                                            link_preview=True,
#                                            buttons=keyboard_subscr_start_inst)
#         await event.edit()
#         sender = event.input_sender
#         msg_id = utils.get_message_id(paymsg)
#         global ORDER_MAP
#         ORDER_MAP[order_id] = (sender_id, msg_id)
#         dt = datetime.now()
#         dt_int = datetime2int(dt)
#         await sql.insert_into_payment_message(order_id, sender_id, msg_id, dt_int, engine)



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
