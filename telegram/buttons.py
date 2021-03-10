from telethon.tl.custom import Button
from project_shared import *

keyboard_start = [
        [Button.text('Главное меню', resize=True), Button.text('Профиль', resize=True)]
    ]

keyboard_0 = [
    [
        Button.inline('\U0001F52C   ' + 'Анализ рынков', b'a1')
    ],
    [
        Button.inline('\U0001F9EC   ' + 'Портфели', b'a2')
    ],
    # [
    #     Button.inline('\U0001F9F0   ' + 'Калькуляторы', b'a3')
    # ],
    [
        Button.inline('\U0001F9BE   ' + 'Управление', b'a4')
    ],
    [
        Button.inline('\U000026D1   ' + 'Инструкции', b'a5')
    ],
    # [
    #     Button.inline('\U0001F393   ' + 'Образование', b'a6')
    # ],
    # [
    #     Button.inline('\U0001F92F   ' + 'Налоги', b'a7')
    # ],
    [
        Button.inline('\U0001F5C3   ' + 'Лента новостей', b'a8')
    ]
]

keyboard_a1 = [
    [
        Button.inline('\U0001F5FD  ' + 'Рынок США', b'a1a1')
    ],
    [
        Button.inline('\U0001F513  ' + 'Рынок криптовалют', b'a1a2')
    ],
    [
        Button.inline('\U0001F43B  ' + 'Рынок РФ', b'a1a3')
    ],
    [
        Button.inline('\U0001F504  ' + 'ETF сантимент', b'a1a4')
    ],
    [
        Button.inline('\U0001F30D  ' + 'Мировые рынки', b'a1a5')
    ],
    # [
    #     Button.inline('\U0001F9ED   ' + 'Основные макро индикаторы', b'a1a6')
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
    # [
    #     Button.inline('\U0001F4BC   ' + 'Твой профиль риска', b'a2a1')
    # ],
    # [
    #     Button.inline('\U0001F4BC  ' + 'Оценка/аудит портфеля', b'a2a2')
    # ],
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
    # [
    #     Button.inline('\U0001F4BC  ' + 'Трейдинг/Дневные стратегии', b'a2a8')
    # ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a2_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a2a-1')
    ]
]
keyboard_a3 = [
    [
        Button.inline('\U0001F50E  ' + 'Рассчет количества акций для портфеля', b'a3a1')
    ],
    [
        Button.inline('\U0001F50E  ' + 'Симуляция 10 летней доходности', b'a3a2')
    ],
    [
        Button.inline('\U0001F50E  ' + 'Рассчет оптимального размера взносов', b'a3a3')
    ],
    [
        Button.inline('\U0001F50E  ' + 'Рассчет безопасного размера вывода средств', b'a3a4')
    ],
    [
        Button.inline('\U0001F50E  ' + 'Сложный процент', b'a3a5')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a3_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a3a-1')
    ]
]
keyboard_a4 = [
    [
        Button.inline('\U0001F4A1 ' + 'Портфели доступные для управления', b'a4a1')
    ],
    [
        Button.inline('\U0001F6E1   ' + 'Регистрация управляющего', b'a4a2')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'main')
    ]
]

keyboard_a4_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'a4a-0')
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
        Button.inline('\U0001F476   ' + 'Основы инвестирования', b'a6a1')
    ],
    [
        Button.inline('\U0001F468  ' + 'Как собрать свой первый портфель', b'a6a2')
    ],
    [
        Button.inline('\U0001F9D4  ' + 'Профессиональные решения', b'a6a3')
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
        Button.inline('\U0001F5DC  ' + 'Оптимизация налогов', b'a7a1')
    ],
    [
        Button.inline('\U0001F46E  ' + 'Подготовка налоговых деклараций', b'a7a2')
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
        Button.inline('\U0001F50D	' + 'Последние новости компании', b'a9a3')
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
        Button.inline('\U0001F519   ' + 'Назад', b'cm-2')
    ]
]

keyboard_core_macro_back = [
    [
        Button.inline('\U0001F519   ' + 'Назад', b'cm-1')
    ]
]

keyboard_us_market = [
    [
        Button.inline('\U0001F9E9	' + 'Подробный анализ рынка', b'us2')
    ],
    [
        Button.inline('\U0001F503   ' + 'Статистика роста/падения', b'us1')
    ],
    [
        Button.inline('\U00002197   ' + 'Моментум в акциях', b'us6')
    ],
    [
        Button.inline('\U0001F3A8   ' + 'Тепловые карты', b'us3')
    ],
    [
        Button.inline('\U0001F4E3	' + 'Макро индикаторы и прогнозы', b'a1a6')
    ],
    [
        Button.inline('\U0001F4C9   ' + 'Кривая волатильности', b'us5')
    ],
    [
        Button.inline('\U0001F9ED   ' + 'Анализ акций компаний', b'us7')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-2')
    ]
]

keyboard_us_market_back = [
    [
        Button.inline('\U0001F519  ' + 'Назад', b'cm-3')
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

keyboard_risk_profile = [
    [
        Button.inline('\U0001F3E6  ' + 'Спекулятивный рост', b'rp1')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'Агрессивный рост', b'rp2')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'Умеренный рост', b'rp3')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'Острожный рост', b'rp4')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'Сохранение капитала', b'rp5')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'Рост и обеспечение текущих расходов.', b'rp6')
    ]
]

keyboard_financial_state = [
    [
        Button.inline('\U0001F3E6  ' + '$0 - $100,000', b'fs1')
    ],
    [
        Button.inline('\U0001F3E6  ' + '$100,000 - $1,000000', b'fs2')
    ],
    [
        Button.inline('\U0001F3E6  ' + '$1,000000 - $5,000000', b'fs3')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'более $5,000000', b'fs4')
    ]
]

keyboard_horizon = [
    [
        Button.inline('\U0001F3E6  ' + '1 год', b'hr1')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'от 1 до 2 лет', b'hr2')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'от 3 до 5 лет', b'hr3')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'более 5 лет', b'hr4')
    ]
]

keyboard_return = [
    [
        Button.inline('\U0001F3E6  ' + 'до 5%', b'ret1')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'до 10%', b'ret2')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'до 15%', b'ret3')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'свыше 15%', b'ret4')
    ]
]

keyboard_managed_strategies = [
    [
        Button.inline('\U0001F3E6  ' + 'Парковочный портфель', b'sac1')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'Сбалансированный портфель', b'sac2')
    ],
    [
        Button.inline('\U0001F3E6  ' + 'Агрессивный', b'sac3')
    ],
    [
        Button.inline('\U0001F519  ' + 'Назад', b'sacback')
    ]
]


def generate_payment_button(kbd_label=None, payment_link=None):
    keyboard_subscr_start_inst = [
        [
            Button.url('\U0001F3E6  ' + kbd_label, payment_link)
        ]
    ]
    return keyboard_subscr_start_inst

# TODO поменять иконки кнопок
