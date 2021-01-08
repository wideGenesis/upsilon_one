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
        'selector_type',
        'std_adj',
        'assets_to_hold',
        'p1',
        'p2'
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
                 linkage_: str = 'ward',

                 selector_type: int = 1,
                 std_adj: bool = False,
                 assets_to_hold: int = 10,
                 p1: int = 21,
                 p2: int = 63,

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

        self.selector_type = selector_type
        self.std_adj = std_adj
        self.assets_to_hold = assets_to_hold
        self.p1 = p1
        self.p2 = p2

    def closes_updater(self, new_closes=None):
        self.closes = new_closes

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

    def selector(self):
        df = self.closes
        columns = df.columns.tolist()
        performance_df = df.copy()
        window = df.shape[0]
        for col in columns:
            if self.selector_type == 0:  # RSI Roll
                delta = df[col].diff()
                delta = delta[1:]
                up, down = delta.copy(), delta.copy()
                up[up < 0] = 0
                down[down > 0] = 0
                roll_up1 = up.ewm(span=window).mean()
                roll_down1 = down.abs().ewm(span=window).mean()
                rs = roll_up1 / roll_down1
                rsi = 100.0 / (1.0 + rs)
                performance_df[col] = rsi

            elif self.selector_type == 1:  # Mom Roll zs
                rets = df[col].pct_change()
                rets = rets[~np.isnan(rets)]
                # lwma Weighting
                weights_1 = np.arange(1, self.p1 + 1)
                mom_1 = rets.rolling(self.p1).apply(lambda x: np.dot(x, weights_1) / weights_1.sum())
                # Z-Score
                zs_1 = (mom_1 - mom_1.rolling(window - self.p2).mean()) / mom_1.rolling(window - self.p2).std()
                performance_df[col] = zs_1

            elif self.selector_type == 2:  # Mom 2 periods Roll zs
                rets = df[col].pct_change()
                rets = rets[~np.isnan(rets)]
                # lwma Weighting
                weights_1 = np.arange(1, self.p1 + 1)
                weights_2 = np.arange(1, self.p2 + 1)
                mom_1 = rets.rolling(self.p1).apply(lambda x: np.dot(x, weights_1) / weights_1.sum())
                mom_2 = rets.rolling(self.p2).apply(lambda x: np.dot(x, weights_2) / weights_2.sum())
                # Z-Score
                zs_1 = (mom_1 - mom_1.rolling(window - self.p2).mean()) / mom_1.rolling(window - self.p2).std()
                zs_2 = (mom_2 - mom_2.rolling(window - self.p2).mean()) / mom_2.rolling(window - self.p2).std()
                performance_df[col] = 0.5 * zs_1 + 0.5 * zs_2

            elif self.selector_type == 10:  # %Ch Calendar
                mom = ((df[col].iloc[-1] - df[col].iloc[0]) / df[col].iloc[0])
                # mom = df[col].pct_change(periods=self.performance_lookback)
                performance_df[col] = mom

            elif self.selector_type == 11:  # %Ch Calendar zs
                rets = df[col].pct_change()
                mom_1 = ((df[col].iloc[-1] - df[col].iloc[0]) / df[col].iloc[0])
                # Z-Score
                zs_1 = (mom_1 - rets.mean()) / rets.std()
                performance_df[col] = zs_1

            elif self.selector_type == 12:  # %Ch 2 periods Calendar
                df1 = date_slicer(df_=df, c_period=1)
                mom1 = ((df1[col].iloc[-1] - df1[col].iloc[0]) / df1[col].iloc[0])

                df2 = date_slicer(df_=df, c_period=3)
                mom2 = ((df2[col].iloc[-1] - df2[col].iloc[0]) / df2[col].iloc[0])
                performance_df[col] = 0.75*mom1 + 0.25*mom2

            elif self.selector_type == 13:  # %Ch 2 periods Calendar zs
                df1 = date_slicer(df_=df, c_period=1)
                rets1 = df1[col].pct_change()
                mom1 = ((df1[col].iloc[-1] - df1[col].iloc[0]) / df1[col].iloc[0])
                zs_1 = (mom1 - rets1.mean()) / rets1.std()
                df2 = date_slicer(df_=df, c_period=3)
                rets2 = df2[col].pct_change()
                mom2 = ((df2[col].iloc[-1] - df2[col].iloc[0]) / df2[col].iloc[0])
                zs_2 = (mom2 - rets2.mean()) / rets2.std()
                performance_df[col] = 0.75*zs_1 + 0.25*zs_2

        performance_df.dropna(inplace=True)
        performance_df.drop_duplicates(inplace=True)
        # print('%%%%%%%% before', performance_df.tail(10))
        sorting = performance_df.T.sort_values(performance_df.last_valid_index(), ascending=False).T
        # print('%%%%%%%% after', sorting.tail(10))
        slicing = sorting.columns.tolist()
        tickers_to_allocator = slicing[:self.assets_to_hold]
        # print(tickers_to_allocator)
        return tickers_to_allocator


def date_slicer(df_=None, c_period=1):
    last_date_month = df_.index[-1].month
    df_.index = pd.to_datetime(df_.index)
    df_filtered = pd.DataFrame()
    for m in range(c_period - 1, -1, -1):
        if last_date_month - m > 0:
            mask = df_.index.month == last_date_month - m
            df_filtered = df_filtered.append(df_[mask])
        elif last_date_month - m <= 0:
            mask = df_.index.month == 12 + (last_date_month - m)
            df_filtered = df_filtered.append(df_[mask])
        return df_filtered


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
