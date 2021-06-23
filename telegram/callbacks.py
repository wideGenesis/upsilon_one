import asyncio
import importlib
import os
import csv
import datetime
import time
import uuid
import re

from datetime import timedelta, datetime
from telethon import utils

from telegram import buttons
from telegram import sql_queries as sql
from telegram import menu
from telegram import shared
from telethon import types
from project_shared import *
from telegram import instructions as ins
from quotes.stock_quotes_news import fin_news
from quotes.parsers import nyse_nasdaq_stat
from messages.message import *
from telethon.tl.types import InputMediaPoll, Poll, PollAnswer, DocumentAttributeFilename, DocumentAttributeVideo
from quotes.parsers import *
from quotes import sql_queries as sql_q
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer


# ============================== Callbacks =======================
async def callback_handler(event, client, img_path=None, yahoo_path=None, engine=None):
    sender_id = event.original_update.user_id
    entity = await client.get_input_entity(sender_id)
    chat = await event.get_chat()
    old_msg_id = await shared.get_old_msg_id(sender_id)
    shared.set_is_inspector_flow(sender_id, False)

    # ============================== 📁 Main menu 1 уровень=============================
    if event.data == b'kb0_market_analysis':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Market Analysis', buttons=buttons.keyboard_a1)
        else:
            msg = await client.send_message(event.input_sender, 'Market Analysis', buttons=buttons.keyboard_a1)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb0_my_portfolio':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, f'My portfolio\n'
                                                                      f'How to buy a portfolio? - /instruction27\n'
                                                                      f'Minimum deposit - /mindepo',
                                      buttons=buttons.keyboard_portfolio)
        else:
            msg = await client.edit_message(event.input_sender, old_msg_id, f'My portfolio\n'
                                                                            f'How to buy a portfolio? - /instruction27\n'
                                                                            f'Minimum deposit - /mindepo',
                                            buttons=buttons.keyboard_portfolio)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb0_stock_screener':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Stock screener',
                                      buttons=buttons.keyboard_screener)
        else:
            msg = await client.send_message(event.input_sender, 'Stock screener', buttons=buttons.keyboard_screener)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'instructions':
        await event.edit()
        msg = await client.send_message(event.input_sender, ins.instructions_main, buttons=buttons.keyboard_info_back)
        await shared.delete_old_message(client, sender_id)

    elif event.data == b'kb0_news_feed':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'News feed', buttons=buttons.keyboard_a8)
        else:
            msg = await client.send_message(event.input_sender, 'News feed', buttons=buttons.keyboard_a8)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb0_donate':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Donate', buttons=buttons.keyboard_donate)
        else:
            msg = await client.send_message(event.input_sender, 'Donate', buttons=buttons.keyboard_donate)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'donate2':
        await make_payment(event, client, 0, 2.0, 'donate')

    elif event.data == b'donate5':
        await make_payment(event, client, 0, 5.0, 'donate')

    elif event.data == b'donate10':
        await make_payment(event, client, 0, 10.0, 'donate')

    elif event.data == b'donate50':
        await make_payment(event, client, 0, 50.0, 'donate')

    elif event.data == b'donate100':
        await make_payment(event, client, 0, 100.0, 'donate')

    # ############# INLINE DONATE KBD
    elif event.data == b'inline_donate':
        await send_invoice(client, event)

    elif event.data == b'donate_back':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Donate', buttons=buttons.keyboard_donate)
        else:
            msg = await client.send_message(event.input_sender, 'Donate', buttons=buttons.keyboard_donate)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'buy_requests5':
        await make_payment(event, client, 33, 5.0, 'replenishment')

    elif event.data == b'buy_requests10':
        await make_payment(event, client, 67, 10.0, 'replenishment')

    elif event.data == b'buy_requests20':
        await make_payment(event, client, 143, 20.0, 'replenishment')

    elif event.data == b'buy_requests50':
        await make_payment(event, client, 417, 50.0, 'replenishment')

    elif event.data == b'buy_requests100':
        await make_payment(event, client, 1000, 100.0, 'replenishment')

    elif event.data == b'buy_requests150':
        await make_payment(event, client, 1875, 150.0, 'replenishment')

    elif event.data == b'buy_requests200':
        await make_payment(event, client, 3333, 200.0, 'replenishment')

    elif event.data == b'buy_requests300':
        await make_payment(event, client, 7500, 300.0, 'replenishment')

    # ############# INLINE PAYMENT KBD
    elif event.data == b'inline_payment':
        await send_invoice(client, event)

    elif event.data == b'payment_back':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id,
                                      '🔋 - one request',
                                      buttons=buttons.keyboard_buy_requests)
        else:
            msg = await client.send_message(event.input_sender,
                                            '🔋 - one request',
                                            buttons=buttons.keyboard_buy_requests)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'main':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, '📁 Main menu', buttons=buttons.keyboard_0)
        else:
            menu_msg = await client.send_message(event.input_sender, '📁 Main menu', buttons=buttons.keyboard_0)
            await shared.delete_old_message(client, sender_id)
            await shared.save_old_message(sender_id, menu_msg)

    # ============================== Market Analysis 2 уровень=============================
    elif event.data == b'kb_a1_us_market':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'US market analysis\n'
                                                                      'При вызове \"Обзора рынка США\" '
                                                                      'списывается 1 запрос🔋',
                                      buttons=buttons.keyboard_us_analysis)
        else:
            msg = await client.send_message(event.input_sender, 'US market analysis\n'
                                                                      'При вызове \"Обзора рынка США\" '
                                                                      'списывается 1 запрос🔋',
                                            buttons=buttons.keyboard_us_analysis)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb_us_analysis_insideview':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Detailed analysis',
                                      buttons=buttons.keyboard_us_market)
        else:
            msg = await client.send_message(event.input_sender, 'Detailed analysis',
                                            buttons=buttons.keyboard_us_market)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb_us_analysis_overview':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        # Подгрузим динамически модуль - вдруг ценообразование изменилось?!
        pricing = None
        if "telegram.pricing" in sys.modules:
            debug(f'module imported --- try reload')
            pricing = importlib.reload(sys.modules["telegram.pricing"])
        else:
            debug(f'module NOT imported --- try first import')
            pricing = importlib.import_module("telegram.pricing")

        pricing_result = await pricing.check_request_amount(event.input_sender.user_id, client)
        if not pricing_result["result"]:
            return
        if os.path.exists(f'{img_path}sectors.png') and os.path.exists(f'{img_path}treemap_1d.png'):
            await client.send_file(entity, f'{img_path}sectors.png')
            await client.send_message(event.input_sender, 'US market overview\n /instruction02\n /instruction35\n')
            await client.send_file(entity, f'{img_path}treemap_1d.png')
            await client.send_message(event.input_sender, 'US Heatmap\n'
                                                          '/instruction04',
                                      buttons=buttons.keyboard_us_analysis_back)
        else:
            # вернем баланс в случае если картинок нет. Вероятно это просто сбой, такого быть не должно
            if pricing_result['Paid'] > 0:
                await sql.increment_paid_request_amount(event.input_sender.user_id, pricing_result['Paid'])
            if pricing_result['Free'] > 0:
                await sql.increment_free_request_amount(event.input_sender.user_id, pricing_result['Free'])
            await shared.delete_old_message(client, sender_id)
            await client.send_message(sender_id, message=f'Oops! Something went wrong.')

    elif event.data == b'kb_a1_coin_market':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_file(entity, img_path + 'crypto.png')
        await client.send_message(event.input_sender, 'BTCUSD and ETHUSD overview\n /instruction07 /instruction35\n')
        await client.send_file(entity, img_path + 'coins_treemap.png')
        await client.send_message(event.input_sender, 'Crypto Heatmap\n'
                                                      '/instruction04',
                                  buttons=buttons.keyboard_a1_back)

    # elif event.data == b'kb_a1_rus_market':
    #     await event.edit()
    #     await shared.delete_old_message(client, sender_id)
    #     await client.send_file(entity, img_path + 'rtsi.png')
    #     await client.send_message(event.input_sender, 'Обзор рынка РФ\n'
    #                                                   '/instruction08')
    #     await client.send_file(entity, img_path + 'moex_map.png')
    #     await client.send_message(event.input_sender, 'Тепловая карта акций РФ\n'
    #                                                   '/instruction04',
    #                               buttons=buttons.keyboard_a1_back)

    elif event.data == b'kb_a1_world_markets':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_file(entity, img_path + 'world.png')
        await client.send_message(event.input_sender, 'Global Markets Overview\n'
                                                      '/instruction04')
        await client.send_file(entity, img_path + 'global_treemap_1d.png')
        await client.send_message(event.input_sender, 'Global Markets Heatmap\n'
                                                      '/instruction04',
                                  buttons=buttons.keyboard_a1_back)

    elif event.data == b'kb_us_market_macro_forecast':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Economic Indicators',
                                      buttons=buttons.keyboard_core_macro)
        else:
            msg = await client.send_message(event.input_sender, 'Economic Indicators',
                                            buttons=buttons.keyboard_core_macro)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb_a1_back':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Market Analysis', buttons=buttons.keyboard_a1)
        await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb_us_market_adl':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        msg = nyse_nasdaq_stat()
        message = await client.send_message(entity=entity, message='Loading...')
        await client.send_message(entity=entity, message=msg)

        await client.edit_message(message, 'Advances/Decliners')
        await client.send_message(event.input_sender, 'How to interpret trading statistics? \n'
                                                      '/instruction01',
                                  buttons=buttons.keyboard_us_market_back)

    elif event.data == b'kb_us_market_mom':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        filename2 = os.path.join(img_path, 'sma50.csv')
        with open(filename2, newline='') as f2:
            data2 = csv.reader(f2, delimiter=',')
            for row2 in data2:
                r2 = str(row2).strip("['']").replace("'", "")
                await client.send_message(entity=entity, message=f'{r2}')
        await client.edit_message(message, 'Stock Momentum')
        await client.send_message(event.input_sender, 'How to interpret momentum? \n'
                                                      '/instruction03',
                                  buttons=buttons.keyboard_us_market_back)

    elif event.data == b'kb_us_market_vol_curve':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        filename6 = os.path.join(img_path, 'vix_cont.csv')
        with open(filename6, newline='') as f6:
            data6 = csv.reader(f6, delimiter=',')
            for row6 in data6:
                row6 = str(row6).strip("[']")
                await client.send_message(entity=entity, message=f'{row6}')
        await client.send_file(entity, img_path + 'vix_curve.png')
        await client.edit_message(message, 'Volatility Structure')
        await client.send_message(event.input_sender, 'How to interpret the volatility structure? /instruction06',
                                  buttons=buttons.keyboard_us_market_back)

    elif event.data == b'hist_parking':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'Parking portfolio')

        await client.send_message(event.input_sender, 'Detailed statistics',
                                  file='http://watchlister.ru/upsilon_files/parking.pdf')
        await client.send_message(event.input_sender, 'Performance since 2008',
                                  file=STATS_PATH + 'parking3.png')
        # await client.send_message(event.input_sender, 'Как интерпретировать результаты симуляций Монте-Карло?\n'
        #                                               '/instruction19',
        #                           file=STATS_PATH + 'parking2.png')
        await client.send_message(event.input_sender, 'When to buy a  Parking portfolio?\n'
                                                      '/instruction14',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'hist_allweather':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'All Weather portfolio')
        await client.send_message(event.input_sender, 'Detailed statistics',
                                  file='http://watchlister.ru/upsilon_files/allweather.pdf')
        await client.send_message(event.input_sender, 'Performance since 2008',
                                  file=STATS_PATH + 'allweather3.png')
        # await client.send_message(event.input_sender, 'Как интерпретировать результаты симуляций Монте-Карло?\n'
        #                                               '/instruction19',
        #                           file=STATS_PATH + 'allweather2.png')
        await client.send_message(event.input_sender, 'When to buy an All Weather portfolio?\n'
                                                      '/instruction15',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'hist_balanced':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'Conservative portfolio')
        await client.send_message(event.input_sender, 'Detailed statistics',
                                  file='http://watchlister.ru/upsilon_files/balanced.pdf')
        await client.send_message(event.input_sender, 'Performance since 2008',
                                  file=STATS_PATH + 'balanced3.png')
        # await client.send_message(event.input_sender, 'Как интерпретировать результаты симуляций Монте-Карло?\n'
        #                                               '/instruction19',
        #                           file=STATS_PATH + 'balanced2.png')
        await client.send_message(event.input_sender, 'When to buy a Conservative portfolio?\n'
                                                      '/instruction16',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'hist_agg':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'Aggressive portfolio')
        await client.send_message(event.input_sender, 'Detailed statistics',
                                  file='http://watchlister.ru/upsilon_files/aggressive.pdf')
        await client.send_message(event.input_sender, 'Performance since 2016 года',
                                  file=STATS_PATH + 'aggressive3.png')
        # await client.send_message(event.input_sender, 'Как интерпретировать результаты симуляций Монте-Карло?\n'
        #                                               '/instruction19',
        #                           file=STATS_PATH + 'aggressive2.png')
        await client.send_message(event.input_sender, 'When to buy an Aggressive portfolio?\n'
                                                      '/instruction17',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'hist_lev':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'Leveraged portfolio')
        await client.send_message(event.input_sender, 'Detailed statistics',
                                  file='http://watchlister.ru/upsilon_files/leveraged.pdf')
        await client.send_message(event.input_sender, 'Performance since 2016 года',
                                  file=STATS_PATH + 'leveraged3.png')
        # await client.send_message(event.input_sender, 'Как интерпретировать результаты симуляций Монте-Карло?\n'
        #                                               '/instruction19',
        #                           file=STATS_PATH + 'leveraged2.png')
        await client.send_message(event.input_sender, 'When to buy a Leveraged portfolio?\n'
                                                      '/instruction18',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'hist_elastic':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'Elastic - stocks only portfolio')
        await client.send_message(event.input_sender, 'Detailed statistics',
                                  file='http://watchlister.ru/upsilon_files/elastic.pdf')
        await client.send_message(event.input_sender, 'Performance since 2008',
                                  file=STATS_PATH + 'elastic3.png')
        # await client.send_message(event.input_sender, 'Как интерпретировать результаты симуляций Монте-Карло?\n'
        #                                               '/instruction19',
        #                           file=STATS_PATH + 'elastic2.png')
        await client.send_message(event.input_sender, 'When to buy an Elastic portfolio?\n'
                                                      '/instruction23',
                                  buttons=buttons.keyboard_a3_back)

    # elif event.data == b'hist_yolo':
    #     await event.edit()
    #     await shared.delete_old_message(client, sender_id)
    #     message = await client.send_message(entity=entity, message='Loading...')
    #     await client.edit_message(message, 'Yolo - portfolio только из акций, торгуемых на spbexchange. '
    #                                        'Доступен для клиентов Сбер, Тинькофф, Альфа-банк, ВТБ')
    #     await client.send_message(event.input_sender, 'Detailed statistics',
    #                               file='http://watchlister.ru/upsilon_files/yolo.pdf')
    #     await client.send_message(event.input_sender, 'Performance since 2020 года',
    #                               file=STATS_PATH + 'yolo3.png')
    #     # await client.send_message(event.input_sender, 'Как интерпретировать результаты симуляций Монте-Карло?\n'
    #     #                                               '/instruction19',
    #     #                           file=STATS_PATH + 'yolo2.png')
    #     await client.send_message(event.input_sender, 'When to buy a  Yolo portfolio?\n'
    #                                                   '/instruction24',
    #                               buttons=buttons.keyboard_a3_back)

    elif event.data == b'hist_allseasons_s':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'All Seasons S')
        await client.send_message(event.input_sender, 'Portfolio statistics',
                                  file=STATS_PATH + 'all_season_s.png')
        await client.send_message(event.input_sender, ins.all_seasons_s + '\n\n'
                                                                         'When to buy an All Seasons '
                                                                         'S portfolio?\n'
                                                                         '/instruction31',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'hist_allseasons_m':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'All Seasons M')
        await client.send_message(event.input_sender, 'Portfolio statistics',
                                  file=STATS_PATH + 'all_season_m.png')
        await client.send_message(event.input_sender, ins.all_seasons_m + '\n\n'
                                                                         'When to buy an All Seasons '
                                                                         'M portfolio?\n'
                                                                         '/instruction32',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'hist_allseasons_l':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'All Seasons L')
        await client.send_message(event.input_sender, 'Portfolio statistics',
                                  file=STATS_PATH + 'all_season_l.png')
        await client.send_message(event.input_sender, ins.all_seasons_l + '\n\n'
                                                                         'When to buy an All Seasons '
                                                                         'L portfolio?\n'
                                                                         '/instruction33',
                                  buttons=buttons.keyboard_a3_back)

    elif event.data == b'historical_tests':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Historical performance',
                                      buttons=buttons.keyboard_historical_tests)
        else:
            msg = await client.send_message(event.input_sender, 'Historical performance',
                                            buttons=buttons.keyboard_historical_tests)
            await shared.save_old_message(sender_id, msg)

    # elif event.data == b'manager_registration':
    #     await event.edit()
    #     await shared.delete_old_message(client, sender_id)
    #     message = await client.send_message(entity=entity, message='Loading...')
    #     await client.edit_message(message, 'Регистрация управляющего')
    #     await client.send_message(event.input_sender, ins.managers_form,
    #                               buttons=buttons.keyboard_info_back)

    elif event.data == b'advertisement':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'Offers and advertisements')
        await client.send_message(event.input_sender, ins.instruction29,
                                  buttons=buttons.keyboard_info_back)

    elif event.data == b'bug_report':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'Report a bug')
        await client.send_message(event.input_sender, ins.instruction30,
                                  buttons=buttons.keyboard_info_back)

    elif event.data == b'brokers_compare':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        message = await client.send_message(entity=entity, message='Loading...')
        await client.edit_message(message, 'Compare brokers')
        await client.send_message(event.input_sender, ins.brokers,
                                  buttons=buttons.keyboard_info_back)

    elif event.data == b'risk_profile_restart':
        await event.edit()
        reset_user_profiler_data(sender_id)
        await client.send_message(event.input_sender, 'Profile')
        await send_next_profiler_question(client, sender_id, 0)

    elif event.data == b'my_strategies':
        await event.edit()
        await my_strategies_dynamic_menu(event, client, sender_id, old_msg_id)

    elif event.data == b'strategy_parking':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        chart_fname = f'{CHARTER_IMAGES_PATH}parking_port_chart_over_TLT.png'
        pie_fname = f'{CHARTER_IMAGES_PATH}parking_portfolio_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, 'The chart is updated daily',
                                  file=chart_fname,
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategy_allweather':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        chart_fname = f'{CHARTER_IMAGES_PATH}allweather_port_chart_over_SPY.png'
        pie_fname = f'{CHARTER_IMAGES_PATH}allweather_portfolio_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, 'The chart is updated daily',
                                  file=chart_fname,
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategy_balanced':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        chart_fname = f'{CHARTER_IMAGES_PATH}balanced_port_chart_over_QQQ.png'
        pie_fname = f'{CHARTER_IMAGES_PATH}balanced_portfolio_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, 'The chart is updated daily',
                                  file=chart_fname,
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategy_aggressive':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        chart_fname = f'{CHARTER_IMAGES_PATH}aggressive_port_chart_over_QQQ.png'
        pie_fname = f'{CHARTER_IMAGES_PATH}aggressive_portfolio_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, 'The chart is updated daily',
                                  file=chart_fname,
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategy_leveraged':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        chart_fname = f'{CHARTER_IMAGES_PATH}leveraged_port_chart_over_QQQ.png'
        pie_fname = f'{CHARTER_IMAGES_PATH}leveraged_portfolio_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, 'The chart is updated daily',
                                  file=chart_fname,
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategy_yolo':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        chart_fname = f'{CHARTER_IMAGES_PATH}yolo_port_chart_over_SPY.png'
        pie_fname = f'{CHARTER_IMAGES_PATH}yolo_portfolio_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, 'The chart is updated daily',
                                  file=chart_fname,
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategy_elastic':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        chart_fname = f'{CHARTER_IMAGES_PATH}elastic_port_chart_over_QQQ.png'
        pie_fname = f'{CHARTER_IMAGES_PATH}elastic_portfolio_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, 'The chart is updated daily',
                                  file=chart_fname,
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategy_allseasons_s':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        pie_fname = f'{CHARTER_IMAGES_PATH}all_seasons_s_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, ins.passive_investments + '\n\n'
                                                                                'When to buy a  All Seasons '
                                                                                'S portfolio?\n'
                                                                                '/instruction31',
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategy_allseasons_m':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        pie_fname = f'{CHARTER_IMAGES_PATH}all_seasons_m_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, ins.passive_investments + '\n\n'
                                                                                'When to buy a  All Seasons '
                                                                                'M portfolio?\n'
                                                                                '/instruction32',
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategy_allseasons_l':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        pie_fname = f'{CHARTER_IMAGES_PATH}all_seasons_l_pie.png'
        await client.send_file(entity, pie_fname)
        await client.send_message(event.input_sender, ins.passive_investments + '\n\n'
                                                                                'When to buy a  All Seasons '
                                                                                'L portfolio?\n'
                                                                                '/instruction33',
                                  buttons=buttons.my_strategies_back)

    elif event.data == b'strategies_back':
        await event.edit()
        await my_strategies_dynamic_menu(event, client, sender_id, old_msg_id)

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
        await client.send_message(entity=entity, message='__Which investment way is right for you?__',
                                  buttons=buttons.keyboard_start)
        await client.send_message(entity, ins.hello_8, file=f'{PROJECT_HOME_DIR}/html/hello_8.jpg',
                                  buttons=buttons.keyboard_forw9)

    elif event.data == b'forw9':
        await event.edit()
        await send_next_profiler_question(client, sender_id, 0)

    elif event.data == b'kb_a8_market_news':
        if old_msg_id is not None:
            await client.edit_message(entity, old_msg_id, 'Latest news')
            shared.pop_old_msg_id(sender_id)
        else:
            await client.send_message(entity, 'Latest news')
        msg1 = fin_news(blogs=False)
        await client.send_message(entity, msg1, buttons=buttons.keyboard_a8_back)

    elif event.data == b'kb_a8_analytical_blogs':
        if old_msg_id is not None:
            await client.edit_message(entity, old_msg_id, 'Latest articles')
            shared.pop_old_msg_id(sender_id)
        else:
            await client.send_message(entity, 'Latest articles')
        msg2 = fin_news(blogs=True)
        await client.send_message(entity, msg2, buttons=buttons.keyboard_a8_back)

    elif event.data == b'kb_a8_back':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'News Aggregator', buttons=buttons.keyboard_a8)
        await shared.save_old_message(sender_id, msg)

    elif event.data == b'financial_analysis':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(event.input_sender, message=ins.instruction21,
                                  buttons=buttons.keyboard_screener_back)
    elif event.data == b'top_gurus':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        guru_link_file = f'{PROJECT_HOME_DIR}/results/gururocketscreener/guru.lnk'
        with open(guru_link_file, 'r') as f:
            guru_link = f.read()
        await client.send_message(event.input_sender,
                                  message=guru_link,
                                  buttons=buttons.keyboard_screener_back)
    elif event.data == b'top_cheap':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        rocket_link_file = f'{PROJECT_HOME_DIR}/results/gururocketscreener/rocket.lnk'
        with open(rocket_link_file, 'r') as f:
            rocket_link = f.read()
        await client.send_message(event.input_sender,
                                  message=rocket_link,
                                  buttons=buttons.keyboard_screener_back)

    elif event.data == b'ticker_news':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(event.input_sender, message=ins.instruction20,
                                  buttons=buttons.keyboard_screener_back)

    # ============================== Основные макро данные =============================
    elif event.data == b'kb_macro_rate':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(entity=entity, message='US interest rate forecast')
        await client.send_file(entity, IMAGES_OUT_PATH + 'Interest Rate.png')
        await client.send_message(event.input_sender, 'Interest Rate \n /instruction10',
                                  buttons=buttons.keyboard_core_macro_back)

    elif event.data == b'kb_macro_inflation':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(entity=entity, message='US inflation forecast')
        await client.send_file(entity, IMAGES_OUT_PATH + 'Inflation Rate.png')
        await client.send_message(event.input_sender, 'Inflation Rate \n /instruction11',
                                  buttons=buttons.keyboard_core_macro_back)

    elif event.data == b'kb_macro_unemployment':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(entity=entity, message='US Unemployment Forecast')
        await client.send_file(entity, IMAGES_OUT_PATH + 'Unemployment Rate.png')
        await client.send_message(event.input_sender, 'Unemployment Rate \n /instruction13',
                                  buttons=buttons.keyboard_core_macro_back)

    elif event.data == b'kb_macro_pmi':
        await event.edit()
        await shared.delete_old_message(client, sender_id)
        await client.send_message(entity=entity, message='US PMI Forecast')
        await client.send_file(entity, IMAGES_OUT_PATH + 'Composite PMI.png')
        await client.send_message(event.input_sender, 'Composite PMI \n /instruction12',
                                  buttons=buttons.keyboard_core_macro_back)

    elif event.data == b'kb_macro_back':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Economic indicators',
                                        buttons=buttons.keyboard_core_macro)
        await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb_us_analysis_up':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'US market analysis',
                                      buttons=buttons.keyboard_a1)
        else:
            msg = await client.send_message(event.input_sender, 'US market analysis',
                                            buttons=buttons.keyboard_a1)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb_macro_up':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Detailed analysis',
                                      buttons=buttons.keyboard_us_market)
        else:
            msg = await client.send_message(event.input_sender, 'Detailed analysis', buttons=buttons.keyboard_us_market)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb_us_market_up':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'US market analysis\n'
                                                                      'При вызове \"Обзора рынка США\" '
                                                                      'списывается 1 запрос🔋',
                                      buttons=buttons.keyboard_us_analysis)
        else:
            msg = await client.send_message(event.input_sender, 'US market analysis\n'
                                                                      'При вызове \"Обзора рынка США\" '
                                                                      'списывается 1 запрос🔋',
                                            buttons=buttons.keyboard_us_analysis)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'screener_back':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Stock screener',
                                      buttons=buttons.keyboard_screener)
        else:
            msg = await client.send_message(event.input_sender, 'Stock screener', buttons=buttons.keyboard_screener)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'hist_back':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'My portfolio\n'
                                                                      'How to buy a portfolio? - /instruction27\n'
                                                                      'Minimum deposit - /mindepo',
                                      buttons=buttons.keyboard_portfolio)
        else:
            msg = await client.send_message(event.input_sender, 'My portfolio\n'
                                                                'How to buy a portfolio? - /instruction27\n'
                                                                'Minimum deposit - /mindepo',
                                            buttons=buttons.keyboard_portfolio)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'kb_3_up':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Historical performance', buttons=buttons.keyboard_historical_tests)
        await shared.save_old_message(sender_id, msg)

    elif event.data == b'portfolio_back':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'My portfolio\n'
                                                                      'How to buy a portfolio? - /instruction27\n'
                                                                      'Minimum deposit - /mindepo',
                                      buttons=buttons.keyboard_portfolio)
        else:
            msg = await client.edit_message(event.input_sender, old_msg_id, 'Your portfolios',
                                            buttons=buttons.keyboard_portfolio)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'friend_back':
        await event.edit()
        # await client.send_message(event.input_sender, 'Profile')
        await menu.profile_menu(event, client, engine=engine)

    elif event.data == b'info_back':
        await event.edit()
        msg = await client.send_message(event.input_sender, 'Information', buttons=buttons.keyboard_info)
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
        await client.send_message(event.input_sender, 'Profile')
        await send_next_profiler_question(client, sender_id, 0)

    elif event.data == b'reset_no':
        await event.edit()
        await menu.profile_menu(event, client, engine=engine)

    elif event.data == b'requests_store':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id,
                                      '🔋 - one request',
                                      buttons=buttons.keyboard_buy_requests)
        else:
            msg = await client.send_message(event.input_sender,
                                            '🔋 - one request',
                                            buttons=buttons.keyboard_buy_requests)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'invite_friends':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id,
                                      'Ты можешь попросить друга запустить бота и получить бесплатную'
                                      ' подписку. '
                                      'Проще всего это сделать через групповые чаты' + '\n' +
                                      f'[https://t.me/UpsilonBot?start={sender_id}]'
                                      f'(https://t.me/UpsilonBot?start={sender_id})',
                                      buttons=buttons.keyboard_friend_back)
        else:
            msg = await client.send_message(event.input_sender,
                                            'Ты можешь попросить друга запустить бота и получить бесплатную'
                                            ' подписку. '
                                            'Проще всего это сделать через групповые чаты' + '\n' +
                                            f'[https://t.me/UpsilonBot?start={sender_id}]'
                                            f'(https://t.me/UpsilonBot?start={sender_id})',
                                            buttons=buttons.keyboard_friend_back)
            await shared.save_old_message(sender_id, msg)
    # ============================== Inspector's Flow ==========================
    elif event.data == b'portfolio_inspector':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id,
                                      'Инспектор портфеля - аналитический тестер, '
                                      'позволяющий определить эффективность портфеля\n\n'
                                      'При использовании инспектора списываются запросы🔋'
                                      'в количестве введенных тикеров\n'
                                      'Размер портфеля не должен превышать 25 тикеров\n\n'                                      
                                      '\U00002757 Как работает инспектор портфелей? - /instruction36',
                                      buttons=buttons.inspector_start)
        else:
            msg = await client.send_message(event.input_sender,
                                            'Инспектор портфеля - аналитический тестер, '
                                            'позволяющий определить эффективность портфеля\n'
                                            'При использовании инспектора списываются запросы🔋'
                                            'в количестве введенных тикеров\n'
                                            'Размер портфеля не должен превышать 25 тикеров\n\n'                                      
                                            '\U00002757 Как работает инспектор портфелей? - /instruction36',
                                            buttons=buttons.inspector_start)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'inspector_start_back':
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Tickers:',
                                      buttons=buttons.keyboard_portfolio)
        else:
            msg = await client.send_message(event.input_sender, 'Tickers:',
                                            buttons=buttons.keyboard_portfolio)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'inspector_start_manual':
        await event.edit()
        shared.set_is_inspector_flow(sender_id, True)
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, ins.inspector_input)
        else:
            msg = await client.send_message(event.input_sender, ins.inspector_input)

            await shared.save_old_message(sender_id, msg)

    elif event.data == b'inspector_next_ok':
        await event.edit()
        ticker, size = shared.get_inspector_ticker(sender_id)
        current_portfolio = shared.get_inspector_portfolio(sender_id)
        income_datetime = await sql.get_income_datetime(sender_id)
        now = datetime.datetime.now()
        is_new_user = True if (now - income_datetime).days < 3 else False
        paid_amount, free_amount = await sql.get_request_amount(sender_id)
        portfolio_size_limit = PORTFOLIO_FREE_SIZE_LIMIT
        message = f'Размер портфеля не должен превышать {portfolio_size_limit} тикеров\n' \
                  f'__Your portfolio сейчас выглядит так:__\n```{current_portfolio}```\n\n' \
                  f'__Выбери действие:__'
        if is_new_user:
            portfolio_size_limit = PORTFOLIO_NEW_USER_SIZE_LIMIT
        if paid_amount > 0:
            portfolio_size_limit = PORTFOLIO_VIP_USER_SIZE_LIMIT
        if current_portfolio is not None and len(current_portfolio) == portfolio_size_limit:
            if old_msg_id is not None:
                await client.edit_message(event.input_sender, old_msg_id,
                                          message,
                                          buttons=buttons.inspector_ends)
            else:
                msg = await client.send_message(event.input_sender, old_msg_id,
                                                message,
                                                buttons=buttons.inspector_ends)
                await shared.save_old_message(sender_id, msg)
            return

        is_first_ticker = shared.update_inspector_portfolio(sender_id, ticker, size)
        if is_first_ticker:
            shared.set_inspector_time(sender_id)
        shared.set_is_inspector_flow(sender_id, True)
        current_portfolio = shared.get_inspector_portfolio(sender_id)
        debug(f'current_portfolio={current_portfolio}')
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id,
                                      f'__Your portfolio сейчас выглядит так:__\n```{current_portfolio}```\n\n'
                                      f'__Введи следующий тикер или выбери действие:__',
                                      buttons=buttons.inspector_ends)
        else:
            msg = await client.send_message(event.input_sender, old_msg_id,
                                            f'__Your portfolio сейчас выглядит так:__\n```{current_portfolio}```\n\n'
                                            f'__Введи следующий тикер или выбери действие:__',
                                            buttons=buttons.inspector_ends)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'inspector_next_edit':
        await event.edit()
        shared.set_is_inspector_flow(sender_id, True)
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, ins.inspector_input)
        else:
            msg = await client.send_message(event.input_sender, ins.inspector_input)

            await shared.save_old_message(sender_id, msg)

    elif event.data == b'inspector_ends_cancel':
        shared.clear_inspectors_data_by_user(sender_id)
        shared.del_is_inspector_flow(sender_id)
        shared.del_inspector_time(sender_id)
        await event.edit()
        if old_msg_id is not None:
            await client.edit_message(event.input_sender, old_msg_id, 'Tickers:',
                                      buttons=buttons.keyboard_portfolio)
        else:
            msg = await client.send_message(event.input_sender, 'Tickers:',
                                            buttons=buttons.keyboard_portfolio)
            await shared.save_old_message(sender_id, msg)

    elif event.data == b'inspector_ends_finish':
        current_portfolio = shared.get_inspector_portfolio(sender_id)
        debug(f'current_portfolio={current_portfolio}')
        first_value = list(current_portfolio.values())[0]
        message = None
        first_int = fast_int(first_value, None)
        if first_int is not None and first_int == 0:
            for k in current_portfolio:
                if fast_int(current_portfolio[k]) != 0:
                    message = f'Если portfolio равновзвешенный, то веса всех акций в портфеле должны быть равны нулю!' \
                          f'__Your portfolio сейчас выглядит так:__\n```{current_portfolio}```\n\n' \
                          f'Необходимо исправить веса, просто введя тикер с некорректным весом снова ' \
                              f'и на этот раз ввести ему вес равный 0!' \

                    break
        elif first_int is not None and first_int != 0:
            for k in current_portfolio:
                if fast_int(current_portfolio[k]) == 0 or current_portfolio[k].endswith('%'):
                    message = f'Если веса активов в портфеле указаны в количестве акций, ' \
                          f'то все веса должны быть указаны в количестве акций!' \
                          f'__Your portfolio сейчас выглядит так:__\n```{current_portfolio}```\n\n' \
                          f'Необходимо исправить веса, просто введя тикер с некорректным весом снова ' \
                              f'и на этот раз ввести ему вес в количестве акций!'
                    break
        elif isinstance(first_value, str) and first_value.endswith('%'):
            total_weight = 0.0
            for k in current_portfolio:
                if not current_portfolio[k].endswith('%'):
                    message = f'Если веса активов в портфеле указаны в процентах, ' \
                          f'то все веса должны быть указаны в процентах!' \
                          f'__Your portfolio сейчас выглядит так:__\n```{current_portfolio}```\n\n' \
                          f'Необходимо исправить веса, просто введя тикер с некорректным весом снова ' \
                              f'и на этот раз ввести ему вес в % !'
                    break
                else:
                    total_weight += fast_float(re.split('%', current_portfolio[k])[0], 0)
            if message is None and total_weight != 100.0:
                message = f'Ошибочный ввод, сумма весов в портфеле не равна 100% !' \
                      f'__Your portfolio сейчас выглядит так:__\n```{current_portfolio}```\n\n' \
                      f'Необходимо исправить веса, просто введя тикер с некорректным весом снова ' \
                          f'и на этот раз ввести ему правильный вес в% !'

        if message is not None:
            shared.set_is_inspector_flow(sender_id, True)
            await event.edit()
            if old_msg_id is not None:
                await client.edit_message(event.input_sender, old_msg_id, message)
            else:
                msg = await client.send_message(event.input_sender, message)
                await shared.save_old_message(sender_id, msg)
            return

        # Подгрузим динамически модуль - вдруг ценообразование изменилось?!
        pricing = None
        if "telegram.pricing" in sys.modules:
            debug(f'module imported --- try reload')
            pricing = importlib.reload(sys.modules["telegram.pricing"])
        else:
            debug(f'module NOT imported --- try first import')
            pricing = importlib.import_module("telegram.pricing")

        pricing_result = await pricing.check_request_amount(event.input_sender.user_id, client, len(current_portfolio))
        if not pricing_result["result"]:
            return

        await shared.delete_old_message(client, sender_id)
        wait_message = await client.send_message(sender_id,
                                                 message=f'Провожу анализ. Это может занять некоторое время.\n'
                                                         f'Дождись ответа, ничего не нажимая! ')
        await shared.save_old_message(sender_id, wait_message)

        filenames = []
        try:
            call = get_inspector_data(current_portfolio)
            filenames, msg = call[0], call[1]
        except Exception as e:
            debug(e, ERROR)
            # вернем баланс в случае если инспектор отработал с ошибкой
            if pricing_result['Paid'] > 0:
                await sql.increment_paid_request_amount(event.input_sender.user_id, pricing_result['Paid'])
            if pricing_result['Free'] > 0:
                await sql.increment_free_request_amount(event.input_sender.user_id, pricing_result['Free'])
            await shared.delete_old_message(client, sender_id)
            await client.send_message(sender_id, message=f'Упс! Что-то пошло не так. '
                                                         f'Опиши баг в "Information" -> "Report a bug"')
            return

        # client.delete_messages(sender_id, message_id)
        await shared.delete_old_message(client, sender_id)
        for filename in filenames:
            if os.path.exists(filename):
                await client.send_file(event.input_sender, filename)
                os.remove(filename)
        await client.send_message(sender_id, message=msg, buttons=buttons.keyboard_0_back)

        # После расчетов и показа всех картинок тоже нужно очистить всю память
        shared.clear_inspectors_data_by_user(sender_id)
        shared.del_is_inspector_flow(sender_id)
        shared.del_inspector_time(sender_id)

<<<<<<< HEAD
    # ============================== Subscriptions =============================
    elif event.data == b'z1':
        await event.edit()
        await client.send_message(event.input_sender, 'Subscription level', buttons=buttons.keyboard_core_subscriptions)
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
                PAYMENT_AGGREGATOR_TIMER = time.time()
            else:
                time.sleep(10 - delta)
                aggregator_status = PAYMENT_AGGREGATOR.get_status()
        else:
            PAYMENT_AGGREGATOR_TIMER = time.time()
            aggregator_status = PAYMENT_AGGREGATOR.get_status()
        # debug(aggregator_status)
        if aggregator_status == 'error':
            # debug("Error description:" + PAYMENT_AGGREGATOR.get_last_error())
            await client.send_message(event.input_sender, 'Oops. Something went wrong.',
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
                                               + 'нажми кнопку Оплатить\n'
                                                 '(Инструкция по оплате [тут](https://telegra.ph/Rrrtt-10-13)! )',
                                               link_preview=True,
                                               buttons=kbd_payment_button)
            await event.edit()
            msg_id = utils.get_message_id(paymsg)
            order_type = 'subscription'
            shared.set_order_data(order_id, sender_id, msg_id, order_type)
            dt = datetime.now()
            dt_int = shared.datetime2int(dt)
            await sql.insert_into_payment_message(order_id, sender_id, msg_id, dt_int, engine)

=======
>>>>>>> 0bb16c110e946b22ebceaa3aef662cb41961d974

async def send_next_profiler_question(client, user_id, curr_num):
    _poll_id = None
    _question = None
    _answers = None
    _poll_id = get_next_id()
    old_msg_id = await shared.get_old_msg_id(user_id)
    if curr_num == 0:
        _question = "Твоя цель:"
        _answers = [PollAnswer("Общее благосостояние", b'1'),
                    PollAnswer("Большие покупки - дом, машина", b'2'),
                    PollAnswer("Учеба детей, свадьба", b'3'),
                    PollAnswer("Пенсия", b'4'),
                    PollAnswer("Пассивный доход", b'5')]
    if curr_num == 1:
        _question = "Что из перечисленного описывает твою ситуацию:"
        _answers = [PollAnswer('Я резидент СНГ, мой брокер из СНГ', b'1'),
                    PollAnswer('Я резидент СНГ, мой брокер из ЕС', b'2'),
                    PollAnswer('Я резидент СНГ, мой брокер из США', b'3'),
                    PollAnswer('Я резидент ЕС, мой брокер из США', b'4'),
                    PollAnswer('Я резидент ЕС, мой брокер из ЕС', b'5'),
                    PollAnswer('Я резидент США, мой брокер из США', b'6'),
                    PollAnswer('У меня нет брокерского счета и я резидент СНГ', b'7')]
    if curr_num == 2:
        _question = "Если у тебя есть брокерский счет, можешь ли ты покупать Американские ETF-фонды?"
        _answers = [PollAnswer('Да', b'1'),
                    PollAnswer('Нет', b'2'),
                    PollAnswer('Не знаю', b'3')]
    if curr_num == 3:
        _question = "Ты хочешь инвестировать свободные средства или они могут вскоре понадобиться?"
        _answers = [PollAnswer('Да, эти средства могут понадобиться', b'1'),
                    PollAnswer('Нет, это свободные средства', b'2')]
    if curr_num == 4:
        _question = "Планируешь ли ты выводить деньги с брокерского счета?"
        _answers = [PollAnswer('Да, регулярно', b'1'),
                    PollAnswer('Иногда, по случаю', b'2'),
                    PollAnswer('Нет', b'3')]
    if curr_num == 5:
        _question = "Будешь ли ты делать дополнительные вложения?"
        _answers = [PollAnswer('Да, регулярно', b'1'),
                    PollAnswer('Иногда, по случаю', b'2'),
                    PollAnswer('Дополнительных вложений не планирую', b'3')]
    if curr_num == 6:
        _question = "Срок вложений:"
        _answers = [PollAnswer('Меньше года', b'1'),
                    PollAnswer('1-3 года', b'2'),
                    PollAnswer('3-5 лет', b'3'),
                    PollAnswer('5-10 лет', b'4'),
                    PollAnswer('Более 10 лет', b'5')]
    if curr_num == 7:
        _question = "Как часто ты будешь заниматься портфелем?"
        _answers = [PollAnswer('Ежедневно', b'1'),
                    PollAnswer('Ежемесячно', b'2'),
                    PollAnswer('Когда нужно', b'3'),
                    PollAnswer('По случаю', b'4')]
    if curr_num == 8:
        _question = "Какую доходность ожидаешь?"
        _answers = [PollAnswer('Выше уровня инфляции', b'1'),
                    PollAnswer('10%', b'2'),
                    PollAnswer('10-15%', b'3'),
                    PollAnswer('15-20%', b'4'),
                    PollAnswer('Более 20%', b'5')]
    if curr_num == 9:
        _question = "Потеря какой части твоего вклада будет катастрофической?"
        _answers = [PollAnswer('От -5% до -10%', b'1'),
                    PollAnswer('От -10% до -20%', b'2'),
                    PollAnswer('От -20% до -35%', b'3'),
                    PollAnswer('От -35% до -50%', b'4'),
                    PollAnswer('До -75', b'5')]
    if curr_num == 10:
        _question = "Убыток в 20% от размера твоего вклада это:"
        _answers = [PollAnswer('Ничего страшного', b'1'),
                    PollAnswer('Терпимо', b'2'),
                    PollAnswer('Не приемлемо', b'3')]
    if curr_num == 11:
        _question = "Твои действия во время просадки на рынке в 15%:"
        _answers = [PollAnswer('Не знаю', b'1'),
                    PollAnswer('Ничего не сделаю', b'2'),
                    PollAnswer('Продам все', b'3'),
                    PollAnswer('Продам часть', b'4'),
                    PollAnswer('Продам убыточные', b'5'),
                    PollAnswer('Продам прибыльные', b'6'),
                    PollAnswer('Докуплю', b'7'),
                    PollAnswer('Что-то продам и что-то докуплю', b'8')]
    if curr_num == 12:
        _question = "Ты предпочел бы акции:"
        _answers = [PollAnswer('С доходностью в 20% годовых, но ранее эти акции падали на -50%', b'1'),
                    PollAnswer('С доходностью в 15% годовых, но ранее эти акции падали на -20%', b'2'),
                    PollAnswer('С доходностью в 150% годовых, но ранее эти акции падали на -70%', b'3'),
                    PollAnswer('С доходностью в 10% годовых, но ранее эти акции падали на -10%', b'4')]
    if curr_num == 13:
        _question = "Ты предпочитаешь:"
        _answers = [PollAnswer('Гарантированные 50% от твоей суммы через 3 года', b'1'),
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


async def polls_handler(update, client):
    poll_id = getattr(update, "poll_id", None)
    if not poll_id:
        return
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
                main_menu_msg = await client.send_message(user_id, '📁 Main menu', buttons=buttons.keyboard_0)
                await shared.save_old_message(user_id, main_menu_msg)
            else:
                menu_msg = await client.send_message(user_id, '📁 Main menu', buttons=buttons.keyboard_0)
                await shared.delete_old_message(client, user_id)
                await shared.save_old_message(user_id, menu_msg)
    else:
        user_id, msg_id = get_userid_by_broadcastpollid(poll_id)
        if user_id is not None:
            sentusrdict, failusrdict, pollresult = get_mailing_data(msg_id)
            votes_list = update.results.results
            if len(pollresult) == 0:
                for count, vote in enumerate(votes_list, start=1):
                    pollresult[str(count)] = 1 if vote.voters == 1 else 0
            else:
                for count, vote in enumerate(votes_list, start=1):
                    if vote.voters == 1:
                        pollresult[str(count)] += 1
            update_mailing_lists(msg_id, sentusrdict, failusrdict, pollresult)


async def my_strategies_dynamic_menu(event, client, sender_id, old_msg_id):
    # Если клиент не до конца прошел профалинг
    # - показываем кнопку определить свой Profile
    if old_msg_id is not None:
        if str(sender_id) in OWNERS:
            await client.edit_message(event.input_sender, old_msg_id,
                                      'Your portfolio', buttons=buttons.risk_profile_owner)
        else:
            if not is_user_profile_done(sender_id):
                await client.edit_message(event.input_sender, old_msg_id,
                                          'Define your Risk Profile', buttons=buttons.keyboard_restart_poll)
            else:
                final_profile_score = get_final_score(sender_id)
                if final_profile_score <= -9:
                    await client.edit_message(event.input_sender, old_msg_id,
                                              'Your portfolio', buttons=buttons.risk_profile1)
                elif -9 < final_profile_score <= -4:
                    await client.edit_message(event.input_sender, old_msg_id,
                                              'Your portfolios', buttons=buttons.risk_profile2)
                elif -4 < final_profile_score <= 1:
                    await client.edit_message(event.input_sender, old_msg_id,
                                              'Your portfolios', buttons=buttons.risk_profile3)
                elif 1 < final_profile_score < 6:
                    await client.edit_message(event.input_sender, old_msg_id,
                                              'Your portfolio', buttons=buttons.risk_profile4)
                elif 6 <= final_profile_score < 10:
                    await client.edit_message(event.input_sender, old_msg_id,
                                              'Your portfolios', buttons=buttons.risk_profile5)
                elif final_profile_score >= 10:
                    await client.edit_message(event.input_sender, old_msg_id,
                                              'Your portfolios', buttons=buttons.risk_profile6)
    else:
        msg = None
        if str(sender_id) in OWNERS:
            msg = await client.send_message(event.input_sender,
                                            'Your portfolio', buttons=buttons.risk_profile_owner)
        else:
            final_profile_score = get_final_score(sender_id)
            if not is_user_profile_done(sender_id):
                msg = await client.send_message(event.input_sender,
                                                'Define your Risk Profile', buttons=buttons.keyboard_restart_poll)
            else:
                if final_profile_score <= -9:
                    msg = await client.send_message(event.input_sender,
                                                    'Your portfolio', buttons=buttons.risk_profile1)
                elif -9 < final_profile_score <= -4:
                    msg = await client.send_message(event.input_sender,
                                                    'Your portfolios', buttons=buttons.risk_profile2)
                elif -4 < final_profile_score <= 1:
                    msg = await client.send_message(event.input_sender,
                                                    'Your portfolios', buttons=buttons.risk_profile3)
                elif 1 < final_profile_score < 6:
                    msg = await client.send_message(event.input_sender,
                                                    'Your portfolio', buttons=buttons.risk_profile4)
                elif 6 <= final_profile_score < 10:
                    msg = await client.send_message(event.input_sender,
                                                    'Your portfolios', buttons=buttons.risk_profile5)
                elif final_profile_score >= 10:
                    msg = await client.send_message(event.input_sender,
                                                    'Your portfolios', buttons=buttons.risk_profile6)
        await shared.save_old_message(sender_id, msg)


# provider_token = '381764678:TEST:25868'  # ЮКасса Тест
provider_token = '390540012:LIVE:17289' #ЮКасса реал


# let's put it in one function for more easier way
def generate_invoice(price_label: str, price_amount: int, currency: str, title: str,
                     description: str, payload: str, start_param: str) -> types.InputMediaInvoice:
    price = types.LabeledPrice(label=price_label, amount=price_amount)  # label - just a text, amount=10000 means 100.00
    invoice = types.Invoice(
        currency=currency,  # currency like USD
        prices=[price],  # there could be a couple of prices.
        test=True,  # if you're working with test token, else set test=False.
        # More info at https://core.telegram.org/bots/payments

        # params for requesting specific fields
        name_requested=False,
        phone_requested=False,
        email_requested=True,
        shipping_address_requested=False,

        # if price changes depending on shipping
        flexible=False,

        # send data to provider
        phone_to_provider=False,
        email_to_provider=False
    )
    return types.InputMediaInvoice(
        title=title,
        description=description,
        invoice=invoice,
        payload=payload.encode('UTF-8'),  # payload, which will be sent to next 2 handlers
        provider=provider_token,

        provider_data=types.DataJSON('{'
                                        '"need_email": true,'
                                        '"send_email_to_provider": true,'
                                        '"provider_data":{'
                                            '"receipt": {'
                                                '"items": ['
                                                    '{'
                                                        f'"description": "{description}",'
                                                        '"quantity": "1.00",'
                                                        '"amount": {'
                                                            f'"value": "{float(price_amount/100)}",'
                                                            '"currency": "RUB"'
                                                        '},'
                                                        '"vat_code": 1'
                                                    '}'
                                                ']'
                                            '}'
                                        '}'
                                     '}'),
        # data about the invoice, which will be shared with the payment provider. A detailed description of
        # required fields should be provided by the payment provider.

        start_param=start_param,
        # Unique deep-linking parameter. May also be used in UpdateBotPrecheckoutQuery
        # see: https://core.telegram.org/bots#deep-linking
        # it may be the empty string if not needed

    )


async def make_payment(event, client_, request_amount, summ, order_type):
    if summ is None or summ <= 0.0:
        debug(f'Упс. Нажали донат {summ}. Но что-топошло не так')
        return

    await event.edit()
    sender_id = event.original_update.user_id
    old_msg_id = await shared.get_old_msg_id(sender_id)

    order_id = str(uuid.uuid4()).replace('-', '')

    debug(f"User_id={sender_id} -- OrderId:{order_id} -- Summa: {summ} -- request_amount = {request_amount}")

    kbd_payment_button = buttons.generate_payment_button(summ, order_type, sender_id)

    if old_msg_id is not None:
        await client_.edit_message(event.input_sender, old_msg_id,
                                   'Для оплаты нажми кнопку', buttons=kbd_payment_button)
    else:
        paymsg = await client_.send_message(event.input_sender,
                                            'Для оплаты нажми кнопку', buttons=kbd_payment_button)
        await shared.save_old_message(sender_id, paymsg)
    make_payment.order_type = order_type
    make_payment.order_id = order_id
    make_payment.request_amount = request_amount
    make_payment.summ = summ


async def send_invoice(client, event):
    await event.edit()
    sender_id = event.original_update.user_id
    old_msg_id = await shared.get_old_msg_id(sender_id)
    await shared.delete_old_message(client, sender_id)
    order_type = getattr(make_payment, 'order_type', None) or None
    order_id = getattr(make_payment, 'order_id', None) or None
    summ = getattr(make_payment, 'summ', None) or None
    request_amount = getattr(make_payment, 'request_amount', None)
    debug(f'make_payment.order_type ={order_type}')
    debug(f'make_payment.order_id ={order_id}')
    debug(f'make_payment.summ ={summ}')
    debug(f'make_payment.request_amount ={request_amount}')
    currency = 'RUB=X'
    last_currency_price = fast_float(sql_q.get_last_currency_price(currency), 73.0)
    debug(f'RUB=X last_price ={last_currency_price}')
    summa = fast_int(summ*100*last_currency_price)
    payload = {'s_i': sender_id,
               'o_t': order_type,
               'o_i': order_id,
               'r_a': request_amount,
               's': summ}
    imi = None
    if order_type == 'replenishment':
        imi = generate_invoice(price_label=f'{request_amount} запросов',
                               price_amount=summa,
                               currency='RUB',
                               title=f'Покупка {request_amount} запросов',
                               description='Покупая запросы, вы приобретаете доступ к внутренней базе данных '
                                           'Ипсилона и приоритет в доступе к любым текущим и будущим данным бота.',
                               payload=json.dumps(payload),
                               start_param='123e')
    elif order_type == 'donate':
        imi = generate_invoice(price_label=f'Пожертвование',
                               price_amount=summa,
                               currency='RUB',
                               title=f'Пожертвование!',
                               description='На поддержку перспективного, быстро развивающегося и вообще '
                                           'классного бота!',
                               payload=json.dumps(payload),
                               start_param='123e')

    await client.send_message(event.chat_id, '', file=imi)

# elif event.data == b'a1a4':
#     await event.edit()
#     message = await client.send_message(entity=entity, message='Loading...')
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

# elif event.data == b'a2a2':
#     await event.edit()
#     message = await client.send_message(entity=entity, message='Loading...')
#     await client.edit_message(message, 'Оценка/аудит портфеля')
#     await client.send_message(event.input_sender, 'Зачем проводить аудит своего портфеля? /instruction04',
#                               buttons=buttons.keyboard_a2_back)

# elif event.data == b'sac1':
#     await event.edit()
#     message = await client.send_message(entity=entity, message='Loading...')
#     await client.edit_message(message, 'Detailed statistics')
#     await client.send_file(entity, STATS_PATH + 'sac_parking.pdf')
#     await client.send_message(event.input_sender, 'О доверительном управлении \n'
#                                                   '/instruction26',
#                               buttons=buttons.keyboard_managed_strategies)
#
# elif event.data == b'sac2':
#     await event.edit()
#     message = await client.send_message(entity=entity, message='Loading...')
#     await client.edit_message(message, 'Detailed statistics')
#     await client.send_file(entity, STATS_PATH + 'sac_balanced.pdf')
#     await client.send_message(event.input_sender, 'О доверительном управлении \n'
#                                                   '/instruction26',
#                               buttons=buttons.keyboard_managed_strategies)
#
# elif event.data == b'sac3':
#     await event.edit()
#     message = await client.send_message(entity=entity, message='Loading...')
#     await client.edit_message(message, 'Detailed statistics')
#     await client.send_file(entity, STATS_PATH + 'sac_growth.pdf')
#     await client.send_message(event.input_sender, 'О доверительном управлении \n'
#                                                   '/instruction26',
#                               buttons=buttons.keyboard_managed_strategies)

# ============================== Образовательные программы =============================
# elif event.data == b'a6a1':
#     await event.edit()
#     message = await client.send_message(entity=entity, message='Loading...')
#     await client.edit_message(message, 'Основы инвестирования')
#     await client.send_message(event.input_sender, 'Основы инвестирования /instruction20',
#                               buttons=buttons.keyboard_a6_back)
# elif event.data == b'a6a2':
#     await event.edit()
#     message = await client.send_message(entity=entity, message='Loading...')
#     await client.edit_message(message, 'Как собрать свой первый portfolio')
#     await client.send_message(event.input_sender, 'Как собрать свой первый portfolio /instruction21',
#                               buttons=buttons.keyboard_a6_back)
# elif event.data == b'a6a3':
#     await event.edit()
#     message = await client.send_message(entity=entity, message='Loading...')
#     await client.edit_message(message, 'Профессиональные решения')
#     await client.send_message(event.input_sender, 'Профессиональные решения /instruction22',
#                               buttons=buttons.keyboard_a6_back)
# elif event.data == b'a6a-1':
#     await event.edit()
#     await client.send_message(event.input_sender, 'Образование', buttons=buttons.keyboard_a6)

# ============================== Агрегатор новостей =============================
# elif event.data == b'cm-6':
#     await event.edit()

#     msg = await client.send_message(event.input_sender, 'Сотрудничество', buttons=buttons.keyboard_relations)
#     await shared.save_old_message(sender_id, msg)
    # elif event.data == b'us7':
    #     await event.edit()
    #     await shared.delete_old_message(client, sender_id)
    #     message = await client.send_message(entity=entity, message='Loading...')
    #     await client.edit_message(message, 'Ключевые статистики акций компании')
    #     await client.send_message(entity=entity, message=ins.instruction21)
    #     await client.send_message(event.input_sender, 'Как интерпретировать ключевые статистики? \n'
    #                                                   '/instruction22',
    #                               buttons=buttons.keyboard_us_market_back)
