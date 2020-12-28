from dataclasses import dataclass
from collections import Counter
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from quotes.sql_queries import *

from mlfinlab.portfolio_optimization import RiskEstimators, HierarchicalRiskParity, HierarchicalEqualRiskContribution
from mlfinlab.codependence import get_dependence_matrix, get_distance_matrix

"""
    etalon = RiskParityAllocator(closes=c_df, cov_method='empirical',
                                 herc=False, linkage_='average', risk_measure_='equal_weighting')
    rp2 = RiskParityAllocator(closes=c_df, cov_method='empirical',
                              herc=True, linkage_='ward', risk_measure_='variance')
"""


@dataclass
class RiskParityAllocator:
    __slots__ = [
        'asset_names_',
        'closes',
        'returns',

        'dependence_method',
        'distance_metric',
        'angular_distance',

        'cov_method',
        'graphs_show',

        'herc',
        'risk_measure_',
        'linkage_',
    ]
    """
    risk_measure supported string: 
    equal_weighting 
    variance
    standard_deviation
    expected_shortfall
    conditional_drawdown_risk
    """

    def __init__(self,
                 asset_names_: list = None,
                 closes: pd = None,
                 returns: pd = None,

                 dependence_method: str = 'distance_correlation',
                 distance_metric: str = 'angular',
                 angular_distance: bool = True,

                 cov_method: str = 'empirical',
                 graphs_show: bool = True,

                 herc: bool = True,
                 risk_measure_: str = 'conditional_drawdown_risk',
                 linkage_: str = 'ward'
                 ):
        self.asset_names_ = asset_names_
        self.closes = closes
        self.returns = returns

        self.dependence_method = dependence_method
        self.distance_metric = distance_metric
        self.angular_distance = angular_distance

        self.cov_method = cov_method
        self.graphs_show = graphs_show

        self.herc = herc
        self.risk_measure_ = risk_measure_
        self.linkage_ = linkage_

    def calc_returns(self):
        asset_names = self.closes.columns.tolist()
        df_pch = round(self.closes.pct_change(periods=1), 3)
        df_pch.dropna(inplace=True)
        self.asset_names_ = asset_names
        self.closes = self.closes
        self.returns = df_pch

    def distance_correlation(self):
        dist_corr = get_dependence_matrix(self.returns, self.dependence_method)
        if self.angular_distance:
            corr = get_distance_matrix(dist_corr, self.distance_metric)
        else:
            corr = get_dependence_matrix(self.returns, self.dependence_method)

        if self.graphs_show:
            cluster_map = sns.clustermap(corr, yticklabels=True)
            plt.figure(figsize=(10, 10))
            cluster_map.fig.suptitle('Distance Correlations', fontsize=15)
            plt.show()
        return corr

    def covariance(self):
        risk_est = RiskEstimators()

        if self.cov_method == 'empirical':
            cov = risk_est.empirical_covariance(returns=self.returns, price_data=False, assume_centered=False)
        elif self.cov_method == 'mcd':
            cov = risk_est.minimum_covariance_determinant(returns=self.returns, price_data=False, assume_centered=False)
        elif self.cov_method == 'semi':
            cov = risk_est.semi_covariance(returns=self.returns, price_data=False, )
        else:
            exit()
        if self.graphs_show:
            cluster_map = sns.clustermap(cov, yticklabels=True)
            plt.figure(figsize=(10, 10))
            cluster_map.fig.suptitle(f'{self.cov_method} Covariance Matrix', fontsize=15)
            plt.show()
        return cov

    def allocator(self):
        if self.herc:
            rp = HierarchicalEqualRiskContribution()
            rp.allocate(
                # asset_prices=self.closes,
                asset_returns=self.returns,
                covariance_matrix=self.covariance(),
                risk_measure=self.risk_measure_,
                linkage=self.linkage_,
                optimal_num_clusters=None)
            title = f'{self.cov_method} {self.linkage_} {self.risk_measure_} HERC Dendrogram'

        else:
            rp = HierarchicalRiskParity()
            rp.allocate(
                # asset_prices=self.closes,
                asset_returns=self.returns,
                covariance_matrix=self.covariance(),
                distance_matrix=self.distance_correlation(),
                linkage=self.linkage_)
            title = f'{self.cov_method} {self.linkage_} HRP Dendrogram'
        weights = rp.weights
        y_pos = np.arange(len(weights.columns))
        di = rp.weights.to_dict(orient='records')
        w = {}
        for k, v in di[0].items():
            w.update({k: v})
        if self.graphs_show:
            plt.figure(figsize=(17, 7))
            rp.plot_clusters(assets=self.asset_names_)
            plt.title(title, size=18)
            plt.xticks(rotation=45)

            plt.figure(figsize=(25, 7))
            plt.bar(list(weights.columns), weights.values[0])
            plt.xticks(y_pos, rotation=45, size=10)
            plt.xlabel('Assets', size=20)
            plt.ylabel('Weights %', size=20)
            plt.title(title + ' Weights', size=20)
            plt.show()

        # print(w)
        return w


@dataclass
class Selector:
    __slots__ = [
        'closes',
        'performance_period',
        'assets_to_hold',
        'selectors_mode'
    ]

    def __init__(self,
                 closes: pd = None,
                 performance_period: int = 63,  # 21,
                 assets_to_hold: int = 10,
                 selectors_mode: int = 0
                 ):
        self.closes = closes
        self.performance_period = performance_period
        self.assets_to_hold = assets_to_hold
        self.selectors_mode = selectors_mode

    def rs_sharpe(self):
        """
        :selectors_mode: 0 = RSI/rolling.Std(), 1 = RSI
        """
        df = self.closes
        columns = df.columns.tolist()
        _rs_sharpe = df.copy()
        for col in columns:
            delta = df[col].diff()
            delta = delta[1:]
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
            roll_up1 = up.ewm(span=self.performance_period).mean()
            roll_down1 = down.abs().ewm(span=self.performance_period).mean()
            rs = roll_up1 / roll_down1
            mrsi = 50.0 - (100.0 / (1.0 + rs))
            sharpe = mrsi / df[col].rolling(self.performance_period).std()
            if self.selectors_mode == 1:
                _rs_sharpe[col] = mrsi
            elif self.selectors_mode == 0:
                _rs_sharpe[col] = sharpe
            else:
                print('Mode doesnt exists')
                exit()
        _rs_sharpe.dropna(inplace=True)
        _rs_sharpe.drop_duplicates(inplace=True)
        sorting = _rs_sharpe.T.sort_values(_rs_sharpe.last_valid_index(), ascending=False).T
        slicing = sorting.columns.tolist()
        tickers_to_allocator = slicing[:self.assets_to_hold]
        # print(tickers_to_allocator)
        return tickers_to_allocator

    def momentum(self):
        df = self.closes
        columns = df.columns.tolist()
        momentum_df = df.copy()
        for col in columns:
            mom = (df[col] - df[col].shift(self.performance_period)) / df[col].shift(self.performance_period) * 100
            # mom = df[col].pct_change(periods=self.performance_period)
            # mom = mom[self.performance_period:]
            momentum_df[col] = mom
        momentum_df.dropna(inplace=True)
        momentum_df.drop_duplicates(inplace=True)
        sorting = momentum_df.T.sort_values(momentum_df.last_valid_index(), ascending=False).T
        slicing = sorting.columns.tolist()
        tickers_to_allocator = slicing[:self.assets_to_hold]
        # print(tickers_to_allocator)
        return tickers_to_allocator


def core_sat(cor=None, cor_perc=None, sat=None, sat_perc=None):
    for k, v in cor.items():
        cor.update({k: round(v * cor_perc, 3)})
    for k, v in sat.items():
        sat.update({k: round(v * sat_perc, 3)})

    port = Counter(cor) + Counter(sat)
    # print(dict(port))
    return dict(port)


def returns_calc(init_capital=100000, ohlc=None):
    cap_ohlc = {}
    shares = 0
    # Расчет OHLC
    for ticker in ohlc:
        for count, dohlcwac in enumerate(ohlc[ticker]):
            if count == 0:
                shares = int((init_capital * dohlcwac[5]) / dohlcwac[4])
            cap_in_open = round(shares * dohlcwac[1], 2)
            cap_in_hi = round(shares * dohlcwac[2], 2)
            cap_in_low = round(shares * dohlcwac[3], 2)
            cap_in_close = round(shares * dohlcwac[4], 2)
            cap_in_adjclose = round(shares * dohlcwac[6], 2)
            if dohlcwac[0] not in cap_ohlc:
                cap_ohlc[dohlcwac[0]] = (dohlcwac[0], cap_in_open, cap_in_hi, cap_in_low, cap_in_close, cap_in_adjclose)
            else:
                cap_ohlc[dohlcwac[0]] = (dohlcwac[0],
                                         round(cap_ohlc[dohlcwac[0]][1] + cap_in_open, 2),
                                         round(cap_ohlc[dohlcwac[0]][2] + cap_in_hi, 2),
                                         round(cap_ohlc[dohlcwac[0]][3] + cap_in_low, 2),
                                         round(cap_ohlc[dohlcwac[0]][4] + cap_in_close, 2),
                                         round(cap_ohlc[dohlcwac[0]][5] + cap_in_adjclose, 2))
    # Расчет Returns
    returns = {}
    for i, ohlc_date in enumerate(cap_ohlc):
        if i > 0:
            last_close = cap_ohlc[ohlc_date][-1]
            prev_close = cap_ohlc[prev_ohlc_date][-1]
            ret = round((last_close - prev_close) / prev_close, 2)
            returns[ohlc_date] = ret
        prev_ohlc_date = ohlc_date
    # debug(cap_ohlc.values())
    # debug(returns)
    return cap_ohlc.values(), returns


def returns_calc_old(init_capital=10000, ohlc=None):
    cap_ohlc = {}
    tmp = ohlc
    for k, v in ohlc.items():
        ticker_qty = init_capital * v[0][5]
        tmp[k].append(ticker_qty)
        tmp[k][-1] = round(ticker_qty / tmp[k][0][4])

    for k, v in tmp.items():
        ohlc_list = []
        cap_in_open = round(v[1] * v[0][1], 2)
        ohlc_list.append(cap_in_open)
        cap_in_hi = round(v[1] * v[0][2], 2)
        ohlc_list.append(cap_in_hi)
        cap_in_lo = round(v[1] * v[0][3], 2)
        ohlc_list.append(cap_in_lo)
        cap_in_close = round(v[1] * v[0][4], 2)
        ohlc_list.append(cap_in_close)
        cap_ohlc.update({k: ohlc_list})

    op, hi, lo, cl = 0, 0, 0, 0
    for k, v in cap_ohlc.items():
        op += v[0]
        hi += v[1]
        lo += v[2]
        cl += v[3]
    print([round(op, 2), round(hi, 2), round(lo, 2), round(cl, 2)])
    return [round(op, 2), round(hi, 2), round(lo, 2), round(cl, 2)]
