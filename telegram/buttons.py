from telethon.tl.custom import Button
from project_shared import *
from random import choice

# lol = ['Подача напитков из улиток', 'Мыло \"Кот Да Винчи\"', 'Гос реестр порно', 'Орден Финансового Лосся',
#        'Шопот крыш', 'Отделение пластики мозга', 'Моргаем диафрагмой', 'Мастерская \"Парики Трампа\"',
#        'Бар \"Финансовое воздержание\"']

keyboard_start = [
    [Button.text('\U0001F4C1 Главное меню', resize=True)],
    [Button.text('\U0001F464 Профиль', resize=True), Button.text('\U0001F6CE Информация', resize=True)]
]

# Кнопки вперед для презентации
keyboard_forw2 = [
    [
        Button.inline('\U000027A1  ' + 'Далее', b'forw2')
    ]
]

keyboard_forw3 = [
    [
        Button.inline('\U000027A1  ' + 'Далее', b'forw3')
    ]
]

keyboard_forw4 = [
    [
        Button.inline('\U000027A1  ' + 'Далее', b'forw4')
    ]
]

keyboard_forw5 = [
    [
        Button.inline('\U000027A1  ' + 'Далее', b'forw5')
    ]
]

keyboard_forw6 = [
    [
        Button.inline('\U000027A1  ' + 'Далее', b'forw6')
    ]
]

keyboard_forw7 = [
    [
        Button.inline('\U000027A1  ' + 'Далее', b'forw7')
    ]
]

keyboard_forw7a = [
    [
        Button.inline('\U000027A1  ' + 'Далее', b'forw7a')
    ]
]

keyboard_forw8 = [
    [
        Button.inline('\U000027A1  ' + 'Далее', b'forw8')
    ]
]

keyboard_forw9 = [
    [
        Button.inline('\U0001F3AF  ' + 'Подобрать инвестиционое решение', b'forw9')
    ]
]

keyboard_0 = [
    [
        Button.inline('\U0001F52C   ' + 'Анализ рынков', b'a1')
    ],
    [
        Button.inline('\U0001F4BC   ' + 'Мой портфель', b'my_portfolio')
    ],
    [
        Button.inline('\U0001F9EC   ' + 'Скринер акций', b'a3')
    ],
    [
        Button.inline('\U0001F4F0   ' + 'Лента новостей', b'a8')
    ],
    [
        Button.inline('\U0001F64F  ' + 'Donate', b'donate')
    ]

]

keyboard_0_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a1 = [
    [
        Button.inline('🇺🇸' + 'Рынок США', b'a1a1')
    ],
    [
        Button.inline('\U0001F510  ' + 'Рынок криптовалют', b'a1a2')
    ],
    [
        Button.inline('\U0001F43B  ' + 'Рынок РФ', b'a1a3')
    ],
    [
        Button.inline('🇺🇳' + 'Мировые рынки', b'world_markets')
    ],
    # [
    #     Button.inline('\U0001F30D  ' + 'Market Valuation', b'a1a13')
    # ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a1_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a1a-1')
    ]
]

keyboard_historical_tests = [
    [
        Button.inline('\U0001F4BC  ' + 'Парковочный', b'hist_parking')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Всепогодный', b'hist_allweather')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Сбалансированный', b'hist_balanced')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Агрессивный', b'hist_agg')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Плечевой', b'hist_lev')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Elastic (только акции, без ETF)', b'hist_elastic')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Yolo (spbexchange)', b'hist_yolo')
    ],
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
        Button.inline('\U0001F519  ' + 'Назад', b'hist_back')
    ]
]

keyboard_a2_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-5')
    ]
]

keyboard_a3_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-51')
    ]
]

keyboard_a5 = [
    # [
    #     Button.inline('\U0001F50D   ' + 'Как ... /instruction01', b'a5a1')
    # ],
    # [
    #     Button.inline('\U0001F50D   ' + 'Что ... /instruction02', b'a5a2')
    # ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a5_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a5a-1')
    ]
]

keyboard_a6 = [
    [
        Button.inline('\U0001F476   ' + 'Мониторинг стратегий', b'a6a1')
    ],
    [
        Button.inline('\U0001F468  ' + 'Исторические тесты', b'a6a2')
    ],
    [
        Button.inline('\U0001F9D4  ' + 'Трекинг личного портфеля', b'a6a3')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a6_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a6a-1')
    ]
]

keyboard_a7 = [
    [
        Button.inline('\U0001F5DC  ' + 'Финансовый анализ', b'a7a1')
    ],
    [
        Button.inline('\U0001F46E  ' + 'Подробный анализ и скоринг', b'a7a2')
    ],
    [
        Button.inline('\U0001F46E  ' + 'Сводка новостей', b'a7a3')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a7_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a7a-1')
    ]
]

keyboard_a8 = [
    [
        Button.inline('\U0001F5DE  ' + 'Новости о рынках', b'a9a1')
    ],
    [
        Button.inline('\U0001F4B1   ' + 'Аналитические статьи', b'a9a2')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a8_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a8a-1')
    ]
]

keyboard_core_macro = [
    [
        Button.inline('\U0001F3E6  ' + 'Процентная ставка', b'cm1')
    ],
    [
        Button.inline('\U0001F321   ' + 'Уровень инфляции', b'cm2')
    ],
    [
        Button.inline('\U0001F525   ' + 'Уровень безработицы', b'cm3')
    ],
    [
        Button.inline('\U0001F3E2   ' + 'Индекс деловой активности', b'cm4')
    ],
    [
        Button.inline('\U0001F519   ' + 'Назад', b'cm-3')
    ]
]

keyboard_core_macro_back = [
    [
        Button.inline('\U0001F519   ' + 'Назад', b'cm-1')
    ]
]

keyboard_us_market = [
    [
        Button.inline('\U0001F503   ' + 'Статистика роста/падения', b'us1')
    ],
    [
        Button.inline('\U00002197   ' + 'Моментум в акциях', b'us6')
    ],
    [
        Button.inline('\U0001F4E3	' + 'Макро индикаторы и прогнозы', b'a1a6')
    ],
    [
        Button.inline('\U0001F4C9   ' + 'Кривая волатильности', b'us5')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-4')
    ]
]

keyboard_us_market_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-3')
    ]
]

keyboard_us_analysis = [
    [
        Button.inline('\U0001F3AF  ' + 'Обзор рынка США', b'us5z')
    ],
    [
        Button.inline('\U0001F9E9  ' + 'Подробный анализ', b'us5x')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-2')
    ]
]

keyboard_us_analysis_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-4')
    ]
]

keyboard_portfolio = [
    # [
    #     Button.inline('\U0001F4B0  ' + 'Мой портфель', b'mp1')
    # ],
    [
        Button.inline('\U0001F9F0  ' + 'Мои стратегии', b'my_strategies')
    ],
    [
        Button.inline('\U000026F3  ' + 'Исторические тесты', b'historical_tests')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_portfolio_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'portfolio_back')
    ]
]

keyboard_screener = [
    [
        Button.inline('\U0001F4B9  ' + 'Финансовый анализ', b'financial_analysis')
    ],
    # [
    #     Button.inline('\U0001F3C6  ' + 'Скринер лучших акций', b'sc1')
    # ],
    [
        Button.inline('\U0001F9E8  ' + 'Новости по компаниям', b'ticker_news')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_screener_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'screener_back')
    ]
]

keyboard_info = [
    [
        Button.inline('\U00002696   ' + 'Сравнение брокеров', b'brokers_compare')
    ],
    [
        Button.inline('\U000026D1   ' + 'Инструкции', b'instructions')
    ],
    [
        Button.inline('\U0001F6E1   ' + 'Регистрация управляющего', b'manager_registration')
    ],
    [
        Button.inline('\U0001F4EC  ' + 'Предложения и реклама', b'advertisement')
    ],
    [
        Button.inline('\U000026A0   ' + 'Сообщить об ошибке', b'bug_report')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_info_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'info_back')
    ]
]

keyboard_reset = [
    [
        Button.inline('\U00002049   ' + 'Подтвердить', b'reset_yes')
    ],
    [
        Button.inline('\U0001F519   ' + 'Отмена', b'reset_no')
    ]
]

keyboard_restart_poll = [
    [
        Button.inline('\U0001F6A9   ' + 'Определеить свой профиль риска', b'risk_profile_restart')
    ]
]

# ============================== Кнопки донатов =============================
keyboard_donate = [
    [
        Button.inline('\U0001F949   ' + '1$', b'donate1')
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
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

# ============================== Кнопки подписок =============================
keyboard_core_subscriptions = [
    [
        Button.inline('\U0001F46E  ' + 'Сравнение тарифов', b'kcs0')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'Старт', b'kcs1')
    ],
    [
        Button.inline('\U0001F321	  ' + 'Базовый', b'kcs2')
    ],
    [
        Button.inline('\U0001F525  ' + 'Продвинутый', b'kcs3')
    ],
    [
        Button.inline('\U0001F3E2  ' + 'Профессиональный', b'kcs4')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'kcs-1')
    ]
]

keyboard_subscription_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'kcs-1')
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


# keyboard_managed_strategies = [
#     [
#         Button.inline('\U0001F3E6  ' + 'Парковочный портфель', b'sac1')
#     ],
#     [
#         Button.inline('\U0001F3E6  ' + 'Сбалансированный портфель', b'sac2')
#     ],
#     [
#         Button.inline('\U0001F3E6  ' + 'Агрессивный', b'sac3')
#     ],
#     [
#         Button.inline('\U0001F519  ' + 'Назад', b'sacback')
#     ]
# ]


def generate_payment_button(kbd_label=None, payment_link=None):
    keyboard_subscr_start_inst = [
        [
            Button.url('\U0001F3E6  ' + kbd_label, payment_link)
        ],
        [
            Button.inline('\U0001F519  ' + 'Назад', b'donate_back')
        ]
    ]
    return keyboard_subscr_start_inst


keyboard_friend_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'friend_back')
    ]
]

# ============= Кнопки для меню мои стратегии =============
risk_profile1 = [
    [
        Button.inline('\U0001F4BC  ' + 'Парковочный', b'strategy_parking')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons S', b'strategy_allseasons_s')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'portfolio_back')
    ]
]

risk_profile2 = [
    [
        Button.inline('\U0001F4BC  ' + 'Парковочный', b'strategy_parking')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Всепогодный', b'strategy_allweather')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons M', b'strategy_allseasons_m')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'portfolio_back')
    ]
]

risk_profile3 = [
    [
        Button.inline('\U0001F4BC  ' + 'Всепогодный', b'strategy_allweather')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Сбалансированный', b'strategy_balanced')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons M', b'strategy_allseasons_m')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'portfolio_back')
    ]
]

risk_profile4 = [
    [
        Button.inline('\U0001F4BC  ' + 'Сбалансированный', b'strategy_balanced')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'All Seasons L', b'strategy_allseasons_l')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'portfolio_back')
    ]
]

risk_profile5 = [
    [
        Button.inline('\U0001F4BC  ' + 'Сбалансированный', b'strategy_balanced')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Агрессивный', b'strategy_aggressive')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Yolo', b'strategy_yolo')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Elastic', b'strategy_elastic')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'portfolio_back')
    ]
]

risk_profile6 = [
    [
        Button.inline('\U0001F4BC  ' + 'Агрессивный', b'strategy_aggressive')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Плечевой', b'strategy_leveraged')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Yolo', b'strategy_yolo')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Elastic', b'strategy_elastic')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'portfolio_back')
    ]
]

my_strategies_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'strategies_back')
    ]
]
