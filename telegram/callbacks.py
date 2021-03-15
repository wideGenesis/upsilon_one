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
from project_shared import *
from telegram import instructions as ins
from quotes.stock_quotes_news import fin_news
from quotes.parsers import nyse_nasdaq_stat
from messages.message import *
from telethon.tl.types import InputMediaPoll, Poll, PollAnswer, DocumentAttributeFilename, DocumentAttributeVideo

PAYMENT_AGGREGATOR = None
PAYMENT_AGGREGATOR_TIMER = None


# ============================== Callbacks =======================

async def callback_handler(event, client, img_path=None, yahoo_path=None, engine=None):
    sender_id = event.original_update.user_id
    entity = await client.get_input_entity(sender_id)
    chat = await event.get_chat()
    old_msg_id = await shared.get_old_msg_id(sender_id)

    # ============================== Главное меню 1 уровень=============================
    if event.data == b'a1':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Анализ рынков', buttons=buttons.keyboard_a1)
        else:
            msg = await client.send_message(event.input_sender, 'Анализ рынков', buttons=buttons.keyboard_a1)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'a2':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Мой портфель\n'
                                                                      'Как купить портфель? - /instruction27\n'
                                                                      'Минимальный депозит - /mindepo',
                                      buttons=buttons.keyboard_portfolio)
        else:
            msg = await client.edit_message(event.input_sender, old_msg_id, 'Мой портфель\n'
                                                                            'Как купить портфель? - /instruction27\n'
                                                                            'Минимальный депозит - /mindepo',
                                            buttons=buttons.keyboard_portfolio)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'a3':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Скринер акций',
                                      buttons=buttons.keyboard_screener)
        else:
            msg = await client.send_message(event.input_sender, 'Скринер акций', buttons=buttons.keyboard_screener)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'a5':
        await event.edit()
        msg = await client.send_message(event.input_sender, ins.instructions_main, buttons=buttons.keyboard_a5)
        await shared.delete_old_message(client, sender_id)

    elif event.data == b'a8':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Лента новостей', buttons=buttons.keyboard_a8)
        else:
            msg = await client.send_message(event.input_sender, 'Лента новостей', buttons=buttons.keyboard_a8)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'main':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Главное меню', buttons=buttons.keyboard_0)
        else:
            menu_msg = await client.send_message(event.input_sender, 'Главное меню', buttons=buttons.keyboard_0)
            await shared.delete_old_message(client, sender_id)
            await shared.save_old_message(sender_id, menu_msg)

    # ============================== Анализ рынков 2 уровень=============================
    elif event.data == b'a1a1':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Анализ США',
                                      buttons=buttons.keyboard_us_analysis)
        else:
            msg = await client.send_message(event.input_sender, 'Анализ США', buttons=buttons.keyboard_us_analysis)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'us5x':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Подробный анализ',
                                      buttons=buttons.keyboard_us_market)
        else:
            msg = await client.send_message(event.input_sender, 'Подробный анализ',
                                            buttons=buttons.keyboard_us_market)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'us5z':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_file(entity, img_path + 'sectors.png')
        await client.send_message(event.input_sender, 'Обзор рынка США\n'
                                                      '/instruction02\n'
                                                      '/instruction05')
        await client.send_file(entity, img_path + 'treemap_1d.png')
        await client.send_message(event.input_sender, 'Тепловая карта акций США\n'
                                                      '/instruction04',
                                  buttons=buttons.keyboard_us_analysis_back)

    elif event.data == b'a1a2':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_file(entity, img_path + 'crypto.png')
        await client.send_message(event.input_sender, 'Обзор BTCUSD и ETHUSD\n'
                                                      '/instruction07')
        await client.send_file(entity, img_path + 'coins_treemap.png')
        await client.send_message(event.input_sender, 'Тепловая карта основных криптовалют\n'
                                                      '/instruction04',
                                  buttons=buttons.keyboard_a1_back)
    elif event.data == b'a1a3':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_file(entity, img_path + 'rtsi.png')
        await client.send_message(event.input_sender, 'Обзор рынка РФ\n'
                                                      '/instruction08')
        await client.send_file(entity, img_path + 'moex_map.png')
        await client.send_message(event.input_sender, 'Тепловая карта акций РФ\n'
                                                      '/instruction04',
                                  buttons=buttons.keyboard_a1_back)
    elif event.data == b'a1a5':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_file(entity, img_path + 'world.png')
        await client.send_message(event.input_sender, 'Обзор мировых рынков\n'
                                                      '/instruction04')
        await client.send_file(entity, img_path + 'global_treemap_1d.png')
        await client.send_message(event.input_sender, 'Тепловая карта мировых акций\n'
                                                      '/instruction04',
                                  buttons=buttons.keyboard_a1_back)

    # elif event.data == b'a1a4':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.send_message(entity=entity, message='Денежные потоки в USD')
    #     await client.send_message(entity=entity, message='Денежные потоки SPY')
    #     await client.send_file(entity, img_path + 'inflows_SPY.png')
    #     await client.send_message(entity=entity, message='Денежные потоки QQQ')
    #     await client.send_file(entity, img_path + 'inflows_QQQ.png')
    #     await client.send_message(entity=entity, message='Денежные потоки VTI')
    #     await client.send_file(entity, img_path + 'inflows_VTI.png')
    #     time.sleep(1)
    #     await client.send_message(entity=entity, message='Денежные потоки VEA')
    #     await client.send_file(entity, img_path + 'inflows_VEA.png')
    #     await client.send_message(entity=entity, message='Денежные потоки VWO')
    #     await client.send_file(entity, img_path + 'inflows_VWO.png')
    #     await client.send_message(entity=entity, message='Денежные потоки LQD')
    #     await client.send_file(entity, img_path + 'inflows_LQD.png')
    #     await client.send_message(entity=entity, message='Денежные потоки VXX')
    #     await client.send_file(entity, img_path + 'inflows_VXX.png')
    #     time.sleep(1)
    #     await client.send_message(entity=entity, message='Денежные потоки SHY')
    #     await client.send_file(entity, img_path + 'inflows_SHY.png')
    #     await client.send_message(entity=entity, message='Денежные потоки TLT')
    #     await client.send_file(entity, img_path + 'inflows_TLT.png')
    #     await client.edit_message(message, 'Ежедневные денежные потоки основных ETF за месяц')
    #     await client.send_message(event.input_sender, 'Как интерпретировать денежные потоки? \n'
    #                                                   '/instruction09',
    #                               buttons=buttons.keyboard_a1_back)

    elif event.data == b'a1a6':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Основные макро индикаторы',
                                      buttons=buttons.keyboard_core_macro)
        else:
            msg = await client.send_message(event.input_sender, 'Основные макро индикаторы',
                                            buttons=buttons.keyboard_core_macro)
            await shared.save_old_message(sender_id, msg)
    elif event.data == b'a1a-1':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Анализ рынков', buttons=buttons.keyboard_a1)
        await shared.save_old_message(sender_id, msg)

    # ============================== Анализ рынков уровень 3 =============================
    elif event.data == b'us1':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        msg = nyse_nasdaq_stat()
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.send_message(entity=entity, message=msg)

        await client.edit_message(message, 'Количество растущих/падающих акций и объёмы за сегодня')
        await client.send_message(event.input_sender, 'Как интепритировать статистику торгов? \n'
                                                      '/instruction01',
                                  buttons=buttons.keyboard_us_market_back)
    # elif event.data == b'us2':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.send_file(entity, img_path + 'sectors.png')
    #     await client.edit_message(message, 'Подробный анализ')
    #     await client.send_message(event.input_sender, 'Как интерпретировать графики выше? \n'
    #                                                   '/instruction02\n/instruction05\n/instruction06',
    #                               buttons=buttons.keyboard_us_market_back)
    elif event.data == b'us6':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        filename2 = os.path.join(img_path, 'sma50.csv')
        with open(filename2, newline='') as f2:
            data2 = csv.reader(f2, delimiter=',')
            for row2 in data2:
                r2 = str(row2).strip("['']").replace("'", "")
                await client.send_message(entity=entity, message=f'{r2}')
        await client.edit_message(message, 'Моментум в акциях')
        await client.send_message(event.input_sender, 'Как интерпретировать моментум? \n'
                                                      '/instruction03',
                                  buttons=buttons.keyboard_us_market_back)

    # elif event.data == b'us3':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.send_message(event.input_sender, 'Тепловая карта 1-day performance')
    #     await client.send_file(entity, img_path + 'treemap_1d.png')
    #     await client.send_message(event.input_sender, 'Тепловая карта YtD performance')
    #     await client.send_file(entity, img_path + 'treemap_ytd.png')
    #     await client.edit_message(message, 'Тепловые карты')
    #     await client.send_message(event.input_sender, 'Как интерпретировать тепловые карты? \n'
    #                                                   '/instruction04',
    #                               buttons=buttons.keyboard_us_market_back)
    # elif event.data == b'us4':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     filename4 = os.path.join(img_path, 'treasury_curve.csv')
    #     with open(filename4, newline='') as f4:
    #         data4 = csv.reader(f4, delimiter=',')
    #         for row4 in data4:
    #             row4 = str(row4).replace("'", "").strip("[]")
    #             await client.send_message(entity=entity, message=f'{row4}')
    #
    #     msg01 = 'SP500 DIV YIELD'
    #     await client.send_message(entity=entity, message=msg01)
    #     filename5 = os.path.join(img_path, 'spx_yield.csv')
    #     temp = []
    #     with open(filename5, newline='') as f5:
    #         data5 = csv.reader(f5, delimiter=' ')
    #         for row5 in data5:
    #             temp.append(row5)
    #     msg0 = str(temp[-1]).strip("[]")
    #     msg0 = msg0.split(',')
    #     await client.send_message(entity=entity, message=f'{msg0[0]} {msg0[-1]}')
    #     await client.edit_message(message, 'Кривая доходности и дивиденды')
    #     await client.send_message(event.input_sender, 'Как интерпретировать кривую доходности? /instruction05',
    #                               buttons=buttons.keyboard_us_market_back)
    elif event.data == b'us5':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        filename6 = os.path.join(img_path, 'vix_cont.csv')
        with open(filename6, newline='') as f6:
            data6 = csv.reader(f6, delimiter=',')
            for row6 in data6:
                row6 = str(row6).strip("[']")
                await client.send_message(entity=entity, message=f'{row6}')
        await client.send_file(entity, img_path + 'vix_curve.png')
        await client.edit_message(message, 'Кривая волатильности')
        await client.send_message(event.input_sender, 'Как интерпретировать кривую волатильности? /instruction06',
                                  buttons=buttons.keyboard_us_market_back)

    elif event.data == b'us7':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Ключевые статистики акций компании')
        await client.send_message(entity=entity, message=ins.instruction21)
        await client.send_message(event.input_sender, 'Как интерпретировать ключевые статистики? \n'
                                                      '/instruction22',
                                  buttons=buttons.keyboard_us_market_back)

    # ============================== Конструктор стратегий =============================
    # elif event.data == b'a2a1':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.edit_message(message, 'Твой профиль риска')
    #     await client.send_message(event.input_sender, 'Зачем нужно знать свой профиль риска? /instruction03',
    #                               buttons=buttons.keyboard_a2_back)
    # elif event.data == b'a2a2':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.edit_message(message, 'Оценка/аудит портфеля')
    #     await client.send_message(event.input_sender, 'Зачем проводить аудит своего портфеля? /instruction04',
    #                               buttons=buttons.keyboard_a2_back)
    elif event.data == b'hist_parking':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Парковочный портфель')

        await client.send_message(event.input_sender, 'Подробная статистика стратегии',
                                  file=STATS_PATH + 'parking.pdf')
        await client.send_message(event.input_sender, 'Симуляция доходности портфеля на 10 лет',
                                  file=STATS_PATH + 'parking.png')
        await client.send_message(event.input_sender, 'Как интерпретировать результаты симуляций Монте-Карло?\n'
                                                      '/instruction19',
                                  file=STATS_PATH + 'parking2.png')
        await client.send_message(event.input_sender, 'Кому и когда покупать парковочный портфель?\n'
                                                      '/instruction14',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'a2a4':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Всепогодный портфель')
        await client.send_message(event.input_sender, 'Текущая структура портфеля')
        await client.send_file(entity, CHARTER_IMAGES_PATH + 'allweather_portfolio_pie.png')
        await client.send_message(event.input_sender, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'allweather.pdf')
        await client.send_message(event.input_sender, 'Симуляция доходности портфеля на 10 лет \n '
                                                      'Как интерпретировать результаты симуляций Монте-Карло?'
                                                      ' - /instruction19')
        await client.send_file(entity, STATS_PATH + 'allweather.png')
        await client.send_file(entity, STATS_PATH + 'allweather2.png')
        await client.send_message(event.input_sender, 'Кому и когда покупать всепогодный портфель? \n'
                                                      '/instruction15 \n End of Day График - /chart_allweather',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'a2a5':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Сбалансированный портфель')
        await client.send_message(event.input_sender, 'Текущая структура портфеля')
        await client.send_file(entity, CHARTER_IMAGES_PATH + 'balanced_portfolio_pie.png')
        await client.send_message(event.input_sender, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'balanced.pdf')
        await client.send_message(event.input_sender, 'Симуляция доходности портфеля на 10 лет \n '
                                                      'Как интерпретировать результаты симуляций Монте-Карло?'
                                                      ' - /instruction19')
        await client.send_file(entity, STATS_PATH + 'balanced.png')
        await client.send_file(entity, STATS_PATH + 'balanced2.png')
        await client.send_message(event.input_sender, 'Кому и когда покупать сбалансированный портфель? \n'
                                                      '/instruction16 \n End of Day График - /chart_balanced',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'a2a6':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Агрессивный портфель')
        await client.send_message(event.input_sender, 'Текущая структура портфеля')
        await client.send_file(entity, CHARTER_IMAGES_PATH + 'aggressive_portfolio_pie.png')
        await client.send_message(event.input_sender, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'aggressive.pdf')
        await client.send_message(event.input_sender, 'Симуляция доходности портфеля на 10 лет \n '
                                                      'Как интерпретировать результаты симуляций Монте-Карло?'
                                                      ' - /instruction19')
        await client.send_file(entity, STATS_PATH + 'aggressive.png')
        await client.send_file(entity, STATS_PATH + 'aggressive2.png')
        await client.send_message(event.input_sender, 'Кому и когда покупать агрессивный портфель? \n'
                                                      '/instruction17 \n End of Day График - /chart_aggressive',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'a2a7':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Плечевой портфель')
        await client.send_message(event.input_sender, 'Текущая структура портфеля')
        await client.send_file(entity, CHARTER_IMAGES_PATH + 'leveraged_portfolio_pie.png')
        await client.send_message(event.input_sender, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'leveraged.pdf')
        await client.send_message(event.input_sender, 'Симуляция доходности портфеля на 10 лет \n '
                                                      'Как интерпретировать результаты симуляций Монте-Карло?'
                                                      ' - /instruction19')
        await client.send_file(entity, STATS_PATH + 'leveraged.png')
        await client.send_file(entity, STATS_PATH + 'leveraged2.png')
        await client.send_message(event.input_sender, 'Кому и когда покупать плечевой портфель? \n'
                                                      '/instruction18 \n End of Day График - /chart_leveraged',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'a2a9':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Elastic Strategy - портфель только из акций')
        await client.send_message(event.input_sender, 'Текущая структура портфеля')
        await client.send_file(entity, CHARTER_IMAGES_PATH + 'elastic_portfolio_pie.png')
        await client.send_message(event.input_sender, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'elastic.pdf')
        await client.send_message(event.input_sender, 'Симуляция доходности портфеля на 10 лет \n '
                                                      'Как интерпретировать результаты симуляций Монте-Карло?'
                                                      ' - /instruction19')
        await client.send_file(entity, STATS_PATH + 'elastic.png')
        await client.send_file(entity, STATS_PATH + 'elastic2.png')
        await client.send_message(event.input_sender, 'Кому и когда покупать Elastic портфель? \n'
                                                      '/instruction23 \n End of Day График - /chart_elastic',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'a2a10':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Yolo Strategy - портфель только из акций, торгуемых на spbexchange. '
                                           'Доступен для клиентов Сбер, Тинькофф, Альфа-банк, ВТБ')
        await client.send_message(event.input_sender, 'Текущая структура портфеля')
        await client.send_file(entity, CHARTER_IMAGES_PATH + 'yolo_portfolio_pie.png')
        await client.send_message(event.input_sender, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'yolo.pdf')

        await client.send_message(event.input_sender, 'Кому и когда покупать Yolo портфель? \n'
                                                      '/instruction24 \n End of Day График - /chart_yolo',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'mp3':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Исторические тесты', buttons=buttons.keyboard_historical_tests)
        else:
            msg = await client.send_message(event.input_sender, 'Исторические тесты', buttons=buttons.keyboard_historical_tests)
            await shared.save_old_message(sender_id, msg)

    # ============================== Управление =============================
    # elif event.data == b'a4a1':
    #     risk_profile = sql.risk_data_lookup(event.original_update.peer.user_id, engine)
    #     if risk_profile:
    #         await event.edit()
    #         await client.send_message(event.input_sender, 'Доступные портфели', buttons=buttons.keyboard_managed_strategies)
    #     else:
    #
    #         message = await client.send_message(entity=entity, message='Загрузка...')
    #         await client.edit_message(message, ' Для доступа к портфелям управляющих необходимо '
    #                                            'определить ваш уровень терпимости к риску')
    #         await client.send_message(event.input_sender, 'Выберите наиболее подходящий вариант для вас \n \n'
    #                                   + ins.instruction25, buttons=buttons.keyboard_risk_profile)

    elif event.data == b'manager_registration':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Регистрация управляющего')
        await client.send_message(event.input_sender, ins.managers_form,
                                  buttons=buttons.keyboard_info_back)

    elif event.data == b'advertisement':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Предложения и реклама')
        await client.send_message(event.input_sender, ins.instruction29,
                                  buttons=buttons.keyboard_info_back)

    elif event.data == b'bug_report':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Сообщить об ошибке')
        await client.send_message(event.input_sender, ins.instruction30,
                                  buttons=buttons.keyboard_info_back)

    elif event.data == b'brokers_compare':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Сравнение брокеров')
        await client.send_message(event.input_sender, ins.brokers,
                                  buttons=buttons.keyboard_info_back)

    # elif event.data == b'sac1':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.edit_message(message, 'Подробная статистика стратегии')
    #     await client.send_file(entity, STATS_PATH + 'sac_parking.pdf')
    #     await client.send_message(event.input_sender, 'О доверительном управлении \n'
    #                                                   '/instruction26',
    #                               buttons=buttons.keyboard_managed_strategies)
    #
    # elif event.data == b'sac2':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.edit_message(message, 'Подробная статистика стратегии')
    #     await client.send_file(entity, STATS_PATH + 'sac_balanced.pdf')
    #     await client.send_message(event.input_sender, 'О доверительном управлении \n'
    #                                                   '/instruction26',
    #                               buttons=buttons.keyboard_managed_strategies)
    #
    # elif event.data == b'sac3':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.edit_message(message, 'Подробная статистика стратегии')
    #     await client.send_file(entity, STATS_PATH + 'sac_growth.pdf')
    #     await client.send_message(event.input_sender, 'О доверительном управлении \n'
    #                                                   '/instruction26',
    #                               buttons=buttons.keyboard_managed_strategies)
    # ============================== Презентация =============================
    elif event.data == b'forw2':
        await event.edit()
        await client.send_message(entity, ins.hello_2, file=f'{PROJECT_HOME_DIR}/html/hello_2.jpg',
                                  buttons=buttons.keyboard_forw3)
    elif event.data == b'forw3':
        await event.edit()
        await client.send_message(entity, ins.hello_3, file=f'{PROJECT_HOME_DIR}/html/hello_3.jpg',
                                  buttons=buttons.keyboard_forw4)
    elif event.data == b'forw4':
        await event.edit()
        await client.send_message(entity, ins.hello_4, file=f'{PROJECT_HOME_DIR}/html/hello_5.jpg',
                                  buttons=buttons.keyboard_forw7)
    # elif event.data == b'forw5':
    #     await event.edit()
    #     await client.send_message(entity, ins.hello_5, file=f'{PROJECT_HOME_DIR}/html/hello_5.jpg',
    #                               buttons=buttons.keyboard_forw6)
    # elif event.data == b'forw6':
    #     await event.edit()
    #     await client.send_message(entity, ins.hello_6, file=f'{PROJECT_HOME_DIR}/html/hello_6.jpg',
    #                               buttons=buttons.keyboard_forw7)
    elif event.data == b'forw7':
        await event.edit()
        await client.send_message(entity, ins.hello_7, file=f'{PROJECT_HOME_DIR}/html/hello_7.jpg',
                                  buttons=buttons.keyboard_forw7a)
    elif event.data == b'forw7a':
        await event.edit()
        await client.send_message(entity, ins.hello_7a, file=f'{PROJECT_HOME_DIR}/html/hello_6.jpg',
                                  buttons=buttons.keyboard_forw8)
    elif event.data == b'forw8':
        await event.edit()
        await client.send_message(entity=entity, message='__Какой путь инвестиций правильный для тебя?__',
                                  buttons=buttons.keyboard_start)
        await client.send_message(entity, ins.hello_8, file=f'{PROJECT_HOME_DIR}/html/hello_8.jpg',
                                  buttons=buttons.keyboard_forw9)
    elif event.data == b'forw9':
        await event.edit()
        await send_next_profiler_question(client, sender_id, 0)

    # ============================== Образовательные программы =============================
    # elif event.data == b'a6a1':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.edit_message(message, 'Основы инвестирования')
    #     await client.send_message(event.input_sender, 'Основы инвестирования /instruction20',
    #                               buttons=buttons.keyboard_a6_back)
    # elif event.data == b'a6a2':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.edit_message(message, 'Как собрать свой первый портфель')
    #     await client.send_message(event.input_sender, 'Как собрать свой первый портфель /instruction21',
    #                               buttons=buttons.keyboard_a6_back)
    # elif event.data == b'a6a3':
    #     await event.edit()
    #     message = await client.send_message(entity=entity, message='Загрузка...')
    #     await client.edit_message(message, 'Профессиональные решения')
    #     await client.send_message(event.input_sender, 'Профессиональные решения /instruction22',
    #                               buttons=buttons.keyboard_a6_back)
    # elif event.data == b'a6a-1':
    #     await event.edit()
    #     await client.send_message(event.input_sender, 'Образование', buttons=buttons.keyboard_a6)

    # ============================== Агрегатор новостей =============================
    elif event.data == b'a9a1':
        if old_msg_id is not None:
            await client.edit_message(entity, old_msg_id, 'Последние новости')
            shared.pop_old_msg_id(sender_id)
        else:
            await client.send_message(entity, 'Последние новости')
        msg1 = fin_news(blogs=False)
        await client.send_message(entity, msg1, buttons=buttons.keyboard_a8_back)

    elif event.data == b'a9a2':
        if old_msg_id is not None:
            await client.edit_message(entity, old_msg_id, 'Последние статьи в блогах')
            shared.pop_old_msg_id(sender_id)
        else:
            await client.send_message(entity, 'Последние статьи в блогах')
        msg2 = fin_news(blogs=True)
        await client.send_message(entity, msg2, buttons=buttons.keyboard_a8_back)

    elif event.data == b'a9a3':
        msg3 = fin_news(blogs=True)
        message = await client.send_message(entity=entity, message='Последние новости компании')
        await client.send_message(entity=entity, message=ins.instruction20, buttons=buttons.keyboard_a8_back)

    elif event.data == b'a8a-1':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Агрегатор новостей', buttons=buttons.keyboard_a8)
        await shared.save_old_message(sender_id, msg)

    # ============================== Основные макро данные =============================
    elif event.data == b'cm1':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(entity=entity, message='Прогноз процентной ставки в США')
        await client.send_file(entity, IMAGES_OUT_PATH + 'Interest Rate.png')
        await client.send_message(event.input_sender, 'Процентная ставка \n /instruction10',
                                  buttons=buttons.keyboard_core_macro_back)
    elif event.data == b'cm2':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(entity=entity, message='Прогноз уровня инфляции в США')
        await client.send_file(entity, IMAGES_OUT_PATH + 'Inflation Rate.png')
        await client.send_message(event.input_sender, 'Уровень инфляции \n /instruction11',
                                  buttons=buttons.keyboard_core_macro_back)
    elif event.data == b'cm3':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(entity=entity, message='Прогноз уровня безработицы в США')
        await client.send_file(entity, IMAGES_OUT_PATH + 'Unemployment Rate.png')
        await client.send_message(event.input_sender, 'Уровень безработицы \n /instruction13',
                                  buttons=buttons.keyboard_core_macro_back)
    elif event.data == b'cm4':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(entity=entity, message='Прогноз индекса PMI в США')
        await client.send_file(entity, IMAGES_OUT_PATH + 'Composite PMI.png')
        await client.send_message(event.input_sender, 'Композитный индекс менеджеров по закупкам \n /instruction12',
                                  buttons=buttons.keyboard_core_macro_back)
    elif event.data == b'cm-1':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Основные макро индикаторы',
                                        buttons=buttons.keyboard_core_macro)
        await shared.save_old_message(sender_id, msg)

    elif event.data == b'cm-2':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Анализ США', buttons=buttons.keyboard_a1)
        else:
            msg = await client.send_message(event.input_sender, 'Анализ США', buttons=buttons.keyboard_a1)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'cm-3':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Подробный анализ',
                                      buttons=buttons.keyboard_us_market)
        else:
            msg = await client.send_message(event.input_sender, 'Подробный анализ', buttons=buttons.keyboard_us_market)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'cm-4':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Анализ США',
                                      buttons=buttons.keyboard_us_analysis)
        else:
            msg = await client.send_message(event.input_sender, 'Анализ США', buttons=buttons.keyboard_us_analysis)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'cm-5':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Мой портфель\n'
                                                                      'Как купить портфель? - /instruction27\n'
                                                                      'Минимальный депозит - /mindepo',
                                      buttons=buttons.keyboard_portfolio)
        else:
            msg = await client.send_message(event.input_sender, 'Мой портфель\n'
                                                                'Как купить портфель? - /instruction27\n'
                                                                'Минимальный депозит - /mindepo',
                                            buttons=buttons.keyboard_portfolio)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'cm-51':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Исторические тесты', buttons=buttons.keyboard_historical_tests)
        await shared.save_old_message(sender_id, msg)

    # elif event.data == b'cm-6':
    #     await event.edit()

    #     msg = await client.send_message(event.input_sender, 'Сотрудничество', buttons=buttons.keyboard_relations)
    #     await shared.save_old_message(sender_id, msg)

    elif event.data == b'z2':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id,
                                      'Вы можете попросить друга запустить бота и получить бесплатную'
                                      ' подписку. '
                                      'Проще всего это сделать через групповые чаты' + '\n' +
                                      f'[https://t.me/UpsilonBot?start={sender_id}]'
                                      f'(https://t.me/UpsilonBot?start={sender_id})',
                                      buttons=buttons.keyboard_friend_back)
        else:
            msg = await client.send_message(event.input_sender,
                                            'Вы можете попросить друга запустить бота и получить бесплатную'
                                            ' подписку. '
                                            'Проще всего это сделать через групповые чаты' + '\n' +
                                            f'[https://t.me/UpsilonBot?start={sender_id}]'
                                            f'(https://t.me/UpsilonBot?start={sender_id})',
                                            buttons=buttons.keyboard_friend_back)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'fiendback':
        await event.edit()
        # await client.send_message(event.input_sender, 'Профиль')
        await menu.profile_menu(event, client, engine=engine)

    elif event.data == b'info_back':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Информация', buttons=buttons.keyboard_info)
        await shared.save_old_message(sender_id, msg)

    elif event.data == b'risk_reset':
        await event.edit()
        if old_msg_id is not None:
            msg = await client.edit_message(event.input_sender, old_msg_id, ins.instruction25,
                                            buttons=buttons.keyboard_reset)
        else:
            msg = await client.send_message(event.input_sender, ins.instruction25, buttons=buttons.keyboard_reset)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'reset_yes':
        await event.edit()
        reset_user_profiler_data(sender_id)
        await client.send_message(event.input_sender, 'Профиль')
        await send_next_profiler_question(client, sender_id, 0)

    elif event.data == b'reset_no':
        await event.edit()
        await menu.profile_menu(event, client, engine=engine)

    # ============================== Subscriptions =============================
    elif event.data == b'z1':
        await event.edit()
        await client.send_message(event.input_sender, 'Уровень подписок', buttons=buttons.keyboard_core_subscriptions)
    elif event.data == b'kcs0':
        await event.edit()
        await client.send_file(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_COMPARE_ID].get_img_path())
    elif event.data == b'kcs1':
        await event.edit()
        await client.send_file(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_START_ID].get_img_path())
        await client.send_message(event.input_sender, shared.SUBSCRIBES[shared.TARIFF_START_ID].get_describe(),
                                  buttons=buttons.keyboard_subscription_start)
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
        # debug(aggregator_status)
        if aggregator_status == 'error':
            # debug("Error description:" + PAYMENT_AGGREGATOR.get_last_error())
            await client.send_message(event.input_sender, 'Упс. Что-то пошло не так.',
                                      buttons=buttons.keyboard_subscription_start)
            await event.edit()
        else:
            # debug("user_id=" + str(sender_id.user_id))
            order_id = str(uuid.uuid4()).replace('-', '')
            debug("OrderId:" + order_id)
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

            debug("Summa:" + summa)
            payment_link = PAYMENT_AGGREGATOR.get_payment_link(order_id, summa)
            debug(payment_link)
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


async def send_next_profiler_question(client, user_id, curr_num):
    _poll_id = None
    _question = None
    _answers = None
    _poll_id = get_next_id()
    old_msg_id = await shared.get_old_msg_id(user_id)
    if curr_num == 0:
        _question = "Ваша цель:"
        _answers = [PollAnswer("Общее благосостояние", b'1'),
                    PollAnswer("Большие покупки - дом, машина", b'2'),
                    PollAnswer("Учеба детей, свадьба", b'3'),
                    PollAnswer("Пенсия", b'4'),
                    PollAnswer("Пассивный доход", b'5')]
    if curr_num == 1:
        _question = "Что из перечисленного описывает вашу ситуацию:"
        _answers = [PollAnswer('Я резидент СНГ, мой брокер из СНГ', b'1'),
                    PollAnswer('Я резидент СНГ, мой брокер из ЕС', b'2'),
                    PollAnswer('Я резидент СНГ, мой брокер из США', b'3'),
                    PollAnswer('Я резидент ЕС, мой брокер из США', b'4'),
                    PollAnswer('Я резидент ЕС, мой брокер из ЕС', b'5'),
                    PollAnswer('Я резидент США, мой брокер из США', b'6'),
                    PollAnswer('У меня нет брокерского счета и я резидент СНГ', b'7')]
    if curr_num == 2:
        _question = "Если у вас есть брокерский счет, можете ли вы покупать ETF-фонды"
        _answers = [PollAnswer('Да', b'1'),
                    PollAnswer('Нет', b'2'),
                    PollAnswer('Незнаю', b'3')]
    if curr_num == 3:
        _question = "Нуждаетесь ли вы в средствах выделенных для инвестиций?"
        _answers = [PollAnswer('Да,эти средства могут понадобиться', b'1'),
                    PollAnswer('Нет, это свободные средства', b'2')]
    if curr_num == 4:
        _question = "Планируете ли Вы выводить деньги с брокерского счета?"
        _answers = [PollAnswer('Да, регулярно', b'1'),
                    PollAnswer('Иногда, по случаю', b'2'),
                    PollAnswer('Нет', b'3')]
    if curr_num == 5:
        _question = "Будете ли Вы делать дополнительные вложения?"
        _answers = [PollAnswer('Да, регулярно', b'1'),
                    PollAnswer('Иногда, по случаю', b'2'),
                    PollAnswer('Дополнительных вложений не планирую', b'3')]
    if curr_num == 6:
        _question = "Срок вложений"
        _answers = [PollAnswer('Меньше года', b'1'),
                    PollAnswer('1-3 года', b'2'),
                    PollAnswer('3-5 лет', b'3'),
                    PollAnswer('5-10 лет', b'4'),
                    PollAnswer('Более 10 лет', b'5')]
    if curr_num == 7:
        _question = "Как часто Вы будете заниматься портфелем?"
        _answers = [PollAnswer('Ежедневно', b'1'),
                    PollAnswer('Ежемесячно', b'2'),
                    PollAnswer('Когда нужно', b'3'),
                    PollAnswer('По случаю', b'4')]
    if curr_num == 8:
        _question = "Какую доходность ожидаете?"
        _answers = [PollAnswer('Выше уровня инфляции', b'1'),
                    PollAnswer('10%', b'2'),
                    PollAnswer('10-15%', b'3'),
                    PollAnswer('15-20%', b'4'),
                    PollAnswer('Более 20%', b'5')]
    if curr_num == 9:
        _question = "Потеря какой части вашего вклада будет катастрофической?"
        _answers = [PollAnswer('От -5% до -10%', b'1'),
                    PollAnswer('От -10% до -20%', b'2'),
                    PollAnswer('От -20% до -35%', b'3'),
                    PollAnswer('От -35% до -50%', b'4'),
                    PollAnswer('До -75', b'5')]
    if curr_num == 10:
        _question = "Убыток в 20% от размера вашего вклада это:"
        _answers = [PollAnswer('Ничего страшного', b'1'),
                    PollAnswer('Терпимо', b'2'),
                    PollAnswer('Не приемлемо', b'3')]
    if curr_num == 11:
        _question = "Ваши действия во время просадки на рынке в 15%:"
        _answers = [PollAnswer('Не знаю', b'1'),
                    PollAnswer('Ничего не сделаю', b'2'),
                    PollAnswer('Продам все', b'3'),
                    PollAnswer('Продам часть', b'4'),
                    PollAnswer('Продам убыточные', b'5'),
                    PollAnswer('Продам прибыльные', b'6'),
                    PollAnswer('Докуплю', b'7'),
                    PollAnswer('Что-то продам и что-то докуплю', b'8')]
    if curr_num == 12:
        _question = "Вы предпочти бы акции:"
        _answers = [PollAnswer('С доходностью в 20% годовых, но ранее эти акции падали на -50%', b'1'),
                    PollAnswer('С доходностью в 15% годовых, но ранее эти акции падали на -20%', b'2'),
                    PollAnswer('С доходностью в 150% годовых, но ранее эти акции падали на -70%', b'3'),
                    PollAnswer('С доходностью в 10% годовых, но ранее эти акции падали на -10%', b'4')]
    if curr_num == 13:
        _question = "Вы предпочитаете:"
        _answers = [PollAnswer('Гарантированные 50% от вашей суммы через 3 года', b'1'),
                    PollAnswer('35% - 80% через  5лет, но без гарантий, но не менее 35%', b'2')]
    poll = Poll(id=_poll_id,
                question=_question,
                answers=_answers)
    input_media_poll = InputMediaPoll(poll)
    poll_msg = None
    if old_msg_id is not None:
        await shared.delete_old_message(client, user_id)
        poll_msg = await client.send_message(user_id, file=input_media_poll)
        await shared.save_old_message(user_id, poll_msg)
        shared.set_old_msg_poll(user_id, True)
        pass
    else:
        poll_msg = await client.send_message(user_id, file=input_media_poll)
    real_poll_id = poll_msg.media.poll.id
    update_user_profiler_map(user_id, real_poll_id, curr_num)
    if curr_num == 0:
        await shared.save_old_message(user_id, poll_msg)
        shared.set_old_msg_poll(user_id, True)


async def update_poll(update, client):
    poll_id = update.poll_id
    user_id, qnumber = get_userid_by_pollid(poll_id)
    if user_id is not None:
        answer_res = None
        votes_list = update.results.results
        for vote in votes_list:
            if vote.voters == 1:
                answer_res = shared.get_prifiler_score(qnumber, vote.option)
                break
        increment_final_score(user_id, answer_res)
        if qnumber < 13:
            await send_next_profiler_question(client, user_id, qnumber + 1)
        else:
            old_msg_id = await shared.get_old_msg_id(user_id)
            shared.set_old_msg_poll(user_id, False)
            if old_msg_id is not None:
                await shared.delete_old_message(client, user_id)
                main_menu_msg = await client.send_message(user_id, 'Главное меню', buttons=buttons.keyboard_0)
                await shared.save_old_message(user_id, main_menu_msg)
            else:
                menu_msg = await client.send_message(user_id, 'Главное меню', buttons=buttons.keyboard_0)
                await shared.delete_old_message(client, user_id)
                await shared.save_old_message(user_id, menu_msg)


        # await client.send_message(event.input_sender, 'Текущая структура портфеля')
        # await client.send_file(entity, CHARTER_IMAGES_PATH + 'parking_portfolio_pie.png')