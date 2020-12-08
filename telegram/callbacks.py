import os
import csv
import datetime
import time
import uuid

from datetime import timedelta, datetime
from telethon import utils

from telegram import buttons
from telegram import sql_queries as sql
from telegram import menu
from telegram import shared
from payments.payagregator import PaymentAgregator
from quotes.parsers import vix_cont

PAYMENT_AGGREGATOR = None
PAYMENT_AGGREGATOR_TIMER = None


# ============================== Callbacks =======================

async def callback_handler(event, client, img_path=None, yahoo_path=None, engine=None):
    sender_id = event.original_update.user_id
    entity = await client.get_input_entity(sender_id)

    # ============================== Главное меню 1 уровень=============================
    if event.data == b'a1':
        await client.send_message(event.input_sender, 'Анализ рынков', buttons=buttons.keyboard_a1)
        await event.edit()
    elif event.data == b'a2':
        await client.send_message(event.input_sender, 'Конструктор портфелей', buttons=buttons.keyboard_a2)
        await event.edit()
    elif event.data == b'a3':
        await client.send_message(event.input_sender, 'Калькуляторы', buttons=buttons.keyboard_a3)
        await event.edit()
    elif event.data == b'a4':
        await client.send_message(event.input_sender, 'Управление', buttons=buttons.keyboard_a4)
        await event.edit()
    elif event.data == b'a5':
        await client.send_message(event.input_sender, 'Инструкции', buttons=buttons.keyboard_a5)
        await event.edit()
    elif event.data == b'a6':
        await client.send_message(event.input_sender, 'Образование', buttons=buttons.keyboard_a6)
        await event.edit()
    elif event.data == b'a7':
        await client.send_message(event.input_sender, 'Налоги', buttons=buttons.keyboard_a7)
        await event.edit()
    elif event.data == b'a8':
        await client.send_message(event.input_sender, 'Агрегатор новостей', buttons=buttons.keyboard_a8)
        await event.edit()
    elif event.data == b'main':
        await client.send_message(event.input_sender, 'Главное меню', buttons=buttons.keyboard_0)
        await event.edit()

    # ============================== Анализ рынков 2 уровень=============================
    elif event.data == b'a1a1':
        await client.send_message(event.input_sender, 'Рынок США', buttons=buttons.keyboard_us_market)
        await event.edit()
    elif event.data == b'a1a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(event.input_sender, 'Общая картина')
        await client.send_file(entity, img_path + 'crypto.png')
        await client.send_message(event.input_sender, 'Тепловая карта 1-day performance')
        await client.send_file(entity, img_path + 'coins_treemap.png')
        await client.edit_message(message, 'Рынок криптовалют')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать графики выше? /instruction01',
                                  buttons=buttons.keyboard_a1_back)
    elif event.data == b'a1a3':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(event.input_sender, 'Общая картина')
        await client.send_file(entity, img_path + 'rtsi.png')
        await client.edit_message(message, 'Рынок РФ')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать графики выше? /instruction01',
                                  buttons=buttons.keyboard_a1_back)
    elif event.data == b'a1a4':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(entity=entity, message='Денежные потоки в миллионах USD')
        await client.send_message(entity=entity, message='Денежные потоки SPY')
        await client.send_file(entity, img_path + 'inflows_SPY.png')
        await client.send_message(entity=entity, message='Денежные потоки QQQ')
        await client.send_file(entity, img_path + 'inflows_QQQ.png')
        await client.send_message(entity=entity, message='Денежные потоки VTI')
        await client.send_file(entity, img_path + 'inflows_VTI.png')
        time.sleep(1)
        await client.send_message(entity=entity, message='Денежные потоки VEA')
        await client.send_file(entity, img_path + 'inflows_VEA.png')
        await client.send_message(entity=entity, message='Денежные потоки VWO')
        await client.send_file(entity, img_path + 'inflows_VWO.png')
        await client.send_message(entity=entity, message='Денежные потоки LQD')
        await client.send_file(entity, img_path + 'inflows_LQD.png')
        await client.send_message(entity=entity, message='Денежные потоки VXX')
        await client.send_file(entity, img_path + 'inflows_VXX.png')
        time.sleep(1)
        await client.send_message(entity=entity, message='Денежные потоки SHY')
        await client.send_file(entity, img_path + 'inflows_SHY.png')
        await client.send_message(entity=entity, message='Денежные потоки TLT')
        await client.send_file(entity, img_path + 'inflows_TLT.png')
        await client.edit_message(message, 'Ежедневные денежные потоки основных ETF за месяц')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать денежные потоки? /instruction02',
                                  buttons=buttons.keyboard_a1_back)
    elif event.data == b'a1a5':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(event.input_sender, 'Общая картина 1-day performance')
        await client.send_file(entity, img_path + 'global_treemap_1d.png')
        time.sleep(1)
        await client.send_message(event.input_sender, 'Общая картина YTD performance')
        await client.send_file(entity, img_path + 'global_treemap_ytd.png')
        await client.edit_message(message, 'Мировые рынки в картах')
        await event.edit()
        await client.send_message(event.input_sender, 'Как ? /instruction02',
                                  buttons=buttons.keyboard_a1_back)
    elif event.data == b'a1a6':
        await client.send_message(event.input_sender, 'Основные макро индикаторы', buttons=buttons.keyboard_core_macro)
        await event.edit()
    elif event.data == b'a1a-1':
        await client.send_message(event.input_sender, 'Анализ рынков', buttons=buttons.keyboard_a1)
        await event.edit()

    # ============================== Анализ рынков уровень 3 =============================
    elif event.data == b'us1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        filename1 = os.path.join(img_path, 'adv.csv')
        await client.send_message(entity=entity, message='NYSE, NASDAQ')
        with open(filename1, newline='') as f1:
            data1 = csv.reader(f1, delimiter=',')
            for row1 in data1:
                r1 = str(row1).strip("['']").replace("'", "")
                await client.send_message(entity=entity, message=f'{r1}')
        await client.edit_message(message, 'Количество растущих/падающих акций и объёмы за сегодня')
        await client.send_message(event.input_sender, 'Как ? /instruction02', buttons=buttons.keyboard_us_market_back)
        await event.edit()
    elif event.data == b'us2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_file(entity, img_path + 'sectors.png')
        await client.send_message(event.input_sender, 'Волатильность и барометр жадности/страха')
        await client.send_file(entity, img_path + 'volatility.png')
        await client.edit_message(message, 'Общая картина рынка')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать графики выше? /instruction02',
                                  buttons=buttons.keyboard_us_market_back)
    elif event.data == b'us6':
        message = await client.send_message(entity=entity, message='Загрузка...')
        filename2 = os.path.join(img_path, 'sma50.csv')
        with open(filename2, newline='') as f2:
            data2 = csv.reader(f2, delimiter=',')
            for row2 in data2:
                r2 = str(row2).strip("['']").replace("'", "")
                await client.send_message(entity=entity, message=f'{r2}')
        await client.edit_message(message, 'Моментум в акциях')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать моментум? /instruction02',
                                  buttons=buttons.keyboard_us_market_back)

    elif event.data == b'us3':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(event.input_sender, 'Тепловая карта 1-day performance')
        await client.send_file(entity, img_path + 'treemap_1d.png')
        await client.send_message(event.input_sender, 'Тепловая карта YtD performance')
        await client.send_file(entity, img_path + 'treemap_ytd.png')
        await client.edit_message(message, 'Тепловые карты')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать карты? /instruction02',
                                  buttons=buttons.keyboard_us_market_back)
    elif event.data == b'us4':
        message = await client.send_message(entity=entity, message='Загрузка...')
        msg0 = 'Date 1M 2M 3M 6M 1Y 2Y 3Y 5Y 7Y 10Y 20Y 30Y'
        await client.send_message(entity=entity, message=msg0)
        filename4 = os.path.join(img_path, 'treasury_curve.csv')
        with open(filename4, newline='') as f4:
            data4 = csv.reader(f4, delimiter=',')
            for row4 in data4:
                if row4 == 0:
                    continue
            else:
                row4 = str(row4).strip("[']")
                await client.send_message(entity=entity, message=f'{row4}')

        msg01 = 'Date SP500_DIV_YIELD'
        await client.send_message(entity=entity, message=msg01)
        filename5 = os.path.join(img_path, 'spx_yield.csv')
        with open(filename5, newline='') as f5:
            data5 = csv.reader(f5, delimiter=',')
            for row5 in data5:
                if row5 < 1:
                    continue
            else:
                row5 = str(row5).strip("[']")
                await client.send_message(entity=entity, message=f'{row5}')
        await client.edit_message(message, 'Кривая доходности и дивиденды')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать кривую доходности? /instruction02',
                                  buttons=buttons.keyboard_us_market_back)
    elif event.data == b'us5':
        message = await client.send_message(entity=entity, message='Загрузка...')
        filename6 = os.path.join(img_path, 'vix_cont.csv')
        with open(filename6, newline='') as f6:
            data6 = csv.reader(f6, delimiter=',')
            for row6 in data6:
                row6 = str(row6).strip("[']")
                await client.send_message(entity=entity, message=f'{row6}')
        await client.send_file(entity, img_path + 'vix_curve.png')
        await client.edit_message(message, 'Кривая волатильности')
        await event.edit()
        await client.send_message(event.input_sender, 'Как интерпритировать кривую волатильности? /instruction02',
                                  buttons=buttons.keyboard_us_market_back)

    # ============================== Конструктор стратегий =============================
    elif event.data == b'a2a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Твой профиль риска')
        await event.edit()
        await client.send_message(event.input_sender, 'Зачем нужно знать свой профиль риска? /instruction03',
                                  buttons=buttons.keyboard_a2_back)
    elif event.data == b'a2a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Оценка/аудит портфеля')
        await event.edit()
        await client.send_message(event.input_sender, 'Зачем проводить аудит своего портфеля? /instruction04',
                                  buttons=buttons.keyboard_a2_back)
    elif event.data == b'a2a3':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, '"Парковочный" портфель без риска')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать парковочный портфель? /instruction05',
                                  buttons=buttons.keyboard_a2_back)
    elif event.data == b'a2a4':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Всепогодный портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать всепогодный портфель? /instruction06',
                                  buttons=buttons.keyboard_a2_back)
    elif event.data == b'a2a5':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Сбалансированный портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать сбалансированный портфель? /instruction07',
                                  buttons=buttons.keyboard_a2_back)
    elif event.data == b'a2a6':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Агрессивный портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать агрессивный портфель? /instruction08',
                                  buttons=buttons.keyboard_a2_back)
    elif event.data == b'a2a7':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Крипто портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Кому и когда покупать крипто портфель? /instruction09',
                                  buttons=buttons.keyboard_a2_back)
    elif event.data == b'a2a8':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Трейдинг/Дневные стратегии')
        await event.edit()
        await client.send_message(event.input_sender, 'Подходит ли вам трейдинг? /instruction10',
                                  buttons=buttons.keyboard_a2_back)
    elif event.data == b'a2a-1':
        await client.send_message(event.input_sender, 'Конструктор стратегий', buttons=buttons.keyboard_a2)
        await event.edit()

    # ============================== Калькуляторы =============================
    elif event.data == b'a3a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Рассчет количества акций для портфеля')
        await event.edit()
        await client.send_message(event.input_sender, 'Конвертация весов в количество? /instruction11',
                                  buttons=buttons.keyboard_a3_back)
    elif event.data == b'a3a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Симуляция 10 летней доходности')
        await event.edit()
        await client.send_message(event.input_sender,
                                  'Что ожидать от текущего портфеля в ближайшую декаду? /instruction12',
                                  buttons=buttons.keyboard_a3_back)
    elif event.data == b'a3a3':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Рассчет оптимального размера взносов')
        await event.edit()
        await client.send_message(event.input_sender, 'Почему взносы необходимы? /instruction13',
                                  buttons=buttons.keyboard_a3_back)
    elif event.data == b'a3a4':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Рассчет безопасного размера вывода средств')
        await event.edit()
        await client.send_message(event.input_sender, 'Сколько можно выводить средств? /instruction14',
                                  buttons=buttons.keyboard_a3_back)
    elif event.data == b'a3a5':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Сложный процент')
        await event.edit()
        await client.send_message(event.input_sender, 'Сложный процент в действии. /instruction15',
                                  buttons=buttons.keyboard_a3_back)
    elif event.data == b'a3a-1':
        await client.send_message(event.input_sender, 'Калькуляторы', buttons=buttons.keyboard_a3)
        await event.edit()

    # ============================== Управление =============================
    elif event.data == b'a4a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Маркетплейс управляющих')
        await event.edit()
        await client.send_message(event.input_sender, 'Все об управлени активами. /instruction16',
                                  buttons=buttons.keyboard_a4_back)
    elif event.data == b'a4a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Стать управляющим')
        await event.edit()
        await client.send_message(event.input_sender, 'Стать управляющим',
                                  buttons=buttons.keyboard_a4_back)
    elif event.data == b'a4a-1':
        await client.send_message(event.input_sender, 'Управление', buttons=buttons.keyboard_a4)
        await event.edit()

    # ============================== Инструкции =============================
    elif event.data == b'a5a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Как ... /instruction01')
        await event.edit()
        await client.send_message(event.input_sender, 'Как ... /instruction01',
                                  buttons=buttons.keyboard_a5_back)
    elif event.data == b'a5a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Что ... /instruction02')
        await event.edit()
        await client.send_message(event.input_sender, 'Что ... /instruction02',
                                  buttons=buttons.keyboard_a5_back)
    elif event.data == b'a5a-1':
        await client.send_message(event.input_sender, 'Инструкции', buttons=buttons.keyboard_a5)
        await event.edit()

    # ============================== Образовательные программы =============================
    elif event.data == b'a6a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Основы инвестирования')
        await event.edit()
        await client.send_message(event.input_sender, 'Основы инвестирования /instruction20',
                                  buttons=buttons.keyboard_a6_back)
    elif event.data == b'a6a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Как собрать свой первый портфель')
        await event.edit()
        await client.send_message(event.input_sender, 'Как собрать свой первый портфель /instruction21',
                                  buttons=buttons.keyboard_a6_back)
    elif event.data == b'a6a3':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Профессиональные решения')
        await event.edit()
        await client.send_message(event.input_sender, 'Профессиональные решения /instruction22',
                                  buttons=buttons.keyboard_a6_back)
    elif event.data == b'a6a-1':
        await client.send_message(event.input_sender, 'Образование', buttons=buttons.keyboard_a6)
        await event.edit()

    # ============================== Налоги =============================
    elif event.data == b'a7a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Оптимизация налогов')
        await event.edit()
        await client.send_message(event.input_sender, 'Оптимизация налогов /instruction30',
                                  buttons=buttons.keyboard_a7_back)
    elif event.data == b'a7a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Подготовка налоговых деклараций')
        await event.edit()
        await client.send_message(event.input_sender, 'Подготовка налоговых деклараций /instruction30',
                                  buttons=buttons.keyboard_a7_back)
    elif event.data == b'a7a-1':
        await client.send_message(event.input_sender, 'Налоги', buttons=buttons.keyboard_a7)
        await event.edit()

    # ============================== Агрегатор новостей =============================
    elif event.data == b'a8a1':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Поставщики новостей')
        await event.edit()
        await client.send_message(event.input_sender, 'Поставщики новостей',
                                  buttons=buttons.keyboard_a8_back)
    elif event.data == b'a8a2':
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Тикеры')
        await event.edit()
        await client.send_message(event.input_sender, 'Тикеры',
                                  buttons=buttons.keyboard_a8_back)
    elif event.data == b'a8a-1':
        await client.send_message(event.input_sender, 'Агрегатор новостей', buttons=buttons.keyboard_a8)
        await event.edit()

    # elif event.data == b'a4a1':
    #     message = await client.send_message(entity=entity, message='Loading...')
    #     await client.send_file(entity, img_path + 'us_index.png')
    #     await client.edit_message(message, 'Ипсилон AI US Index')
    #     await event.edit()
    # elif event.data == b'a4a2':
    #     message = await client.send_message(entity=entity, message='Loading...')
    #     await client.send_file(entity, img_path + 'world_index.png')
    #     await client.edit_message(message, 'Ипсилон AI WORLD Index')
    #     await event.edit()

    # ============================== Основные макро данные =============================
    elif event.data == b'cm1':
        await client.send_message(entity=entity, message='Interest Rates')
        await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
        filename = os.path.join(yahoo_path, 'economic_data.csv')
        with open(filename, newline='') as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                if row[0] == 'Interest Rate':
                    new_row = ',  '.join(row)
                    await client.send_message(entity=entity, message=f'{new_row}')
        await event.edit()
        await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
    elif event.data == b'cm2':
        await client.send_message(entity=entity, message='Interest Rates')
        await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
        filename = os.path.join(yahoo_path, 'economic_data.csv')
        with open(filename, newline='') as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                if row[0] == 'Inflation Rate':
                    new_row = ',  '.join(row)
                    await client.send_message(entity=entity, message=f'{new_row}')
        await event.edit()
        await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
    elif event.data == b'cm3':
        await client.send_message(entity=entity, message='Interest Rates')
        await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
        filename = os.path.join(yahoo_path, 'economic_data.csv')
        with open(filename, newline='') as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                if row[0] == 'Unemployment Rate':
                    new_row = ',  '.join(row)
                    await client.send_message(entity=entity, message=f'{new_row}')
        await event.edit()
        await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
    elif event.data == b'cm4':
        await client.send_message(entity=entity, message='Interest Rates')
        await client.send_message(entity=entity, message='Data, Country, Last, Previous, Reference, Unit')
        filename = os.path.join(yahoo_path, 'economic_data.csv')
        with open(filename, newline='') as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                if row[0] == 'Composite PMI':
                    new_row = ',  '.join(row)
                    await client.send_message(entity=entity, message=f'{new_row}')
        await event.edit()
        await client.send_message(event.input_sender, '________________________', buttons=buttons.keyboard_core_macro)
    elif event.data == b'cm-1':
        await client.send_message(event.input_sender, 'Назад', buttons=buttons.keyboard_core_macro_back)
        await event.edit()
    elif event.data == b'cm-2':
        await client.send_message(event.input_sender, 'Назад', buttons=buttons.keyboard_a1)
        await event.edit()
    elif event.data == b'cm-3':
        await client.send_message(event.input_sender, 'Назад', buttons=buttons.keyboard_us_market)
        await event.edit()

    elif event.data == b'z2':
        await client.send_message(event.input_sender,
                                  'Вы можете попросить друга запустить бота и получить бесплатную'
                                  ' подписку. '
                                  'Проще всего это сделать через групповые чаты' + '\n' +
                                  f'[https://t.me/UpsilonBot?start={sender_id}]'
                                  f'(https://t.me/UpsilonBot?start={sender_id})')
        # TODO Изменить на оригинал
        await event.edit()

    # ============================== Subscriptions =============================
    elif event.data == b'z1':
        await client.send_message(event.input_sender, 'Уровень подписок', buttons=buttons.keyboard_core_subscriptions)
        await event.edit()
    elif event.data == b'kcs0':
        await client.send_file(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_COMPARE_ID].get_img_path())
        await event.edit()
    elif event.data == b'kcs1':
        await client.send_file(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_START_ID].get_img_path())
        await client.send_message(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_START_ID].get_describe(),
                                  buttons=buttons.keyboard_subscription_start)
        await event.edit()
    elif event.data == b'kcs2':
        await client.send_file(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_BASE_ID].get_img_path())
        await client.send_message(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_BASE_ID].get_describe(),
                                  buttons=buttons.keyboard_subscription_base)
    elif event.data == b'kcs3':
        await client.send_file(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_ADVANCED_ID].get_img_path())
        await client.send_message(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_ADVANCED_ID].get_describe(),
                                  buttons=buttons.keyboard_subscription_advanced)
    elif event.data == b'kcs4':
        await client.send_file(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_PROFESSIONAL_ID].get_img_path())
        await client.send_message(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_PROFESSIONAL_ID].get_describe(),
                                  buttons=buttons.keyboard_subscription_professional)
    elif event.data == b'kcs-1':
        await menu.profile_menu(event, client, engine)
    #   TODO добавить описание подписок
    #   TODO добавить таблицу сравнения подписок
    elif event.data == b'kss1' or event.data == b'kss2' or event.data == b'kss3' or event.data == b'kss4':
        global PAYMENT_AGGREGATOR
        if PAYMENT_AGGREGATOR is None:
            PAYMENT_AGGREGATOR = PaymentAgregator()
            PAYMENT_AGGREGATOR.creator('Free Kassa')
        aggregator_status = None
        global PAYMENT_AGGREGATOR_TIMER
        if PAYMENT_AGGREGATOR_TIMER is not None:
            delta = time.time() - PAYMENT_AGGREGATOR_TIMER
            if delta >= 10:
                aggregator_status = PAYMENT_AGGREGATOR.get_status()
            else:
                time.sleep(10 - delta)
                aggregator_status = PAYMENT_AGGREGATOR.get_status()
        else:
            PAYMENT_AGGREGATOR_TIMER = time.time()
            aggregator_status = PAYMENT_AGGREGATOR.get_status()
        # print(aggregator_status)
        if aggregator_status == 'error':
            # print("Error description:" + PAYMENT_AGGREGATOR.get_last_error())
            await client.send_message(event.input_sender, 'Упс. Что-то пошло не так.',
                                      buttons=buttons.keyboard_subscription_start)
            await event.edit()
        else:
            # print("user_id=" + str(sender_id.user_id))
            order_id = str(uuid.uuid4()).replace('-', '')
            print("OrderId:" + order_id)
            summa = ""
            kbd_label = ""
            if event.data == b'kss1':
                summa = str(shared.SUBSCRIBES[shared.TARIFF_START_ID].get_cost())
                kbd_label = "Оплатить ($" + str(shared.SUBSCRIBES[shared.TARIFF_START_ID].get_cost()) + ')'
            elif event.data == b'kss2':
                summa = str(shared.SUBSCRIBES[shared.TARIFF_BASE_ID].get_cost())
                kbd_label = "Оплатить ($" + str(shared.SUBSCRIBES[shared.TARIFF_BASE_ID].get_cost()) + ')'
            elif event.data == b'kss3':
                summa = str(shared.SUBSCRIBES[shared.TARIFF_ADVANCED_ID].get_cost())
                kbd_label = "Оплатить ($" + str(shared.SUBSCRIBES[shared.TARIFF_ADVANCED_ID].get_cost()) + ')'
            elif event.data == b'kss2':
                summa = str(shared.SUBSCRIBES[shared.TARIFF_PROFESSIONAL_ID].get_cost())
                kbd_label = "Оплатить ($" + str(shared.SUBSCRIBES[shared.TARIFF_PROFESSIONAL_ID].get_cost()) + ')'

            print("Summa:" + summa)
            payment_link = PAYMENT_AGGREGATOR.get_payment_link(order_id, summa)
            print(payment_link)
            kbd_payment_button = buttons.generate_payment_button(kbd_label, payment_link)

            paymsg = await client.send_message(event.input_sender,
                                               'Для оплаты тарифа ' \
                                               + shared.SUBSCRIBES[shared.TARIFF_START_ID].get_name() \
                                               + 'нажмите кнопку Оплатить\n'
                                                 '(Инструкция по оплате [тут](https://telegra.ph/Rrrtt-10-13)! )',
                                               link_preview=True,
                                               buttons=kbd_payment_button)
            await event.edit()
            msg_id = utils.get_message_id(paymsg)
            shared.ORDER_MAP[order_id] = (sender_id, msg_id)
            dt = datetime.now()
            dt_int = shared.datetime2int(dt)
            await sql.insert_into_payment_message(order_id, sender_id, msg_id, dt_int, engine)
