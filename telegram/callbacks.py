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

PAYMENT_AGGREGATOR = None
PAYMENT_AGGREGATOR_TIMER = None


# ============================== Callbacks =======================

async def callback_handler(event, client, img_path=None, yahoo_path=None, engine=None):
    sender_id = event.original_update.user_id
    entity = await client.get_input_entity(sender_id)
    chat = await event.get_chat()
    old_msg_id = await shared.get_old_msg_id(sender_id)

    # ============================== Главное меню 1 уровень=============================
    # message = await client.send_message(entity=entity, message='Загрузка...')
    # await client.delete_messages(event.input_sender, message)

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
            await client.edit_message(event.input_sender, old_msg_id, 'Скринер акций', buttons=buttons.keyboard_screener)
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

    elif event.data == b'a20':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Сотрудничество', buttons=buttons.keyboard_relations)
        else:
            msg = await client.send_message(event.input_sender, 'Сотрудничество', buttons=buttons.keyboard_relations)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'main':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Главное меню', buttons=buttons.keyboard_0)
        else:
            menu_msg = await client.send_message(event.input_sender, 'Главное меню', buttons=buttons.keyboard_0)
            await shared.delete_old_message(client, sender_id)
            shared.save_old_message(sender_id, menu_msg)

    # ============================== Анализ рынков 2 уровень=============================
    elif event.data == b'a1a1':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Анализ США', buttons=buttons.keyboard_us_analysis)
        else:
            msg = await client.send_message(event.input_sender, 'Анализ США', buttons=buttons.keyboard_us_analysis)
            shared.save_old_message(sender_id, msg)

    elif event.data == b'us5x':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Подробный анализ', buttons=buttons.keyboard_us_market)
        else:
            msg = await client.send_message(event.input_sender, 'Подробный анализ', buttons=buttons.keyboard_us_market)
            shared.save_old_message(sender_id, msg)

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
            await client.edit_message(event.input_sender, old_msg_id, 'Основные макро индикаторы', buttons=buttons.keyboard_core_macro)
        else:
            msg = await client.send_message(event.input_sender, 'Основные макро индикаторы', buttons=buttons.keyboard_core_macro)
            shared.save_old_message(sender_id, msg)
    elif event.data == b'a1a-1':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Анализ рынков', buttons=buttons.keyboard_a1)
        shared.save_old_message(sender_id, msg)

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
    elif event.data == b'a2a3':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, '"Парковочный" портфель без риска')
        await client.send_message(event.input_sender, 'Текущая структура портфеля')
        await client.send_file(entity, CHARTER_IMAGES_PATH + 'parking_portfolio_pie.png')
        await client.send_message(event.input_sender, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'parking.pdf')
        await client.send_message(event.input_sender, 'Симуляция доходности портфеля на 10 лет \n '
                                                      'Как интерпретировать результаты симуляций Монте-Карло?'
                                                      ' - /instruction19')
        await client.send_file(entity, STATS_PATH + 'parking.png')
        await client.send_file(entity, STATS_PATH + 'parking2.png')
        await client.send_message(event.input_sender, 'Кому и когда покупать парковочный портфель? \n'
                                                      '/instruction14 \n End of Day График - /chart_parking',
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
            await client.edit_message(event.input_sender, old_msg_id, 'Исторические тесты', buttons=buttons.keyboard_a2)
        else:
            msg = await client.send_message(event.input_sender, 'Исторические тесты', buttons=buttons.keyboard_a2)
            shared.save_old_message(sender_id, msg)

    # ============================== Управление =============================
    elif event.data == b'a4a1':
        risk_profile = sql.risk_data_lookup(event.original_update.peer.user_id, engine)
        if risk_profile:
            await event.edit()
            await client.send_message(event.input_sender, 'Доступные портфели', buttons=buttons.keyboard_managed_strategies)
        else:

            message = await client.send_message(entity=entity, message='Загрузка...')
            await client.edit_message(message, ' Для доступа к портфелям управляющих необходимо '
                                               'определить ваш уровень терпимости к риску')
            await client.send_message(event.input_sender, 'Выберите наиболее подходящий вариант для вас \n \n'
                                      + ins.instruction25, buttons=buttons.keyboard_risk_profile)

    elif event.data == b'rel1':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Предложения и реклама')
        await client.send_message(event.input_sender, ins.managers_form,
                                  buttons=buttons.keyboard_relations_back)

    elif event.data == b'rel2':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Регистрация управляющего')
        await client.send_message(event.input_sender, ins.managers_form,
                                  buttons=buttons.keyboard_relations_back)

    elif event.data == b'rel3':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Сообщить об ошибке')
        await client.send_message(event.input_sender, ins.managers_form,
                                  buttons=buttons.keyboard_relations_back)

    # elif event.data == b'a4a-0':
    #     await event.edit()
    #     await client.send_message(event.input_sender, 'Регистрация управляющего', buttons=buttons.keyboard_a4)

    elif event.data == b'sac1':
        await event.edit()
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'sac_parking.pdf')
        await client.send_message(event.input_sender, 'О доверительном управлении \n'
                                                      '/instruction26',
                                  buttons=buttons.keyboard_managed_strategies)
    elif event.data == b'sac2':
        await event.edit()
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'sac_balanced.pdf')
        await client.send_message(event.input_sender, 'О доверительном управлении \n'
                                                      '/instruction26',
                                  buttons=buttons.keyboard_managed_strategies)

    elif event.data == b'sac3':
        await event.edit()
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Подробная статистика стратегии')
        await client.send_file(entity, STATS_PATH + 'sac_growth.pdf')
        await client.send_message(event.input_sender, 'О доверительном управлении \n'
                                                      '/instruction26',
                                  buttons=buttons.keyboard_managed_strategies)
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
        await client.send_message(entity, ins.hello_4, file=f'{PROJECT_HOME_DIR}/html/hello_4.jpg',
                                  buttons=buttons.keyboard_forw5)
    elif event.data == b'forw5':
        await event.edit()
        await client.send_message(entity, ins.hello_5, file=f'{PROJECT_HOME_DIR}/html/hello_5.jpg',
                                  buttons=buttons.keyboard_forw6)
    elif event.data == b'forw6':
        await event.edit()
        await client.send_message(entity, ins.hello_6, file=f'{PROJECT_HOME_DIR}/html/hello_6.jpg',
                                  buttons=buttons.keyboard_forw7)
    elif event.data == b'forw7':
        await event.edit()
        await client.send_message(entity, ins.hello_7, file=f'{PROJECT_HOME_DIR}/html/hello_7.jpg',
                                  buttons=buttons.keyboard_forw8)
    elif event.data == b'forw8':
        await event.edit()
        await client.send_message(entity, ins.hello_8, file=f'{PROJECT_HOME_DIR}/html/hello_8.jpg',
                                  buttons=buttons.keyboard_forw9)

    # ============================== Образовательные программы =============================
    elif event.data == b'a6a1':
        await event.edit()
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Основы инвестирования')
        await client.send_message(event.input_sender, 'Основы инвестирования /instruction20',
                                  buttons=buttons.keyboard_a6_back)
    elif event.data == b'a6a2':
        await event.edit()
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Как собрать свой первый портфель')
        await client.send_message(event.input_sender, 'Как собрать свой первый портфель /instruction21',
                                  buttons=buttons.keyboard_a6_back)
    elif event.data == b'a6a3':
        await event.edit()
        message = await client.send_message(entity=entity, message='Загрузка...')
        await client.edit_message(message, 'Профессиональные решения')
        await client.send_message(event.input_sender, 'Профессиональные решения /instruction22',
                                  buttons=buttons.keyboard_a6_back)
    elif event.data == b'a6a-1':
        await event.edit()
        await client.send_message(event.input_sender, 'Образование', buttons=buttons.keyboard_a6)

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
        shared.save_old_message(sender_id, msg)

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
        msg = await client.send_message(event.input_sender, 'Основные макро индикаторы', buttons=buttons.keyboard_core_macro)
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
            await client.edit_message(event.input_sender, old_msg_id, 'Подробный анализ', buttons=buttons.keyboard_us_market)
        else:
            msg = await client.send_message(event.input_sender, 'Подробный анализ', buttons=buttons.keyboard_us_market)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'cm-4':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Анализ США', buttons=buttons.keyboard_us_analysis)
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
        msg = await client.send_message(event.input_sender, 'Исторические тесты', buttons=buttons.keyboard_a2)
        await shared.save_old_message(sender_id, msg)

    elif event.data == b'cm-6':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Сотрудничество', buttons=buttons.keyboard_relations)
        await shared.save_old_message(sender_id, msg)

    elif event.data == b'z2':
        await event.edit()
        await client.send_message(event.input_sender,
                                  'Вы можете попросить друга запустить бота и получить бесплатную'
                                  ' подписку. '
                                  'Проще всего это сделать через групповые чаты' + '\n' +
                                  f'[https://t.me/UpsilonBot?start={sender_id}]'
                                  f'(https://t.me/UpsilonBot?start={sender_id})')

        # ============================== Risk Profile =============================
    elif event.data == b'rp1':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message='Укажите примерную стоимость средств выделенных для инвестирования',
                                  buttons=buttons.keyboard_financial_state)

    elif event.data == b'rp2':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message='Укажите примерную стоимость средств выделенных для инвестирования',
                                  buttons=buttons.keyboard_financial_state)
    elif event.data == b'rp3':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message='Укажите примерную стоимость средств выделенных для инвестирования',
                                  buttons=buttons.keyboard_financial_state)
    elif event.data == b'rp4':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message='Укажите примерную стоимость средств выделенных для инвестирования',
                                  buttons=buttons.keyboard_financial_state)
    elif event.data == b'rp5':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message='Укажите примерную стоимость средств выделенных для инвестирования',
                                  buttons=buttons.keyboard_financial_state)
    elif event.data == b'rp6':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message='Укажите примерную стоимость средств выделенных для инвестирования',
                                  buttons=buttons.keyboard_financial_state)

    elif event.data == b'fs1':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_fs,
                                  buttons=buttons.keyboard_horizon)
    elif event.data == b'fs2':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_fs,
                                  buttons=buttons.keyboard_horizon)
    elif event.data == b'fs3':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_fs,
                                  buttons=buttons.keyboard_horizon)
    elif event.data == b'fs4':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_fs,
                                  buttons=buttons.keyboard_horizon)

    elif event.data == b'hr1':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_hr,
                                  buttons=buttons.keyboard_return)
    elif event.data == b'hr2':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_hr,
                                  buttons=buttons.keyboard_return)
    elif event.data == b'hr3':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_hr,
                                  buttons=buttons.keyboard_return)
    elif event.data == b'hr4':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_hr,
                                  buttons=buttons.keyboard_return)

    elif event.data == b'ret1':
        await event.edit()

        await client.send_message(event.input_sender,
                                  message=ins.msg_ret,
                                  buttons=buttons.keyboard_a4)
    elif event.data == b'ret2':
        await event.edit()

        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_ret,
                                  buttons=buttons.keyboard_a4)
    elif event.data == b'ret3':
        await event.edit()
        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_ret,
                                  buttons=buttons.keyboard_a4)
    elif event.data == b'ret4':
        await event.edit()
        user_profile = await sql.user_search(event.original_update.peer.user_id, engine)
        update = str(event.data)
        update = update.strip("b'")
        await sql.db_save_risk_profile(update, user_profile[1], engine)
        await client.send_message(event.input_sender,
                                  message=ins.msg_ret,
                                  buttons=buttons.keyboard_a4)

    elif event.data == b'sacback':
        await event.edit()
        await client.send_message(event.input_sender,
                                  message='Назад',
                                  buttons=buttons.keyboard_a4)

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


def update_poll(update, client, engine=engine):
    pass