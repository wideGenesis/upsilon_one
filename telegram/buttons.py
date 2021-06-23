from telethon.tl.custom import Button
from project_shared import *
from random import choice



keyboard_start = [
    [Button.text('\U0001F4C1 Main menu', resize=True)],
    [Button.text('\U0001F464 Profile', resize=True), Button.text('\U0001F6CE Information', resize=True)]
]

# Кнопки вперед для презентации
keyboard_forw2 = [
    [
        Button.inline('\U000027A1  ' + 'Next', b'forw2')
    ]
]

keyboard_forw3 = [
    [
        Button.inline('\U000027A1  ' + 'Next', b'forw3')
    ]
]

keyboard_forw4 = [
    [
        Button.inline('\U000027A1  ' + 'Next', b'forw4')
    ]
]

keyboard_forw5 = [
    [
        Button.inline('\U000027A1  ' + 'Next', b'forw5')
    ]
]

keyboard_forw6 = [
    [
        Button.inline('\U000027A1  ' + 'Next', b'forw6')
    ]
]

keyboard_forw7 = [
    [
        Button.inline('\U000027A1  ' + 'Next', b'forw7')
    ]
]

keyboard_forw7a = [
    [
        Button.inline('\U000027A1  ' + 'Next', b'forw7a')
    ]
]

keyboard_forw8 = [
    [
        Button.inline('\U000027A1  ' + 'Next', b'forw8')
    ]
]

keyboard_forw9 = [
    [
        Button.inline('\U0001F3AF  ' + 'Choose an investment solution', b'forw9')
    ]
]

keyboard_0 = [
    [
        Button.inline('\U0001F52C   ' + 'Market Analysis', b'kb0_market_analysis')
    ],
    [
        Button.inline('\U0001F4BC   ' + 'My Portfolio', b'kb0_my_portfolio')
    ],
    [
        Button.inline('\U0001F9EC   ' + 'Stock Screener', b'kb0_stock_screener')
    ],
    [
        Button.inline('\U0001F4F0   ' + 'News Feed', b'kb0_news_feed')
    ],
    [
        Button.inline('\U0001F64F  ' + 'Donate', b'kb0_donate')
    ]

]

keyboard_0_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'main')
    ]
]

keyboard_a1 = [
    [
        Button.inline('🇺🇸' + 'Stock Market', b'kb_a1_us_market')
    ],
    [
        Button.inline('\U0001F510  ' + 'Cryptocurrency market', b'kb_a1_coin_market')
    ],
    # [
    #     Button.inline('\U0001F43B  ' + 'Рынок РФ', b'kb_a1_rus_market')
    # ],
    [
        Button.inline('🇺🇳' + 'Global markets', b'kb_a1_world_markets')
    ],
    # [
    #     Button.inline('\U0001F30D  ' + 'Market Valuation', b'a1a13')
    # ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'main')
    ]
]

keyboard_a1_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'kb_a1_back')
    ]
]

keyboard_historical_tests = [
    [
        Button.inline('\U0001F4BC  ' + 'Parking', b'hist_parking')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Weather', b'hist_allweather')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Conservative', b'hist_balanced')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Aggressive', b'hist_agg')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Leveraged', b'hist_lev')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Elastic (stocks only)', b'hist_elastic')
    ],
    # [
    #     Button.inline('\U0001F4BC  ' + 'Yolo (spbexchange)', b'hist_yolo')
    # ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons S', b'hist_allseasons_s')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons M', b'hist_allseasons_m')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons L', b'hist_allseasons_l')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'hist_back')
    ]
]

keyboard_a3_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'kb_3_up')
    ]
]

keyboard_a8 = [
    [
        Button.inline('\U0001F5DE  ' + 'Market News', b'kb_a8_market_news')
    ],
    [
        Button.inline('\U0001F4B1   ' + 'Articles', b'kb_a8_analytical_blogs')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'main')
    ]
]

keyboard_a8_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'kb_a8_back')
    ]
]

keyboard_core_macro = [
    [
        Button.inline('\U0001F3E6  ' + 'Interest Rate', b'kb_macro_rate')
    ],
    [
        Button.inline('\U0001F321   ' + 'Inflation Rate', b'kb_macro_inflation')
    ],
    [
        Button.inline('\U0001F525   ' + 'Unemployment Rate', b'kb_macro_unemployment')
    ],
    [
        Button.inline('\U0001F3E2   ' + 'United States PMI', b'kb_macro_pmi')
    ],
    [
        Button.inline('\U0001F519   ' + 'Back', b'kb_macro_up')
    ]
]

keyboard_core_macro_back = [
    [
        Button.inline('\U0001F519   ' + 'Back', b'kb_macro_back')
    ]
]

keyboard_us_market = [
    [
        Button.inline('\U0001F503   ' + 'Advances/Declines', b'kb_us_market_adl')
    ],
    [
        Button.inline('\U00002197   ' + 'Momentum', b'kb_us_market_mom')
    ],
    [
        Button.inline('\U0001F4E3	' + 'US Economic Indicators', b'kb_us_market_macro_forecast')
    ],
    [
        Button.inline('\U0001F4C9   ' + 'Volatility Structure', b'kb_us_market_vol_curve')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'kb_us_market_up')
    ]
]

keyboard_us_market_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'kb_macro_up')
    ]
]

keyboard_us_analysis = [
    [
        Button.inline('\U0001F3AF  ' + 'Stock Market Overview', b'kb_us_analysis_overview')
    ],
    [
        Button.inline('\U0001F9E9  ' + 'Detailed Analysis', b'kb_us_analysis_insideview')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'kb_us_analysis_up')
    ]
]

keyboard_us_analysis_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'kb_us_market_up')
    ]
]

keyboard_portfolio = [
    [
        Button.inline('🔮  ' + 'Portfolio inspector', b'portfolio_inspector')
    ],
    [
        Button.inline('\U0001F9F0  ' + 'My strategies', b'my_strategies')
    ],
    [
        Button.inline('\U000026F3  ' + 'Historical performance', b'historical_tests')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'main')
    ]
]

keyboard_portfolio_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'portfolio_back')
    ]
]

keyboard_screener = [
    [
        Button.inline('\U0001F4B9  ' + 'Financial Analysis', b'financial_analysis')
    ],
    [
        Button.inline('🎩  ' + 'TOP-50 guru stocks', b'top_gurus')
    ],
    [
        Button.inline('🐹  ' + 'TOP-50 cheap stocks', b'top_cheap')
    ],
    [
        Button.inline('\U0001F9E8  ' + 'Companies news', b'ticker_news')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'main')
    ]
]

keyboard_screener_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'screener_back')
    ]
]

keyboard_info = [
    # [
    #     Button.inline('\U00002696   ' + 'Сравнение брокеров', b'brokers_compare')
    # ],
    [
        Button.inline('\U000026D1   ' + 'Instructions', b'instructions')
    ],
    # [
    #     Button.inline('\U0001F6E1   ' + 'Регистрация управляющего', b'manager_registration')
    # ],
    [
        Button.inline('\U0001F4EC  ' + 'Offers and advertisements', b'advertisement')
    ],
    [
        Button.inline('\U000026A0   ' + 'Report a bug', b'bug_report')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'main')
    ]
]

keyboard_info_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'info_back')
    ]
]

keyboard_reset = [
    [
        Button.inline('\U00002049   ' + 'OK', b'reset_yes')
    ],
    [
        Button.inline('\U0001F519   ' + 'Cancel', b'reset_no')
    ]
]

keyboard_restart_poll = [
    [
        Button.inline('\U0001F6A9   ' + 'Define a risk profile', b'risk_profile_restart')
    ]
]

# ============================== Кнопки донатов =============================
keyboard_donate = [
    [
        Button.inline('\U0001F949   ' + '2$', b'donate2')
    ],
    [
        Button.inline('\U0001F948   ' + '5$', b'donate5')
    ],
    [
        Button.inline('\U0001F947	   ' + '10$', b'donate10')
    ],
    [
        Button.inline('\U0001F3C5	   ' + '50$', b'donate50')
    ],
    [
        Button.inline('\U0001F451   ' + '100$', b'donate100')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'main')
    ]
]


# ============================== Кнопки покупки запросов =============================
keyboard_buy_requests = [
    [
        Button.inline('33 🔋', b'buy_requests5'),
        Button.inline('67 🔋', b'buy_requests10')
    ],
    [
        Button.inline('143 🔋 (6% 🎁)', b'buy_requests20'),
        Button.inline('417 🔋 (20% 🎁)', b'buy_requests50')
    ],
    [
        Button.inline('1000 🔋 (33% 🎁)', b'buy_requests100'),
        Button.inline('1875 🔋 (46% 🎁)', b'buy_requests150')
    ],
    [
        Button.inline('3333 🔋 (60% 🎁)', b'buy_requests200'),
        Button.inline('7500 🔋 (73% 🎁)', b'buy_requests300')
    ],
    [
        Button.inline('\U0001F519   ' + 'Back', b'main')
    ]
]


<<<<<<< HEAD
# ============================== Кнопки подписок =============================
# keyboard_core_subscriptions = [
#     [
#         Button.inline('\U0001F46E  ' + 'Сравнение тарифов', b'kcs0')
#     ],
#     [
#         Button.inline('\U0001F3E6  ' + 'Старт', b'kcs1')
#     ],
#     [
#         Button.inline('\U0001F321	  ' + 'Базовый', b'kcs2')
#     ],
#     [
#         Button.inline('\U0001F525  ' + 'Продвинутый', b'kcs3')
#     ],
#     [
#         Button.inline('\U0001F3E2  ' + 'Профессиональный', b'kcs4')
#     ],
#     [
#         Button.inline('\U0001F519  ' + 'Back', b'kcs-1')
#     ]
# ]

keyboard_subscription_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'kcs-1')
    ]
]

keyboard_subscription_start = [
    [
        Button.inline('\U0001F3E6  ' + '$15', b'kss1')
    ]
]

keyboard_subscription_base = [
    [
        Button.inline('\U0001F3E6  ' + '$25', b'kss2')
    ]
]

keyboard_subscription_advanced = [
    [
        Button.inline('\U0001F3E6  ' + '$30', b'kss3')
    ]
]

keyboard_subscription_professional = [
    [
        Button.inline('\U0001F3E6  ' + '$40', b'kss4')
    ]
]


=======
>>>>>>> 0bb16c110e946b22ebceaa3aef662cb41961d974
def generate_payment_button(summ=None, order_type=None, sender_id=None):
    keyboard_subscr_start_inst = []
    if order_type == 'donate':
        keyboard_subscr_start_inst = [
            [
                Button.inline(f'\U0001F3E6  Checkout ( ${summ} )', b'inline_donate')
            ],
            [
                Button.inline(f'\U0001F519  Back', b'donate_back')
            ]
        ]
    elif order_type == 'replenishment':
        keyboard_subscr_start_inst = [
            [
                Button.inline(f'\U0001F3E6  Checkout ( ${summ} )', b'inline_payment')
            ],
            [
                Button.inline(f'\U0001F519  Back', b'payment_back')
            ]
        ]
    return keyboard_subscr_start_inst


keyboard_friend_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'friend_back')
    ]
]

# ============= Кнопки для меню мои стратегии =============
risk_profile1 = [
    [
        Button.inline('\U0001F4BC  ' + 'Parking', b'strategy_parking')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons S', b'strategy_allseasons_s')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'portfolio_back')
    ]
]

risk_profile2 = [
    [
        Button.inline('\U0001F4BC  ' + 'Parking', b'strategy_parking')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Weather', b'strategy_allweather')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons M', b'strategy_allseasons_m')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'portfolio_back')
    ]
]

risk_profile3 = [
    [
        Button.inline('\U0001F4BC  ' + 'All Weather', b'strategy_allweather')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Conservative', b'strategy_balanced')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons M', b'strategy_allseasons_m')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'portfolio_back')
    ]
]

risk_profile4 = [
    [
        Button.inline('\U0001F4BC  ' + 'Conservative', b'strategy_balanced')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons L', b'strategy_allseasons_l')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'portfolio_back')
    ]
]

risk_profile5 = [
    [
        Button.inline('\U0001F4BC  ' + 'Conservative', b'strategy_balanced')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Aggressive', b'strategy_aggressive')
    ],
    # [
    #     Button.inline('\U0001F4BC  ' + 'Yolo', b'strategy_yolo')
    # ],
    [
        Button.inline('\U0001F4BC  ' + 'Elastic', b'strategy_elastic')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'portfolio_back')
    ]
]

risk_profile6 = [
    [
        Button.inline('\U0001F4BC  ' + 'Aggressive', b'strategy_aggressive')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Leveraged', b'strategy_leveraged')
    ],
    # [
    #     Button.inline('\U0001F4BC  ' + 'Yolo', b'strategy_yolo')
    # ],
    [
        Button.inline('\U0001F4BC  ' + 'Elastic', b'strategy_elastic')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'portfolio_back')
    ]
]

risk_profile_owner = [
    [
        Button.inline('\U0001F4BC  ' + 'Parking', b'strategy_parking')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Weather', b'strategy_allweather')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Conservative', b'strategy_balanced')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Aggressive', b'strategy_aggressive')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Leveraged', b'strategy_leveraged')
    ],
    # [
    #     Button.inline('\U0001F4BC  ' + 'Yolo', b'strategy_yolo')
    # ],
    [
        Button.inline('\U0001F4BC  ' + 'Elastic', b'strategy_elastic')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons S', b'strategy_allseasons_s')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons M', b'strategy_allseasons_m')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons L', b'strategy_allseasons_l')
    ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'portfolio_back')
    ]
]

my_strategies_back = [
    [
        Button.inline('\U0001F519  ' + 'Back', b'strategies_back')
    ]
]


# ============= Кнопки Инспектора =============
inspector_start = [
    [
        Button.inline('⌨  ' + 'Tickers:', b'inspector_start_manual')
    ],
    # [
    #     Button.inline('\U0001F4BC  ' + 'Загрузить csv-файл', b'inspector_start_csv')
    # ],
    [
        Button.inline('\U0001F519  ' + 'Back', b'inspector_start_back')
    ]
]

inspector_next = [
    [
        Button.inline('✅  ' + 'OK', b'inspector_next_ok'),
        Button.inline('🔄  ' + 'Edit', b'inspector_next_edit')
    ],

]

inspector_error = [
    [
        Button.inline('🔄  ' + 'Edit', b'inspector_next_edit')
    ],
]

inspector_ends = [
    [
        Button.inline('🏁  ' + 'Start analysis', b'inspector_ends_finish')
    ],
    [
        Button.inline('🗑  ' + 'Cancel. Quit', b'inspector_ends_cancel')
    ]
]


# keyboard_managed_strategies = [
#     [
#         Button.inline('\U0001F3E6  ' + 'Parking портфель', b'sac1')
#     ],
#     [
#         Button.inline('\U0001F3E6  ' + 'Conservative портфель', b'sac2')
#     ],
#     [
#         Button.inline('\U0001F3E6  ' + 'Aggressive', b'sac3')
#     ],
#     [
#         Button.inline('\U0001F519  ' + 'Back', b'sacback')
#     ]
# ]

# keyboard_a2_back = [
#     [
#         Button.inline('\U0001F519  ' + 'Back', b'cm-5')
#     ]
# ]
#
# keyboard_a5 = [
#     # [
#     #     Button.inline('\U0001F50D   ' + 'Как ... /instruction01', b'a5a1')
#     # ],
#     # [
#     #     Button.inline('\U0001F50D   ' + 'Что ... /instruction02', b'a5a2')
#     # ],
#     [
#         Button.inline('\U0001F519  ' + 'Back', b'main')
#     ]
# ]

# keyboard_a5_back = [
#     [
#         Button.inline('\U0001F519  ' + 'Back', b'a5a-1')
#     ]
# ]

# keyboard_a6 = [
#     [
#         Button.inline('\U0001F476   ' + 'Мониторинг стратегий', b'a6a1')
#     ],
#     [
#         Button.inline('\U0001F468  ' + 'Исторические тесты', b'a6a2')
#     ],
#     [
#         Button.inline('\U0001F9D4  ' + 'Трекинг личного портфеля', b'a6a3')
#     ],
#     [
#         Button.inline('\U0001F519  ' + 'Back', b'main')
#     ]
# ]

# keyboard_a6_back = [
#     [
#         Button.inline('\U0001F519  ' + 'Back', b'a6a-1')
#     ]
# ]

# keyboard_a7 = [
#     [
#         Button.inline('\U0001F5DC  ' + 'Финансовый анализ', b'a7a1')
#     ],
#     [
#         Button.inline('\U0001F46E  ' + 'Подробный анализ и скоринг', b'a7a2')
#     ],
#     [
#         Button.inline('\U0001F46E  ' + 'Сводка новостей', b'a7a3')
#     ],
#     [
#         Button.inline('\U0001F519  ' + 'Back', b'main')
#     ]
# ]

# keyboard_a7_back = [
#     [
#         Button.inline('\U0001F519  ' + 'Back', b'a7a-1')
#     ]
# ]
