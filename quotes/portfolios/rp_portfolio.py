from dataclasses import dataclass
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from  quotes.sql_queries import *

from mlfinlab.portfolio_optimization import RiskEstimators, HierarchicalRiskParity, HierarchicalEqualRiskContribution
from mlfinlab.codependence import get_dependence_matrix, get_distance_matrix


def get_rp_alloction(q_table_name, u_table_name, engine):
    closes_df = get_closes_universe_df(q_table_name, u_table_name, engine)
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
                 returns=None,
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
            returns=self.asset_returns_,
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
                 returns=None,
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

# def us_stock_filtration():
#     path = os.path.join(HOLDINGS, 'us_mega_caps.csv')
#     df = pd.read_csv(path, index_col='No.')
#     df.drop(columns={'P/E', 'Price', 'Change', 'Volume'}, axis=1, inplace=True)
#     df['Market Cap'] = df['Market Cap'].str.extract(r'(\d+.\d+)').astype(float)
#     df = df[df['Market Cap'] > 20.0]
#     df = df[df['Sector'] != 'Real Estate']
#     df = df[df['Sector'] != 'Financial']
#     df = df[df['Country'] == 'USA']
#     df.reset_index(drop=True, inplace=True)
#     ticker_list = df['Ticker'].tolist()
#     df.to_csv(os.path.join(HOLDINGS, 'filtered_us_mega_caps.csv'))
#     print('passed 1')
#     return ticker_list
#
#
# def momentum(filename=None):
#     path = os.path.join(HOLDINGS, filename)
#     data_df = pd.read_csv(path, index_col='Date', parse_dates=True)
#     columns = data_df.columns.tolist()
#     _mom = data_df.copy()
#     for col in columns:
#         symm1 = (data_df[col] - data_df[col].shift(21))/data_df[col].shift(21)
#         symm3 = (data_df[col] - data_df[col].shift(63))/data_df[col].shift(63)
#         zscore_m1 = (symm1 - symm1.rolling(252).mean())/symm1.rolling(252).std()
#         zscore_m3 = (symm3 - symm3.rolling(252).mean())/symm3.rolling(252).std()
#         _mom[col] = 0.5*zscore_m1 + 0.5*zscore_m3
#     _mom.dropna(inplace=True)
#     _mom.drop_duplicates(inplace=True)
#     _mom.to_csv(os.path.join(HOLDINGS, 'mtum_' + filename))
#     return _mom
#
#
# def rsi(filename=None, n=21):
#     path = os.path.join(HOLDINGS, filename)
#     data_df = pd.read_csv(path, index_col='Date', parse_dates=True)
#     columns = data_df.columns.tolist()
#     _rsi = data_df.copy()
#     for col in columns:
#         delta = data_df[col].diff()
#         delta = delta[1:]
#         up, down = delta.copy(), delta.copy()
#         up[up < 0] = 0
#         down[down > 0] = 0
#         roll_up1 = up.ewm(span=n).mean()
#         roll_down1 = down.abs().ewm(span=n).mean()
#         RS1 = roll_up1 / roll_down1
#         RSI1 = 100.0 - (100.0 / (1.0 + RS1))
#         _rsi[col] = RSI1
#     _rsi.dropna(inplace=True)
#     _rsi.drop_duplicates(inplace=True)
#     _rsi.to_csv(os.path.join(HOLDINGS, 'rsi_' + filename))
#     return _rsi
#
#
# def get_market_cap(ticker):
#     yf = YahooFinancials(ticker)
#     data = yf.get_market_cap()
#     return data
#
#
# def impulse_cap_sorting(filename=None):
#     df = pd.read_csv(os.path.join(HOLDINGS, filename), index_col='Date', parse_dates=True)
#     columns = df.columns.tolist()
#     mcap_mtum = df.copy()
#     last = df.iloc[[-1]]
#     for col in columns:
#         cap_mom = 0.5*last[col] * 0.5*get_market_cap(col)
#         print(col, '\n')
#         mcap_mtum[col+'_cap_mom'] = cap_mom
#         mcap_mtum.drop(columns={col}, axis=1, inplace=True)
#     mcap_mtum.dropna(inplace=True)
#     last_sorted = mcap_mtum.T.sort_values(mcap_mtum.last_valid_index(), ascending=False).T
#     last_sorted.to_csv(os.path.join(HOLDINGS, 'sorted_' + filename))
#     return last_sorted