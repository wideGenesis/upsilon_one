from dataclasses import dataclass
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from quotes.sql_queries import *

from mlfinlab.portfolio_optimization import RiskEstimators, HierarchicalRiskParity, HierarchicalEqualRiskContribution
from mlfinlab.codependence import get_dependence_matrix, get_distance_matrix


def get_rp_alloction(q_table_name, u_table_name, engine):
    closes_df = get_closes_universe_df(q_table_name, u_table_name, 9287523328, engine)
    print(str(closes_df))


@dataclass
class RiskParityAllocator:
    __slots__ = [
        'closes',
        'returns',
        'dependence_method',
        'distance_metric',
        'angular_distance',
        'corr_matrix_show',
        'herc',
        'asset_names_',
        'asset_prices_',
        'asset_returns_',
        'risk_measure_',
        'linkage_',
    ]

    def __init__(self,
                 closes=None,
                 returns: pd = None,
                 dependence_method: str = 'distance_correlation',
                 distance_metric: str = 'angular',
                 corr_matrix_show: bool = True,
                 angular_distance: bool = True,
                 herc: bool = True,
                 asset_names_: list = None,
                 asset_prices_: pd = None,
                 asset_returns_: pd = None,
                 risk_measure_: str = 'conditional_drawdown_risk',
                 linkage_: str = 'ward'
                 ):
        self.closes = closes
        self.returns = returns
        self.dependence_method = dependence_method
        self.distance_metric = distance_metric
        self.angular_distance = angular_distance
        self.corr_matrix_show = corr_matrix_show
        self.herc = herc
        self.asset_names_ = asset_names_
        self.asset_prices_ = asset_prices_
        self.asset_returns_ = asset_returns_
        self.risk_measure_ = risk_measure_
        self.linkage_ = linkage_

    def returns_(self):
        df = pd.DataFrame(data=self.closes)
        df_pch = round(df.pct_change(periods=1), 3)
        df_pch.dropna(inplace=True)
        self.returns = df_pch
        print(self.returns.head())

    def distance_correlation(self):
        dist_corr = get_dependence_matrix(self.returns, self.dependence_method)
        if self.angular_distance:
            corr = get_distance_matrix(dist_corr, self.distance_metric)
        else:
            corr = get_dependence_matrix(self.returns, self.dependence_method)

        if self.corr_matrix_show:
            cluster_map = sns.clustermap(corr, yticklabels=True)
            plt.figure(figsize=(10, 10))
            cluster_map.fig.suptitle('Distance Correlations', fontsize=15)
            plt.show()
        return corr

    def covariance(self):
        cov = RiskEstimators.empirical_covariance(
            returns=self.returns_,
            price_data=False,
            assume_centered=False)
        if self.corr_matrix_show:
            cluster_map = sns.clustermap(cov, yticklabels=True)
            plt.figure(figsize=(10, 10))
            cluster_map.fig.suptitle('Empirical Covariance Matrix', fontsize=15)
            plt.show()
        return cov

    def allocator(self):
        if self.herc:
            rp = HierarchicalEqualRiskContribution()
            rp.allocate(
                asset_names=self.asset_names_,
                asset_prices=self.asset_prices_,
                asset_returns=self.asset_returns_,
                covariance_matrix=self.distance_correlation(),
                risk_measure=self.risk_measure_,
                linkage=self.linkage_,
                optimal_num_clusters=None)
            di = rp.weights.to_dict(orient='records')
            w = {}
            for k, v in di[0].items():
                w.update({k: v})
            plt.figure(figsize=(17, 7))
            rp.plot_clusters(assets=self.asset_names_)
            plt.title(f'{self.risk_measure_} {self.linkage_} HERC Dendrogram', size=18)
            plt.xticks(rotation=45)
            plt.show()
            return w
        else:
            rp = HierarchicalRiskParity()
            rp.allocate(
                asset_names=self.asset_names_,
                asset_prices=self.asset_prices_,
                asset_returns=self.asset_returns_,
                covariance_matrix=self.distance_correlation(),
                distance_matrix=self.distance_correlation(),
                linkage=self.linkage_)
            di = rp.weights.to_dict(orient='records')
            w = {}
            for k, v in di[0].items():
                w.update({k: v})
            plt.figure(figsize=(17, 7))
            rp.plot_clusters(assets=self.asset_names_)
            plt.title(f'HRP_lab {self.linkage_} HERC Dendrogram', size=18)
            plt.xticks(rotation=45)
            plt.show()
            return w


@dataclass
class Selector:
    __slots__ = [
        'closes',
        'performance_period',
        'mcap_reduction',
        'assets_to_hold'
    ]

    def __init__(self,
                 closes: pd = None,
                 performance_period: int = 21,
                 mcap_reduction: int = 20000000000,
                 assets_to_hold: int = 10
                 ):
        self.closes = closes
        self.performance_period = performance_period
        self.mcap_reduction = mcap_reduction
        self.assets_to_hold = assets_to_hold

    def cap_reduction(self, closes, mcap_reduction):
        df = closes  # "(index_col=\"Date\", parse_dates=True)"
        columns = df.columns.tolist()
        rsharpe = df.copy()
        df = df[df['Market Cap'] > 20.0]
        df.reset_index(drop=True, inplace=True)
        ticker_list = df['Ticker'].tolist()
        return ticker_list

    def rs_sharpe(self, closes, performance_period, assets_to_hold):
        df = closes  # "(index_col=\"Date\", parse_dates=True)"
        columns = df.columns.tolist()
        _rs_sharpe = df.copy()
        for col in columns:
            delta = df[col].diff()
            delta = delta[1:]
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
            roll_up1 = up.ewm(span=performance_period).mean()
            roll_down1 = down.abs().ewm(span=performance_period).mean()
            rs = roll_up1 / roll_down1
            mrsi = 50.0 - (100.0 / (1.0 + rs))
            sharpe = mrsi / df[col].rolling(performance_period).std()
            _rs_sharpe[col] = sharpe
        _rs_sharpe.dropna(inplace=True)
        _rs_sharpe.drop_duplicates(inplace=True)
        tickers_to_allocator = _rs_sharpe.T.sort_values(_rs_sharpe.last_valid_index(), ascending=False).T
        tickers_to_allocator = tickers_to_allocator[1:performance_period]
        return tickers_to_allocator



