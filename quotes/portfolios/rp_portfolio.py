from dataclasses import dataclass
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from mlfinlab.portfolio_optimization import RiskEstimators, HierarchicalRiskParity, HierarchicalEqualRiskContribution
from mlfinlab.codependence import get_dependence_matrix, get_distance_matrix


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
        """
        :dependence_method: dependence_method=information_variation, mutual_information, distance_correlation,
        spearmans_rho, gpr_distance, gnpr_distance
        """
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
