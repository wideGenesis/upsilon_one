from dataclasses import dataclass
from finviz.screener import Screener
import pandas as pd
from telegraph import Telegraph, upload_file
from datetime import date
from csv import reader
from project_shared import *


def percent_to_float(x):
    return float(x.strip('%'))


def cap_norm(x):
    try:

        if x[-1] == 'M':
            x = float(x.strip('M'))
            x = x * 1000000
        elif x[-1] == 'B':
            x = float(x.strip('B'))
            x = x * 1000000000
        else:
            return x
    except:
        return x
    return x


def img_to_telegraph(path=None):
    telegraph = Telegraph(access_token=None)
    uploading = upload_file(f'{path}')
    debug(uploading)
    return uploading


@dataclass
class GuruRocketScreener:
    __slots__ = [
        'guru',
        'short_name',
        'author_name',
        'author_url',
        'access_token',
        'custom',
        'guru_filename',
        'rocket_filename',
        'path',
        'tlgph_guru_fname',
        'tlgph_rock_fname',
    ]

    def __init__(self,
                 guru: bool = True,
                 short_name: str = 'Upsilon',
                 author_name: str = 'Upsilon',
                 author_url: str = None,
                 access_token: str = 'dde4d5a2f8e0e12e98fa5e9d524a5a91129855fbb37cbb45879871051a29',
                 custom=None,
                 guru_filename: str = 'guru_stocks.csv',
                 rocket_filename: str = 'rocket_stocks.csv',
                 path: str = f'{PROJECT_HOME_DIR}/results/gururocketscreener/',
                 tlgph_guru_fname: str = '/file/85198326b0ef5ebda6a17.png',
                 tlgph_rock_fname: str = '/file/ae6c623cb2013a4dcb0f8.jpg',
                 ):
        if custom is None:
            custom = ['1', '2', '3', '6', '43', '44', '46', '49', '59', '65']
        self.guru = guru
        self.short_name = short_name
        self.author_name = author_name
        self.author_url = author_url
        self.access_token = access_token
        self.custom = custom
        self.guru_filename = guru_filename
        self.rocket_filename = rocket_filename
        self.path = path
        self.tlgph_guru_fname = tlgph_guru_fname
        self.tlgph_rock_fname = tlgph_rock_fname

    def get_picks(self):
        df = pd.DataFrame()
        if self.guru:
            mk = 0.25
            qk = 0.35
            yk = 0.4
            cap = None
            filters = ['idx_sp500', 'ta_perf_26wup', 'ta_sma50_pa']
            filename = self.guru_filename
        else:
            mk = 0.20
            qk = 0.70
            yk = 0.10
            cap = 1
            filters = ['cap_microover', 'ind_stocksonly', 'ipodate_more1', 'avgvol_o50', 'sh_price_u10',
                       'ta_perf_13wup', 'ta_sma50_pa']
            filename = self.rocket_filename

        get_stocks = Screener(filters=filters, table='Performance', order='price', custom=self.custom)
        get_stocks.to_csv(f'{self.path}{filename}')

        df = pd.read_csv(f'{self.path}{filename}', index_col='Ticker',
                         converters={'Perf Month': percent_to_float, 'Perf Quart': percent_to_float,
                                     'Perf Year': percent_to_float, 'Market Cap': cap_norm})

        if cap is None:
            cap = df['Market Cap']
        else:
            cap = 1
        df['rank'] = (mk * df['Perf Month'] + qk * df['Perf Quart'] + yk * df['Perf Year']) / df['RSI'] * cap
        df['Daily SL %'] = round(df['ATR'] / df['Price'] * 100 * 2.71828, ndigits=2)
        df.sort_values(by=['rank'], inplace=True, ascending=False)
        df = df[0:50]
        df.drop(columns={'No.', 'Market Cap', 'Perf Month', 'Perf Quart', 'Perf Year', 'ATR', 'RSI', 'Price', 'rank'},
                inplace=True)
        df.to_csv(f'{self.path}{filename}')

        msg = ''
        with open(f'{self.path}{filename}', 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            if header is not None:
                for row in csv_reader:
                    msg += f'<li><b>{row[0]}</b> | {row[1]} | {row[2]} | {row[3]}</li>'
                return msg

    def telegraph_acc_create(self):
        telegraph = Telegraph()
        acc = telegraph.create_account(short_name=self.short_name, author_name=self.author_name,
                                       author_url=self.author_url)
        debug(acc)

    def publish_to_telegraph(self):
        today = date.today()
        telegraph = Telegraph(access_token=self.access_token)
        if self.guru:
            title = 'Консолидированные длинные позиции Гуру'
            img_filename = self.tlgph_guru_fname
            text = 'Ипсилон анализирует последние сделки самых прибыльных гуру фондового рынка и затем выбирает ' \
                   'наиболее перспективные и значимые компании. Лучшим вариантом портфеля будет: ' \
                   '15-20 акций из списка. Стоп-лоссы использовать не обязательно!\n'
            msg = self.get_picks()
        else:
            title = 'Дешевые акции с высоким потенциалом роста'
            img_filename = self.tlgph_rock_fname
            text = 'Ипсилон анализирует упоминания тикеров в социальных сетях и выбирает самые недорогие, ' \
                   'но потенциально прибыльные акции. Cheap-тикеры выбираются без учета фундаментального анализа, ' \
                   'а исключительно статистически, поэтому следует с осторожностью инвестировать в данные акции.\n' \
                   'Лучшим вариантом портфеля будет: 15-20 акций из списка. Рекомендуется использовать стоп-лоссы, ' \
                   'величина которых указанна напротив каждого тикера. Если какая-то акция не стрельнула, ' \
                   'ее нужно продать, а не надеться!'
            msg = self.get_picks()
        try:
            posting = telegraph.create_page(
                f'{title} по состоянию на {today}',
                content=None,
                html_content=f'<img src={img_filename}/>'
                             f'<p>{text}</p>'
                             f'<br><p><b>\nTicker | Company | Sector | Daily SL %</b></p><ul>{msg}</ul>',
                author_name='@UpsilonBot',
                author_url=None,
                return_content=True

            )
            debug(posting)
            debug('Posting has been completed')
            return posting
        except Exception as e0:
            debug(e0)
            debug('Posting to telegraph failed')

    def edit_page(self, link=None, msg=None, img_path=None):
        today = date.today()
        telegraph = Telegraph(access_token=self.access_token)
        if self.guru:
            title = 'Консолидированные длинные позиции Гуру'
            img_filename = self.tlgph_guru_fname
            text = 'Ипсилон анализирует последние сделки самых прибыльных гуру фондового рынка и затем выбирает ' \
                   'наиболее перспективные и значимые компании. Лучшим вариантом портфеля будет: ' \
                   '15-20 акций из списка. Стоп-лоссы использовать не обязательно!\n'
            msg = self.get_picks()
        else:
            title = 'Дешевые акции с высоким потенциалом роста'
            img_filename = self.tlgph_rock_fname
            text = 'Ипсилон анализирует упоминания тикеров в социальных сетях и выбирает самые недорогие, ' \
                   'но потенциально прибыльные акции. Cheap-тикеры выбираются без учета фундаментального анализа, ' \
                   'а исключительно статистически, поэтому следует с осторожностью инвестировать в данные акции.\n' \
                   'Лучшим вариантом портфеля будет: 15-20 акций из списка. Рекомендуется использовать стоп-лоссы, ' \
                   'величина которых указанна напротив каждого тикера. Если какая-то акция не \'стрельнула\', ' \
                   'ее нужно продать, а не надеться рост!\n'
            msg = self.get_picks()

        try:
            edit = telegraph.create_page(
                f'{link}'
                f'{title} по состоянию на {today}',
                content=None,
                html_content=f'<img src={img_filename}/>'
                             f'<p>{text}</p>'
                             f'<br><p><b>\nTicker | Company | Sector | Daily SL %</b></p><ul>{msg}</ul>',
                author_name='@UpsilonBot',
                author_url=None,
                return_content=True

            )
            debug(edit)
            debug('Posting has been completed')
            return edit
        except Exception as e0:
            debug(e0)
            debug('Posting to telegraph failed')


# start = GuruRocketScreener(guru=False, path='')
# start.publish_to_telegraph()

# start.edit_page(link='Konsolidirovannye-dlinnye-pozicii-Guru-po-sostoyaniyu-na-2021-05-20-05-20')
# start.edit_page(link='Deshevye-loterejnye-akcii-na-2021-05-20-05-20')



