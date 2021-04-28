import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from mlfinlab.codependence import get_dependence_matrix, get_distance_matrix

def angular_dist(ret_df_=None, distance_metric='angular', save_path=None, title=None):
    from scipy.cluster.hierarchy import ClusterWarning
    from warnings import simplefilter
    simplefilter("ignore", ClusterWarning)
    # Calculate absolute angular distance from a Pearson correlation matrix
    distance_corr_ = get_dependence_matrix(ret_df_, dependence_method='distance_correlation')
    angular_distance = get_distance_matrix(distance_corr_, distance_metric=distance_metric)
    sns.set(font_scale=0.95)

# def skew(returns):
#     """
#     calculates returns' skewness
#     (the degree of asymmetry of a distribution around its mean)
#     """
#     return _utils._prepare_returns(returns).skew()
#
# def ulcer_index(returns, rf=0):
#     """ calculates the ulcer index score (downside risk measurment) """
#     returns = _utils._prepare_returns(returns, rf)
#     dd = 1. - returns/returns.cummax()
#     return _np.sqrt(_np.divide((dd**2).sum(), returns.shape[0] - 1))
#
#
# def ulcer_performance_index(returns, rf=0):
#     """
#     calculates the ulcer index score
#     (downside risk measurment)
#     """
#     returns = _utils._prepare_returns(returns, rf)
#     dd = 1. - returns/returns.cummax()
#     ulcer = _np.sqrt(_np.divide((dd**2).sum(), returns.shape[0] - 1))
#     return returns.mean() / ulcer
#
# def value_at_risk(returns, sigma=1, confidence=0.95):
#     """
#     calculats the daily value-at-risk
#     (variance-covariance calculation with confidence n)
#     """
#     returns = _utils._prepare_returns(returns)
#     mu = returns.mean()
#     sigma *= returns.std()
#
#     if confidence > 1:
#         confidence = confidence/100
#
#     return _norm.ppf(1-confidence, mu, sigma)
#
# def conditional_value_at_risk(returns, sigma=1, confidence=0.95):
#     """
#     calculats the conditional daily value-at-risk (aka expected shortfall)
#     quantifies the amount of tail risk an investment
#     """
#     returns = _utils._prepare_returns(returns)
#     var = value_at_risk(returns, sigma, confidence)
#     c_var = returns[returns < var].values.mean()
#     return c_var if ~_np.isnan(c_var) else var

# def scatter():
#     df = pd.read_csv('/home/gene/projects/upsilon_one/results/inspector/data.csv')
#     sns.set(rc={'figure.facecolor': 'black', 'figure.edgecolor': 'black', 'xtick.color': 'white',
#                 'ytick.color': 'white', 'text.color': 'white', 'axes.labelcolor': 'white',
#                 'axes.facecolor': 'black', 'grid.color': '#17171a'})
#     sns.set_context('paper', font_scale=1.1)
#     # sns.set_context('talk', font_scale=1.1)
#     palette = sns.color_palette("RdYlGn_r", n_colors=10, as_cmap=False)
#     sns.despine()
#     ave_risk = df.iloc[2]
#     ave_alpha = df.iloc[0]
#     ave_premia = df.iloc[1]
#     vola = df.iloc[3]
#     plt.figure(figsize=(10, 6))
#     sns.scatterplot(data=df, x=ave_risk, y=ave_alpha, size=ave_premia,
#                     alpha=0.95, legend=True, sizes=(20, 500), hue=vola, markers=True, palette=palette)
#
#     # points = plt.scatter(ave_risk, ave_alpha,
#     #                      c=vola, s=20, cmap="jet")  # set style options
#     # plt.colorbar(points)
#     names = df.columns.tolist()
#
#     for line in range(0, df.shape[1]):
#         plt.text(df.iloc[2][line] + 0.1, df.iloc[0][line] + 0.1, names[line],
#                  horizontalalignment='left', size='x-small', color='white', weight='semibold')
#     #
#     # plt.text(11.75, -2.7, 'Premium',
#     #          horizontalalignment='left', size='small', color='white', weight='bold')
#     plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
#     plt.xlabel("Ave. Monthly Risk (%)")
#     plt.ylabel("Ave. Excess Return over Risk (%)")
#     # plt.tight_layout()
#     plt.suptitle('Risk-Premium Analysis', fontsize=25)
#     plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#     plt.savefig('/home/gene/projects/upsilon_one/results/inspector/data.png',
#                 facecolor='black', transparent=True, bbox_inches='tight')
#     plt.show()


def scatter():

