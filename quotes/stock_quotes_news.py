from dataclasses import dataclass
from math_stat.fin_stat import angular_distance
import pandas as pd
import json
import finviz
from finvizfinance.news import News
import quantstats as qs
from quotes.historical_universe import *
from quotes.parsers import *
from telegram import instructions as ins
from collections import OrderedDict

def sma(data, window):
    weights = np.repeat(1.0, window) / window
    sma8 = np.convolve(data, weights, 'valid')
    return sma8


@dataclass
class StockStat:
    __slots__ = [
        'stock',
        'returns',
        'limit_',
        'title',
        'ticker',
        'benchmark',
        'mode',
        'ticker_',
        'display',
        'sma_signal',
        'ticker_type',
        'mom_rank_dict'
    ]

    def __init__(self,
                 stock: str = None,
                 returns: pd = None,
                 sma_signal: bool = None,
                 limit_: int = None,
                 title: str = None,
                 benchmark: str = 'QQQ',
                 mode: str = 'full',
                 ticker_: str = None,
                 display: bool = False,
                 ticker_type: str = False,
                 mom_rank_dict: dict = None
                 ):
        self.stock = stock
        self.returns = returns
        self.sma_signal = sma_signal
        self.limit_ = limit_
        self.title = title
        self.benchmark = benchmark
        self.mode = mode
        self.ticker_ = ticker_
        self.display = display
        self.ticker_type = ticker_type
        self.mom_rank_dict = mom_rank_dict

    def stock_download(self):
        try:
            returns = qs.utils.download_returns(self.stock)
        except ValueError as e11:
            return e11
        if returns.empty:
            self.returns = None
        else:
            self.returns = returns

    def higher_sma8(self):
        try:
            weekly_returns = qs.utils.download_weekly(self.stock)
        except ValueError as e11:
            return e11
        if weekly_returns.empty:
            self.sma_signal = None
        else:
            sma8 = sma(weekly_returns, 8)
            sma8 = sma8.tolist()
            last_close = weekly_returns.iloc[-2]
            if last_close > sma8[-2:-1]:
                self.sma_signal = True
            else:
                self.sma_signal = False
        return self.sma_signal

    def stock_type(self):
        s_type = {}
        asset_returns = qs.utils.download_returns(self.stock, period='1y')
        asset_returns.dropna(inplace=True)
        factors = ['SPY', 'QQQ', 'ARKK', 'VLUE']
        for factor in factors:
            try:
                factor_returns = qs.utils.download_returns(factor, period='1y')
                factor_returns.dropna(inplace=True)
                angular_d = angular_distance(asset_returns, factor_returns)
                s_type.update({f'{factor}': angular_d})
            except ValueError as e11:
                print(e11)
                return '🛸 нет данных'
        min_angular = min(s_type, key=s_type.get)
        if min_angular == 'SPY' and min(s_type.values()) <= 0.45:
            msg_type = '⚖ Quality - стабильные и \"качественные\" компании\n'
        elif min_angular == 'QQQ' and min(s_type.values()) <= 0.45:
            msg_type = '✈ Growth - стабильно растущие компании\n'
        elif min_angular == 'ARKK' and min(s_type.values()) <= 0.45:
            msg_type = '🛫 Startup - компании в начальной стадии своего жизненного цикла\n'
        elif min_angular == 'VLUE' and min(s_type.values()) <= 0.45:
            msg_type = '🛬 Value - компании достигшие пика своего жизненного цикла\n'
        elif min(s_type.values()) >= 0.65:
            msg_type = '⚠️ - рискованный тикер Среди(Junk Stock) или это не класс акций\n'
        else:
            msg_type = '🛸 тикер не классифицируем\n'
        self.ticker_type = msg_type
        return msg_type

    def new_var(self):
        path = f'{PROJECT_HOME_DIR}/results/ticker_stat/'
        try:
            returns = self.returns * 100
        except TypeError as e13a:
            debug(e13a)
            return
        min_returns = abs(returns.rolling(21).min())
        n_var = min_returns.iloc[-63:].mean() + min_returns.iloc[-63:].std()
        n_var_euler = min_returns.iloc[-63:].mean() + 2.71 * min_returns.iloc[-63:].std()

        new_var_array = []
        new_var_array_e = []
        num_days = int(10)
        for x in range(1, num_days + 1):
            new_var_array.append(np.round(n_var * np.sqrt(x), 2))
            new_var_array_e.append(np.round(n_var_euler * np.sqrt(x), 2))

        df = pd.DataFrame()
        df['Expected Large Loss'] = new_var_array
        df['Expected Tail Loss'] = new_var_array_e

        sns.set(rc={'figure.facecolor': 'black', 'figure.edgecolor': 'black', 'xtick.color': 'white',
                    'ytick.color': 'white', 'text.color': 'white', 'axes.labelcolor': 'white',
                    'axes.facecolor': 'black', 'grid.color': '#17171a'})
        sns.despine()
        sns.set_context('paper', font_scale=1.25)
        plt.figure(figsize=(11, 7))
        sns.lineplot(markers=True, dashes=False,
                     palette="hls", alpha=.9,
                     data=df,
                     legend="brief")

        plt.xlabel("День #")
        plt.ylabel("Убытки (%)")
        plt.suptitle(f'Возможные максимальные убытки {self.stock} за следующие 10 дней', fontsize=15)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', facecolor='black', transparent=True, bbox_inches='tight')
        buf.seek(0)
        im = Image.open(buf)
        filename_h5 = str(uuid.uuid4()).replace('-', '')
        debug(f"Tail loss filename: {filename_h5}")
        im.save(f'{path}{filename_h5}.png')
        buf.close()
        plt.close('all')
        add_watermark(f'{path}{filename_h5}.png', f'{path}{filename_h5}.png', 60, wtermark_color=(255, 255, 255, 70))
        result_files = f'{path}{filename_h5}.png'
        return result_files

    def momentum_rank(self):
        path = f'{PROJECT_HOME_DIR}/results/ticker_stat/'
        mom_rank = {}
        sectors = [self.stock]
        sectors.extend(BENCHMARKS)
        for t in sectors:
            try:
                if t in BENCHMARKS:
                    prices = get_closes_by_ticker(t,
                                                  include_left_bound=True,
                                                  include_right_bound=True,
                                                  table_name=BENCHMARKS_QUOTES_TABLE_NAME)
                else:
                    prices = qs.utils.download_weekly(t, period="1y", interval="1d")
            except ValueError as e11:
                debug(e11)
                return
            # calc nom as weighed mom
            m20 = ((prices - prices.rolling(20).mean()) / prices.rolling(20).mean()) * 100
            m50 = ((prices - prices.rolling(50).mean()) / prices.rolling(50).mean()) * 100
            m200 = ((prices - prices.rolling(200).mean()) / prices.rolling(200).mean()) * 100

            # calc denominator as rsi
            delta = prices.diff()
            delta = delta[1:]
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
            roll_up1 = up.ewm(span=10).mean()
            roll_down1 = down.abs().ewm(span=10).mean()
            rs = roll_up1 / roll_down1
            rsi = 100.0 - (100.0 / (1.0 + rs))

            rank = (0.25 * m20 + 0.35 * m50 + 0.4 * m200) / rsi
            try:
                rank = round(rank.iloc[-1], ndigits=3)
            except IndexError as rank_err:
                debug(rank_err)
                return
            mom_rank.update({f'{t}': rank})

        mom_rank = {k: v for k, v in sorted(mom_rank.items(), key=lambda item: item[1])}
        self.mom_rank_dict = mom_rank

        sns.set(rc={'figure.facecolor': 'black', 'figure.edgecolor': 'black', 'xtick.color': 'white',
                    'ytick.color': 'white', 'text.color': 'white', 'axes.labelcolor': 'white',
                    'axes.facecolor': 'black', 'grid.color': '#17171a'})
        sns.despine()
        sns.set_context('paper', font_scale=1)
        plt.figure(figsize=(11, 7))

        sns.scatterplot(
            palette="hls", alpha=.9,
            markers=True,
            data=mom_rank,
            x=mom_rank.keys(),
            y=mom_rank.values(),
            hue=mom_rank.keys(),
            s=150,
        )
        plt.text(f'{self.stock}', mom_rank[f'{self.stock}'], f'{self.stock}',
                 horizontalalignment='center', size='medium', color='white', weight='semibold')
        # plt.legend().remove()
        plt.legend(title='Momentum Rank', loc='center left', bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
        plt.xlabel("Assets")
        plt.ylabel("Momentum Rank")
        plt.suptitle(f'Моментум {self.stock} в сравнении с секторами и классами', fontsize=18)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', facecolor='black', transparent=True, bbox_inches='tight')
        buf.seek(0)
        im = Image.open(buf)
        filename_h7 = str(uuid.uuid4()).replace('-', '')
        debug(f"Mom_rank filename: {filename_h7}")
        im.save(f'{path}{filename_h7}.png')
        buf.close()
        plt.close('all')
        add_watermark(f'{path}{filename_h7}.png', f'{path}{filename_h7}.png', 60, wtermark_color=(255, 255, 255, 70))

        result_files = f'{path}{filename_h7}.png'
        return result_files

    def stock_snapshot(self):
        if self.returns is not None:
            img = f'results/ticker_stat/{self.stock}.png'
            qs.plots.snapshot_v2(self.returns[-335:],
                                 title=f'{self.stock}',
                                 savefig=img)

    # def stock_stat_v3(self, rank_type=None, rank=None, sma_sig=None):
    #     if self.returns is not None:
    #         stats = qs.reports.metrics_v2(self.returns,
    #                                       benchmark=self.benchmark,
    #                                       mode=self.mode,
    #                                       ticker_=self.stock,
    #                                       display=self.display)
    #         parse = json.loads(stats)
    #         if float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 11 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score максимален для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 11 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score максимален для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 8 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score достаточно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 8 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score достаточно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 6 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score умеренно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 6 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score умеренно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank <= 5 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Но Upsilon-score низок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank <= 5 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Но Upsilon-score низок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 13 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score максимален для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️⭐'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 13 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score максимален для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 10 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score достаточно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 10 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score достаточно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 7 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Upsilon-score умеренно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 7 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Upsilon-score умеренно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 5 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Upsilon-score низок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️️'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank >= 5 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Upsilon-score низок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank <= 4 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'И Upsilon-score слишком низок для компании этого типа. Потенциальный риск не оправдан. ' \
    #                      f'\n\n{self.stock} - ⭐️'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
    #                 and rank <= 4 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'И Upsilon-score слишком низок для компании этого типа. Потенциальный риск не оправдан. ' \
    #                      f'\n\n{self.stock} - ⛔️'
    #
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 8 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score максимален для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 8 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score максимален для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 6 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score достаточно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 6 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score достаточно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 4 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score умеренно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 4 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Upsilon-score умеренно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank <= 3 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Но Upsilon-score низок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank <= 3 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
    #                      f'Но Upsilon-score низок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 10 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score максимален для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 10 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score максимален для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 8 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score достаточно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 8 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score достаточно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐️️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 6 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score умеренно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️⭐'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 6 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Но Upsilon-score умеренно высок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 4 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Upsilon-score низок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️⭐️'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank >= 4 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'Upsilon-score низок для компании этого типа. ' \
    #                      f'\n\n{self.stock} - ⭐️'
    #
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank <= 3 and sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'И Upsilon-score слишком низок для компании этого типа. Потенциальный риск не оправдан. ' \
    #                      f'\n\n{self.stock} - ⭐'
    #         elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
    #                 and rank <= 3 and not sma_sig:
    #             sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
    #                      f'И Upsilon-score слишком низок для компании этого типа. Потенциальный риск не оправдан. ' \
    #                      f'\n\n{self.stock} - ⛔'
    #
    #         elif rank == 0:
    #             sharpe = f'\U000026D4 отсутствуют данные для оценки {self.stock} или крайне плохое ведение бизнеса'
    #         else:
    #             sharpe = f'\U000026A0 противоречивые результаты анализа. Финансовая оценка не соответсвует ' \
    #                      f'ценовой динамике акций {self.stock}'
    #
    #         msg = f'{self.stock} __проанализирована __\nс ' + parse[self.stock]['Start Period'] + ' по ' + \
    #               parse[self.stock]['End Period'] + '\n' + '\n' + '```Вывод: ```' + '\n' + sharpe + '\n' + '\n'
    #         print(rank, rank_type)
    #         return msg

    def stock_stat_v4(self, rank_type=None, rank=None, sma_sig=None):
        if self.mom_rank_dict is not None:
            ranking = 0
            d = OrderedDict(self.mom_rank_dict)
            temp = list(d.items())
            top10_percentile = temp[-3][1]

            if self.mom_rank_dict[self.stock] >= top10_percentile and sma_sig:
                ranking += 3
                rank_msg = f'сильнее, чем у 90% секторов. {self.stock} технически очень сильна'

            elif self.mom_rank_dict[self.stock] >= top10_percentile and not sma_sig:
                ranking += 2
                rank_msg = f'сильнее, чем у 90% секторов. {self.stock} технически сильна'

            elif self.mom_rank_dict[self.stock] >= self.mom_rank_dict['SPY'] and sma_sig:
                ranking += 2
                rank_msg = f'сильнее, чем у индекса. {self.stock} технически сильна'

            elif self.mom_rank_dict[self.stock] >= self.mom_rank_dict['SPY'] and not sma_sig:
                ranking += 1
                rank_msg = f'сильнее, чем у индекса. {self.stock} технически нейтральна'

            elif self.mom_rank_dict[self.stock] < self.mom_rank_dict['SPY'] and sma_sig:
                ranking += 1
                rank_msg = f'слабее, чем у индекса. {self.stock} технически слаба, но начались покупки'

            else:
                ranking = 0
                rank_msg = f'отсутствует. {self.stock} технически очень слаба, без признаков покупок'

            if sma_sig:
                sma_sig_msg = f'✅ Институционалы покупают {self.stock} или как минимум не продают'
            else:
                sma_sig_msg = f'⚠️ Институционалы продают {self.stock}'

# ========================== Main, usual Rank ======================================
            if rank_type == 0 and rank >= 11 and ranking == 3:
                abs_rank = f'⭐️⭐️⭐ Моментум {self.stock} {rank_msg}\n' \
                         f'🟢 Финансовая оценка максимальна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐🟢️️'

            elif rank_type == 0 and rank >= 11 and ranking == 2:
                abs_rank = f'⭐️⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🟢 Финансовая оценка максимальна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️🟢️️'

            elif rank_type == 0 and rank >= 11 and ranking == 1:
                abs_rank = f'⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🟢 Финансовая оценка максимальна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️🟢️️'
            elif rank_type == 0 and rank >= 11 and ranking == 0:
                abs_rank = f'📉️ Моментум у {self.stock} {rank_msg}\n' \
                         f'🟢 Финансовая оценка максимальна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - 📉️🟢️️'

            elif rank_type == 0 and rank >= 6 and ranking == 3:
                abs_rank = f'⭐️⭐️⭐ Моментум {self.stock} {rank_msg}\n' \
                         f'🟡 Финансовая оценка стабильна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐🟡️'
            elif rank_type == 0 and rank >= 6 and ranking == 2:
                abs_rank = f'⭐️⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🟡 Финансовая оценка стабильна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️🟡️'
            elif rank_type == 0 and rank >= 6 and ranking == 1:
                abs_rank = f'⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🟡 Финансовая оценка стабильна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️🟡️'
            elif rank_type == 0 and rank >= 6 and ranking == 0:
                abs_rank = f'📉️ Моментум у {self.stock} {rank_msg}\n' \
                         f'🟡 Финансовая оценка стабильна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - 📉️🟡️'

            elif rank_type == 0 and rank <= 5 and ranking == 3:
                abs_rank = f'⭐️⭐️⭐ Моментум {self.stock} {rank_msg}\n' \
                         f'🔴 Финансовая оценка негативна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐🔴️'
            elif rank_type == 0 and rank <= 5 and ranking == 2:
                abs_rank = f'⭐️⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🔴 Финансовая оценка негативна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️🔴️'
            elif rank_type == 0 and rank <= 5 and ranking == 1:
                abs_rank = f'⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🔴 Финансовая оценка негативна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️🔴️'
            elif rank_type == 0 and rank <= 5 and ranking == 1:
                abs_rank = f'📉️️ Моментум у {self.stock} {rank_msg}\n' \
                         f'🔴 Финансовая оценка негативна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - 📉️️🔴️'

# ========================== Other Fin Rank ======================================
            elif rank_type == 1 and rank >= 8 and ranking == 3:
                abs_rank = f'⭐️⭐️⭐ Моментум {self.stock} {rank_msg}\n' \
                         f'🟢 Финансовая оценка максимальна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐🟢️️'

            elif rank_type == 1 and rank >= 8 and ranking == 2:
                abs_rank = f'⭐️⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🟢 Финансовая оценка максимальна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️🟢️️'

            elif rank_type == 1 and rank >= 8 and ranking == 1:
                abs_rank = f'⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🟢 Финансовая оценка максимальна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️🟢️️'
            elif rank_type == 1 and rank >= 8 and ranking == 0:
                abs_rank = f'📉️ Моментум у {self.stock} {rank_msg}\n' \
                         f'🟢 Финансовая оценка максимальна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - 📉️🟢️️'

            elif rank_type == 1 and rank >= 4 and ranking == 3:
                abs_rank = f'⭐️⭐️⭐ Моментум {self.stock} {rank_msg}\n' \
                         f'🟡 Финансовая оценка стабильна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐🟡️'
            elif rank_type == 1 and rank >= 4 and ranking == 2:
                abs_rank = f'⭐️⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🟡 Финансовая оценка стабильна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️🟡️'
            elif rank_type == 1 and rank >= 4 and ranking == 1:
                abs_rank = f'⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🟡 Финансовая оценка стабильна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️🟡️'
            elif rank_type == 0 and rank >= 4 and ranking == 0:
                abs_rank = f'📉️ Моментум у {self.stock} {rank_msg}\n' \
                         f'🟡 Финансовая оценка стабильна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - 📉️🟡️'

            elif rank_type == 1 and rank <= 3 and ranking == 3:
                abs_rank = f'⭐️⭐️⭐ Моментум {self.stock} {rank_msg}\n' \
                         f'🔴 Финансовая оценка негативна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐🔴️'
            elif rank_type == 1 and rank <= 3 and ranking == 2:
                abs_rank = f'⭐️⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🔴 Финансовая оценка негативна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️⭐️🔴️'
            elif rank_type == 1 and rank <= 3 and ranking == 1:
                abs_rank = f'⭐️ Моментум {self.stock} {rank_msg}\n' \
                         f'🔴 Финансовая оценка негативна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - ⭐️🔴️'
            elif rank_type == 1 and rank <= 3 and ranking == 1:
                abs_rank = f'📉️️ Моментум у {self.stock} {rank_msg}\n' \
                         f'🔴 Финансовая оценка негативна\n' \
                         f'{sma_sig_msg}' \
                         f'\n\n{self.stock} - 📉️️🔴️'

            else:
                abs_rank = f'\U000026A0 отсутствуют данные для оценки {self.stock} или крайне плохое ведение бизнеса'

            msg = f'```Вывод: ```\n\n{abs_rank}'
            print(rank, rank_type, abs_rank)
            return msg

    def stock_description_v3(self):
        msg1 = None
        msg2 = None
        msg3 = None
        try:
            description, rank, revenue_data = get_ranking_data3(self.stock)
        except Exception as e10:
            msg1 = 'Ошибка, попробуйте позже...'
            return msg1, msg2, msg3
        if len(description) == 0 and rank['rank'] is None and rank['data'] is None:
            return msg1, msg2, msg3
        if description['marketCap'] is not None:
            mc = round(float(description['marketCap'] / 1000000000), 2)
        else:
            mc = 'нет данных'
        if description['beta'] is not None:
            beta = round(float(description['beta']), 2)
        else:
            beta = 'нет данных'
        if description['volume'] is not None:
            vol = round(float(description['volume'] / 1000000), 4)
        else:
            vol = 0
        if description['averageVolume'] is not None:
            avol = round(float(description['averageVolume'] / 1000000), 4)
        else:
            avol = 0
        if description['trailingPE'] is not None:
            pe = round(float(description['trailingPE']), 2)
        else:
            pe = 0
        if description['forwardPE'] is not None:
            fpe = round(float(description['forwardPE']), 2)
        else:
            fpe = 'нет данных'
        if description['exDividendDate'] is not None:
            exDividendDate = description['exDividendDate']
        else:
            exDividendDate = 'нет данных'
        if description['dividendDate'] is not None:
            dividendDate = description['dividendDate']
        else:
            dividendDate = 'нет данных'
        if len(description['earnings_earningsDate']) == 0:
            earn = 'нет данных'
        else:
            earnings_earningsDate = description['earnings_earningsDate']
            earn = ' - '.join(map(str, earnings_earningsDate))

        msg1 = f"__Тикер:__ {str(description['ticker'])}\n" \
               f"__Компания:__ {str(description['longName'])}\n" \
               f"__Сектор:__ {str(description['sector'])}\n" \
               f"__Индустрия:__ {str(description['industry'])}\n" \
               f"__Страна:__ {str(description['country'])}\n \n" \
               f"__Капитализация:__ {str(mc)} Млрд\n" \
               f"__Объём:__ {str(vol)} Млн\n" \
               f"__Средний объём (3м):__ {str(avol)} Млн\n" \
               f"__P/E:__ {str(pe)} \n" \
               f"__Forward P/E:__ {str(fpe)} \n" \
               f"__Цена:__ {str(description['regularMarketPrice'])}\n" \
               f"__Состояние рынка:__ {str(description['marketState'])}\n" \
               f"__exDividend Date:__ {str(exDividendDate)}\n" \
               f"__Dividend Date:__ {str(dividendDate)}\n" \
               f"__Earnings Date:__ {str(earn)}\n"
        # f"__Тип:__ {str(description['quoteType'])}\n" \
        # f"__Бета:__ {str(beta)}\n" \

        msg2 = ''
        if ("is_fin" in rank and rank["is_fin"]) or ("is_bagger" in rank and rank["is_bagger"]):
            msg3 = {'other': 1, 'rank': rank['rank']}
        else:
            msg3 = {'other': 0, 'rank': rank['rank']}
        for k, v in rank.items():
            if k == "next_earning_date":
                next_earning_date = v
            elif k is None:
                msg2 = 'Нет данных для введённого тикера '
            elif k == 'rank':
                if ("is_fin" in rank and rank["is_fin"]) or ("is_bagger" in rank and rank["is_bagger"]):
                    msg2 += '\n' + ins.ranking_v3["other_rank"][v]
                else:
                    msg2 += '\n' + ins.ranking_v3[k][v]
            elif k == "is_fin" or k == "is_bagger":
                continue
            else:
                # print(rank)
                msg2 += '\n' + ins.ranking_v3[k][v]
        print('\n', msg1, '\n', msg2, '\n', msg3)  # TODO REMOVE!
        return msg1, msg2, msg3, revenue_data

    def stock_news(self):
        try:
            news = finviz.get_news(self.stock)
        except Exception as e10:
            msg = 'Описание для ETF недоступно'
            return msg
        msg = ''
        for n in news[0:15]:
            msg += ' '.join(n) + '\n' + '\n'
        return msg


def fin_news(blogs=False, rows=20):
    fnews = News()
    all_news = fnews.getNews()
    if blogs:
        news = all_news['blogs'][0:rows]
        news = news[(news.Source == "zerohedge") | (news.Source == "vantagepointtrading.com") | (
                news.Source == "seekingalpha.com")]
    else:
        news = all_news['news'][0:rows]
        news = news[(news.Source == "www.reuters.com") | (news.Source == "www.marketwatch.com") | (
                news.Source == "www.bloomberg.com")]
    news_list = []
    for index, row in news.iterrows():
        row = (row['Date'], row['Title'], row['Link'])
        news_list.append(row)
    msg = ''
    for n in news_list[0:rows]:
        msg += ' '.join(n) + '\n' + '\n'
    return msg


def none_to_str(s):
    if s is None:
        return '*'
    return str(s)

