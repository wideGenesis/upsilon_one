from telethon.tl.custom import Button
from project_shared import *
from random import choice


lol = ['Подача напитков из улиток', 'Мыло \"Кот Да Винчи\"', 'Гос реестр порно', 'Орден Финансового Лосся',
       'Шопот крыш', 'Отделение пластики мозга', 'Моргаем диафрагмой', 'Мастерская \"Парики Трампа\"',
       'Бар \"Финансовое воздержание\"']

keyboard_start = [
        [Button.text('Меню', resize=True), Button.text('Профиль', resize=True)],
    [Button.text('Информация', resize=True), Button.text(f'{choice(lol)}', resize=True)]
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
        Button.inline('\U0001F4BC   ' + 'Мой портфель', b'a2')
    ],
    [
        Button.inline('\U0001F9EC   ' + 'Скринер акций', b'a3')
    ],
    [
        Button.inline('\U0001F4F0   ' + 'Лента новостей', b'a8')
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
        Button.inline('🇺🇳' + 'Мировые рынки', b'a1a5')
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

keyboard_a2 = [
    [
        Button.inline('\U0001F4BC  ' + 'Парковочный портфель', b'a2a3')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Всепогодный портфель', b'a2a4')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Сбалансированный портфель', b'a2a5')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Агрессивный портфель', b'a2a6')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Плечевой портфель', b'a2a7')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Elastic портфель (только акции, без ETF)', b'a2a9')
    ],
    [
        Button.inline('\U0001F4BC  ' + 'Yolo портфель (spbexchange)', b'a2a10')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-5')
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
        Button.inline('\U0001F3E6  ' + 'Interest Rates', b'cm1')
    ],
    [
        Button.inline('\U0001F321   ' + 'Inflation Rates', b'cm2')
    ],
    [
        Button.inline('\U0001F525   ' + 'Unemployment Rates', b'cm3')
    ],
    [
        Button.inline('\U0001F3E2   ' + 'Composite PMI', b'cm4')
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
    [
        Button.inline('\U0001F4B0  ' + 'Мой портфель', b'mp1')
    ],
    [
        Button.inline('\U0001F9F0  ' + 'Мои стратегии', b'mp1')
    ],
    [
        Button.inline('\U000026F3  ' + 'Исторические тесты', b'mp3')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_portfolio_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-5')
    ]
]

keyboard_screener = [
    [
        Button.inline('\U0001F4B9  ' + 'Финансовый анализ', b'sc1')
    ],
    [
        Button.inline('\U0001F3C6  ' + 'Скринер лучших акций', b'sc1')
    ],
    [
        Button.inline('\U0001F9E8  ' + 'Новости по компаниям', b'sc3')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_screener_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-4')
    ]
]

keyboard_info = [
    [
        Button.inline('\U000026D1   ' + 'Инструкции', b'a5')
    ],
    [
        Button.inline('\U0001F6E1   ' + 'Регистрация управляющего', b'rel1')
    ],
    [
        Button.inline('\U0001F4EC  ' + 'Предложения и реклама', b'rel1')
    ],
    [
        Button.inline('\U000026A0   ' + 'Сообщить об ошибке', b'rel1')
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
        ]
    ]
    return keyboard_subscr_start_inst

# TODO поменять иконки кнопок