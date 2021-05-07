from dataclasses import dataclass
from collections import Counter
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from quotes.sql_queries import *

from portfoliolab.clustering import HierarchicalRiskParity, HierarchicalEqualRiskContribution
from portfoliolab.estimators import RiskEstimators
from math_stat.fin_stat import get_dependence_matrix, get_distance_matrix

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

        'cov_method',  # 'empirical' 'mcd' 'semi' 'shrinked' 'de'
        'shrinkage_type',  # 'basic' 'lw' 'oas'
        'denoise_method',  # 'const_resid_eigen' 'spectral' 'target_shrink'
        'detone',  # True / False
        'graphs_show',

        'herc',
        'risk_measure_',
        'linkage_',
        'selector_type',
        'std_adj',
        'assets_to_hold',
        'p1',
        'p2',
        'c_p1',
        'c_p2',

        'mkt_caps',
        'cap_weight',
        'cap_limit_1',
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
                 shrinkage_type: str = 'basic',
                 denoise_method: str = 'const_resid_eigen',
                 detone: bool = False,
                 graphs_show: bool = True,

                 herc: bool = True,
                 risk_measure_: str = 'conditional_drawdown_risk',
                 linkage_: str = 'ward',

                 selector_type: int = 1,
                 std_adj: bool = False,
                 assets_to_hold: int = 10,
                 p1: int = 21,
                 p2: int = 63,
                 c_p1: int = 1,
                 c_p2: int = 3,

                 mkt_caps: dict = None,
                 cap_weight: int = 0,
                 cap_limit_1: float = 0.13,
                 ):

        self.asset_names_ = asset_names_
        self.closes = closes
        self.returns = returns

        self.dependence_method = dependence_method
        self.distance_metric = distance_metric
        self.angular_distance = angular_distance

        self.cov_method = cov_method
        self.shrinkage_type = shrinkage_type
        self.denoise_method = denoise_method
        self.detone = detone
        self.graphs_show = graphs_show

        self.herc = herc
        self.risk_measure_ = risk_measure_
        self.linkage_ = linkage_

        self.selector_type = selector_type
        self.std_adj = std_adj
        self.assets_to_hold = assets_to_hold
        self.p1 = p1
        self.p2 = p2
        self.c_p1 = c_p1
        self.c_p2 = c_p2

        self.mkt_caps = mkt_caps
        self.cap_weight = cap_weight
        self.cap_limit_1 = cap_limit_1

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

    def covariance(self, kde_bwidth=0.01):
        risk_est = RiskEstimators()

        if self.cov_method == 'empirical':
            cov = risk_est.empirical_covariance(returns=self.returns, price_data=False, assume_centered=False)
        elif self.cov_method == 'mcd':
            cov = risk_est.minimum_covariance_determinant(returns=self.returns, price_data=False, assume_centered=False)
        elif self.cov_method == 'semi':
            cov = risk_est.semi_covariance(returns=self.returns, price_data=False, threshold_return=0)
        elif self.cov_method == 'shrinked':  # 'basic' 'lw' 'oas'
            cov = risk_est.shrinked_covariance(returns=self.returns, price_data=False,
                                               shrinkage_type=self.shrinkage_type,
                                               assume_centered=False, basic_shrinkage=0.1)

        elif self.cov_method == 'de':  # 'const_resid_eigen' 'spectral' 'target_shrink'
            # Relation of number of observations T to the number of variables N (T/N)
            tn_relation = self.closes.shape[0] / self.closes.shape[1]

            cov_matrix = risk_est.empirical_covariance(returns=self.returns, price_data=False, assume_centered=False)
            cov = risk_est.denoise_covariance(cov_matrix, tn_relation, denoise_method=self.denoise_method,
                                              detone=self.detone, market_component=1, kde_bwidth=kde_bwidth)
        elif self.cov_method == 'de2':  # 'const_resid_eigen' 'spectral' 'target_shrink'
            # Relation of number of observations T to the number of variables N (T/N)
            tn_relation = self.closes.shape[0] / self.closes.shape[1]

            cov_matrix = risk_est.minimum_covariance_determinant(returns=self.returns, price_data=False, assume_centered=False)
            cov = risk_est.denoise_covariance(cov_matrix, tn_relation, denoise_method=self.denoise_method,
                                              detone=self.detone, market_component=1, kde_bwidth=kde_bwidth)

        elif self.cov_method == 'de3':  # 'const_resid_eigen' 'spectral' 'target_shrink'
            # Relation of number of observations T to the number of variables N (T/N)
            tn_relation = self.closes.shape[0] / self.closes.shape[1]

            cov_matrix = risk_est.shrinked_covariance(returns=self.returns, price_data=False,
                                               shrinkage_type='lw',
                                               assume_centered=False, basic_shrinkage=0.1)
            cov = risk_est.denoise_covariance(cov_matrix, tn_relation, denoise_method=self.denoise_method,
                                              detone=self.detone, market_component=1, kde_bwidth=kde_bwidth)
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
        mcaps = {}
        temp = {}
        if self.cap_weight == 0:
            for k, v in di[0].items():
                w.update({k: v})

        elif self.cap_weight > 0:
            for k, v in di[0].items():
                w.update({k: v})

            final_dict = {x: self.mkt_caps[x] for x in self.mkt_caps if x in w}
            total_cap = sum(final_dict.values())

            for k, v in final_dict.items():
                mcaps.update({k: v / total_cap})

            # debug(f"MCAPS={mcaps}")
            for k in mcaps:
                if mcaps[k] > self.cap_limit_1:
                    temp.update({k: mcaps[k] - self.cap_limit_1})
                    # debug(f"temp={temp}")
                    excess = sum(temp.values())
                    # debug(f"excess={excess}")
                    # debug(f"len(mcaps.keys()={len(mcaps.keys())}")
                    # debug(f"len(temp.keys()={len(temp.keys())}")
                    if len(mcaps.keys()) - len(temp.keys()) > 0:
                        qty = excess / (len(mcaps.keys()) - len(temp.keys()))
                    elif len(mcaps.keys()) - len(temp.keys()) == 0:
                        qty = excess / len(mcaps.keys())
                    mcaps.update({k: self.cap_limit_1})

            for k1 in mcaps:
                if mcaps[k1] < self.cap_limit_1:
                    mcaps.update({k1: mcaps[k1] + qty})

            pr_weight = 1 - self.cap_weight
            cap_rp = {k: self.cap_weight * mcaps[k] + pr_weight * w[k] for k in w}
            w = cap_rp

        elif self.cap_weight > 1:
            print('Control Error')
            return
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
                zs_1 = (mom_1 - mom_1.rolling(window - self.p1).mean()) / mom_1.rolling(window - self.p1).std()
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
                zs_1 = (mom_1 - mom_1.rolling(window - self.p1).mean()) / mom_1.rolling(window - self.p1).std()
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
                df1 = date_slicer(df_=df, c_period=self.c_p1)
                mom1 = ((df1[col].iloc[-1] - df1[col].iloc[0]) / df1[col].iloc[0])

                df2 = date_slicer(df_=df, c_period=self.c_p2)
                mom2 = ((df2[col].iloc[-1] - df2[col].iloc[0]) / df2[col].iloc[0])
                performance_df[col] = 0.5 * mom1 + 0.5 * mom2

            elif self.selector_type == 13:  # %Ch 2 periods Calendar zs
                df1 = date_slicer(df_=df, c_period=self.c_p1)
                rets1 = df1[col].pct_change()
                mom1 = ((df1[col].iloc[-1] - df1[col].iloc[0]) / df1[col].iloc[0])
                zs_1 = (mom1 - rets1.mean()) / rets1.std()
                df2 = date_slicer(df_=df, c_period=self.c_p2)
                rets2 = df2[col].pct_change()
                mom2 = ((df2[col].iloc[-1] - df2[col].iloc[0]) / df2[col].iloc[0])
                zs_2 = (mom2 - rets2.mean()) / rets2.std()
                performance_df[col] = 0.5 * zs_1 + 0.5 * zs_2


            elif self.selector_type == 14:  # %Ch 2 periods Calendar
                df1 = date_slicer(df_=df, c_period=self.c_p1)
                mom1 = ((df1[col].iloc[-1] - df1[col].iloc[0]) / df1[col].iloc[0])

                pct_df1 = date_slicer(df_=df, c_period=self.c_p1 + 1)
                pct1 = ((pct_df1[col].iloc[-1] - pct_df1[col].iloc[0]) / pct_df1[col].iloc[0])

                df2 = date_slicer(df_=df, c_period=self.c_p2)
                mom2 = ((df2[col].iloc[-1] - df2[col].iloc[0]) / df2[col].iloc[0])
                performance_df[col] = 0.4 * mom1 + 0.4 * mom2 + 0.2 * pct1

            elif self.selector_type == 20:  # %Ch Calendar
                df1 = date_slicer(df_=df, c_period=self.c_p1)
                mom = ((df1[col].iloc[-1] - df1[col].iloc[0]) / df1[col].iloc[0])
                performance_df[col] = mom

            elif self.selector_type == 21:  # %Ch 2 periods Calendar
                df1 = date_slicer(df_=df, c_period=self.c_p1)
                mom1 = ((df1[col].iloc[-1] - df1[col].iloc[0]) / df1[col].iloc[0])
                df2 = date_slicer(df_=df, c_period=self.c_p2)
                mom2 = ((df2[col].iloc[-1] - df2[col].iloc[0]) / df2[col].iloc[0])
                performance_df[col] = 0.5 * mom1 + 0.5 * mom2

            elif self.selector_type == 100:  # 'Head of Universe'
                performance_df[col] = df[col]

            # elif self.selector_type == 14:  # Down GLS Calendar zs
            #
            #     dn = 0
            #     df1 = date_slicer(df_=df, c_period=self.c_p1)
            #     if df1[col].pct_change() < 0:
            #         rets1 = df1[col].pct_change()
            #         dn += 1
            #     dn_prob = dn / window-1
            #     gls = 1 - (rets1 * dn_prob)
            #     sma_gls = gls.mean()
            #     zs_1 = (-1)*(sma_gls - rets1.mean()) / rets1.std()
            #     performance_df[col] = zs_1

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
    prev_ohlc_date = -1
    for i, ohlc_date in enumerate(cap_ohlc):
        if i > 0:
            last_close = cap_ohlc[ohlc_date][-1]
            prev_close = cap_ohlc[prev_ohlc_date][-1]
            ret = round((last_close - prev_close) / prev_close, 4)
            returns[ohlc_date] = ret
        prev_ohlc_date = ohlc_date
    # debug(cap_ohlc.values())
    # debug(returns)
    return cap_ohlc.values(), returns


def returns_calc_w(init_capital=100000, data=None):
    res_ohlc = {}
    res_ret = {}
    shares = 0
    in_cap = init_capital
    # Расчет OHLC
    for did in data:
        cap_ohlc = {}
        for ticker in data[did]:
            for count, dohlcwac in enumerate(data[did][ticker]):
                if count == 0:
                    shares = int((in_cap * dohlcwac[5]) / dohlcwac[4])
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
        prev_ohlc_date = -1
        for i, ohlc_date in enumerate(cap_ohlc):
            if i > 0:
                last_close = cap_ohlc[ohlc_date][-1]
                prev_close = cap_ohlc[prev_ohlc_date][-1]
                ret = round((last_close - prev_close) / prev_close, 4)
                returns[ohlc_date] = ret
            prev_ohlc_date = ohlc_date

        c_val = list(cap_ohlc.values())
        cash = round(in_cap - c_val[0][4], 2)
        if cash > 0:
            in_cap = round(c_val[-1][4] + cash, 2)
        res_ohlc.update(cap_ohlc)
        res_ret.update(returns)
    return res_ohlc.values(), res_ret
