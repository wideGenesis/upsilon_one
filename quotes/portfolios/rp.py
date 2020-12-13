# import os
# import sys
# import yaml
# import datetime
# import pandas as pd
# import numpy as np
# from pandas_datareader import data
# import requests_cache
# from matplotlib import pyplot as plt
# from pandas.plotting import register_matplotlib_converters
# import matplotlib.patches as mpatches
# import seaborn as sns
#
# from mlfinlab.portfolio_optimization import RiskEstimators, HierarchicalRiskParity
# from mlfinlab.portfolio_optimization.herc import HierarchicalEqualRiskContribution
# from mlfinlab.online_portfolio_selection import *
# from mlfinlab.codependence import get_dependence_matrix, get_distance_matrix
#
# from pypfopt.risk_models import risk_matrix, CovarianceShrinkage, semicovariance, cov_to_corr
# from pypfopt.hierarchical_portfolio import HRPOpt
# from pypfopt.plotting import _plot_io, plot_dendrogram, plot_weights
#
#
#
# conf = yaml.safe_load(open('/home/gene/projects/nauvoo/settings.yaml'))
# PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# sys.path.append(PYTHON_PATH)
# os.environ["PYTHONUNBUFFERED"] = "1"
#
# YAHOO_PATH = conf['PATHS']['YAHOO_PATH']
# HOLDINGS = conf['PATHS']['HOLDINGS']
# LOGS = conf['PATHS']['LOGS']
#
#
# def coins_merge(coins_list):
#     main_df = pd.DataFrame()
#     for coin in coins_list:
#         path = os.path.join('/home/gene/projects/nauvoo/all-weather-risk-parity/data', f'{coin}.csv')
#         coins_df = pd.read_csv(path, index_col='date', parse_dates=True)
#         coins_df.rename({'adjusted_close': f'{coin}'}, axis=1, inplace=True)
#         if len(main_df) == 0:
#             main_df = coins_df
#         else:
#             main_df = pd.merge(main_df, coins_df, left_index=True, right_index=True)
#     main_df.dropna(inplace=True)
#     path = os.path.join('/home/gene/projects/nauvoo/portfolio strategies', 'all_coins.csv')
#     main_df.to_csv(path, index_label='Date')
#     print('Coins Data preparation complete!')
#
#
# def asset_download(asset_list, start_, end_, path_=None, filename=None, session_=None):
#     asset_df = pd.DataFrame([data.DataReader(ticker, 'yahoo', start_, end_, session=session_)['Close']
#                              for ticker in asset_list]).T
#     asset_df.columns = asset_list
#     asset_df.to_csv(os.path.join(path_, filename), index_label='Date')
#     print('Assets Data download complete!')
#
#
# def resample(path_=None, filename=None, adj_close=False, resample_to='M'):
#     if adj_close:
#         close = 'Adj Close'
#     else:
#         close = 'Close'
#     logic = {'Open': 'first',
#              'High': 'max',
#              'Low': 'min',
#              close: 'last',
#              'Volume': 'sum'}
#
#     offset = pd.offsets.timedelta(days=-6)
#     path = os.path.join(path_, filename)
#     df = pd.read_csv(path_=path, filename=None, index_col='Date', parse_dates=True)
#     df.resample(resample_to=resample_to, loffset=offset).apply(logic)
#     return df
#
#
# def returns(file_path=None, filename=None):
#     df = pd.read_csv(os.path.join(file_path, filename), index_col='Date', parse_dates=True)
#     df_pch = df.pct_change(periods=1)
#     df_pch.dropna(inplace=True)
#     return df_pch
#
#
# def momentum(path_=None, filename=None, mar=1.25):
#     path = os.path.join(path_, filename)
#     data_df = pd.read_csv(path, index_col='Date', parse_dates=True)
#     columns = data_df.columns.tolist()
#     _mom = data_df.copy()
#     mar = mar / 252
#     for col in columns:
#         symm1 = (data_df[col] - data_df[col].shift(21))/data_df[col].shift(21)
#         symm3 = (data_df[col] - data_df[col].shift(42))/data_df[col].shift(42)
#         zscore_m1 = (symm1 - symm1.rolling(63).mean()) / symm1.rolling(63).std()
#         zscore_m3 = (symm3 - symm3.rolling(63).mean())/symm3.rolling(63).std()
#         diff = (0.5*zscore_m1 + 0.5*zscore_m3) * (-1)
#         downside = np.where(diff < 0, 0, diff)
#         _mom[col+'_mtum'] = downside
#         _mom.drop(columns={col}, axis=1, inplace=True)
#     _mom.dropna(inplace=True)
#     _mom.drop_duplicates(inplace=True)
#     # _mom.to_csv(path_ + filename + '_mtum.csv')
#     return _mom
#
#
# def covar(df_, returns_data_=True, cov_method='min_cov_determinant', delta_=0.35):
#     """
#     :param df_:
#     :param returns_data_:
#     :param cov_method:
#         sample_cov
#         semicovariance
#         exp_cov
#         min_cov_determinant
#         ledoit_wolf
#         ledoit_wolf_constant_variance
#         ledoit_wolf_single_factor
#         ledoit_wolf_constant_correlation
#         oracle_approximating
#     :param delta_:
#     :return:
#     """
#
#     risk_est = RiskEstimators()
#     if cov_method == 'sample_cov':
#         cov_ = risk_matrix(prices=df_, returns_data=returns_data_, method=cov_method)
#     elif cov_method == 'exp_cov':
#         cov_ = risk_matrix(prices=df_, returns_data=returns_data_, method=cov_method)
#     elif cov_method == 'min_cov_determinant':
#         cov_ = risk_matrix(prices=df_, returns_data=returns_data_, method=cov_method)
#     elif cov_method == 'ledoit_wolf':
#         cov_ = risk_matrix(prices=df_, returns_data=returns_data_, method=cov_method)
#     elif cov_method == 'ledoit_wolf_constant_variance':
#         cov_ = risk_matrix(prices=df_, returns_data=returns_data_, method=cov_method)
#     elif cov_method == 'ledoit_wolf_single_factor':
#         cov_ = risk_matrix(prices=df_, returns_data=returns_data_, method=cov_method)
#     elif cov_method == 'oracle_approximating':
#         cov_ = risk_matrix(prices=df_, returns_data=returns_data_, method=cov_method)
#     elif cov_method == 'ledoit_wolf_constant_correlation':
#         cov_ = risk_matrix(prices=df_, returns_data=returns_data_, method=cov_method)
#     elif cov_method == 'semicovariance':
#         cov_ = semicovariance(prices=df_, returns_data=returns_data_, benchmark=0, frequency=252)
#     elif cov_method == 'ledoit_wolf_shrinkage':
#         cov_ = CovarianceShrinkage(prices=df_, returns_data=returns_data_, frequency=252).ledoit_wolf()
#     elif cov_method == 'oracle_approximating_shrinkage':
#         cov_ = CovarianceShrinkage(prices=df_, returns_data=returns_data_, frequency=252).oracle_approximating()
#     elif cov_method == 'shrunk_covariance':
#         cov_ = CovarianceShrinkage(prices=df_, returns_data=returns_data_, frequency=252).shrunk_covariance(
#             delta=delta_)
#
#     else:
#         raise ValueError('Invalid method of cov')
#     plt.figure(figsize=(10, 10))
#     g = sns.clustermap(cov_, yticklabels=True)
#     g.fig.suptitle(f'{cov_method} matrix of Returns', fontsize=15)
#     plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)  # ytick rotate
#     # plt.savefig('cov.png')
#     plt.show()
#     return cov_
#
#
# def distance_corr(ret_df_=None):
#     # Calculate distance correlation matrix
#     distance_corr_ = get_dependence_matrix(ret_df_, dependence_method='distance_correlation')
#     # dependence_method=information_variation, mutual_information,
#     # distance_correlation, spearmans_rho, gpr_distance, gnpr_distance
#     distance_corr_.to_csv('distance_corr.csv')
#     plt.figure(figsize=(10, 10))
#     g = sns.clustermap(distance_corr_, yticklabels=True)
#     g.fig.suptitle('distance_corr', fontsize=15)
#     plt.show()
#     return distance_corr
#
#
# def angular_dist(ret_df_=None, distance_metric='angular'):
#     # Calculate absolute angular distance from a Pearson correlation matrix
#     distance_corr_ = get_dependence_matrix(ret_df_, dependence_method='distance_correlation')
#     angular_dist = get_distance_matrix(distance_corr_, distance_metric=distance_metric)
#     # angular, squared_angular, and absolute_angular.
#     angular_dist.to_csv('angular_dist.csv')
#     plt.figure(figsize=(10, 10))
#     g = sns.clustermap(angular_dist)
#     g.fig.suptitle('angular_dist', fontsize=15)
#     plt.show()
#
#
# def herc(asset_list_=None, path_=None, filename=None, returns_=None, cov_=None,
#          risk_measure_='conditional_drawdown_risk', linkage_='ward'):
#     """
#     :param asset_list_: list
#     :param path_: path
#     :param filename: csv
#     :param returns_: df
#     :param cov_:
#     :param risk_measure_:
#         'equal_weighting'
#         'standard_deviation'
#         'variance'
#         'expected_shortfall'
#         'conditional_drawdown_risk'
#     :param linkage_:
#         'complete'
#         'ward'
#     :return:
#     """
#     herc_ = HierarchicalEqualRiskContribution()
#     path = os.path.join(path_, filename)
#     prices_df = pd.read_csv(path, index_col='Date', parse_dates=True)
#     herc_.allocate(asset_names=asset_list_,
#                    asset_prices=prices_df,
#                    asset_returns=returns_,
#                    covariance_matrix=cov_,
#                    risk_measure=risk_measure_,
#                    optimal_num_clusters=6,
#                    linkage=linkage_)
#     print(f'{risk_measure_} Portfolio Weights - {linkage_} \n', herc_.weights)
#     di = herc_.weights.to_dict(orient='records')
#     w = {}
#     for k, v in di[0].items():
#         w.update({k: v})
#     plt.figure(figsize=(17, 7))
#     herc_.plot_clusters(assets=asset_list_)
#     plt.title(f'{risk_measure_} {linkage_} HERC Dendrogram', size=18)
#     plt.xticks(rotation=45)
#     plt.show()
#     return w
#
#
# def hrp(returns_=None, cov_matrix_=None, name_=None):
#     rp = HRPOpt(returns=returns_, cov_matrix=cov_matrix_)
#     weights = rp.optimize()
#     cleaned_weights = rp.clean_weights()
#     # rp.save_weights_to_file("weights.txt")  # saves to file
#     print(cleaned_weights)
#     rp.portfolio_performance(verbose=True)
#     _plot_io(filename=f'{name_}_pypfopt', dpi=300, showfig=True)
#     plot_dendrogram(hrp=rp, show_tickers=True, filename=f'{name_}_pypfopt_dendro', showfig=True)
#     plot_weights(weights=weights)
#
#
# def hrp_lab(asset_list_=None, path_=None, filename=None, returns_=None, cov_=None,
#             distance_matrix_=None, linkage_='ward'):
#     hrp_l = HierarchicalRiskParity()
#     path = os.path.join(path_, filename)
#     prices_df = pd.read_csv(path, index_col='Date', parse_dates=True)
#     hrp_l.allocate(asset_names=asset_list_,
#                    asset_prices=prices_df,
#                    asset_returns=returns_,
#                    covariance_matrix=cov_,
#                    distance_matrix=distance_matrix_,
#                    linkage=linkage_)
#     print(f'HRP_lab Portfolio Weights - {linkage_} \n', hrp_l.weights.sort_values(by=0, ascending=False, axis=1))
#     di = hrp_l.weights.to_dict(orient='records')
#     w = {}
#     for k, v in di[0].items():
#         w.update({k: v})
#     plt.figure(figsize=(17, 7))
#     hrp_l.plot_clusters(assets=asset_list_)
#     plt.title(f'HRP_lab {linkage_} HERC Dendrogram', size=18)
#     plt.xticks(rotation=45)
#     plt.show()
#     plot_weights(weights=w)
#     return w
#
#
# # ========================================  Execute  ==========================================================
# register_matplotlib_converters()
#
# expire_after = datetime.timedelta(days=3)
# session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
# start = datetime.datetime(2019, 1, 1)
# end = datetime.datetime.utcnow()
# # assets = ["TMF", "TLT", "QLD", "FBT", "AAPL", "AMZN", "MSFT", "NVDA", "PEP", "ADBE", "AMGN", "COST", "FB", "GOOG"]
# # assets = [
# #     "QQQ",
# #     "TLT",
# #     "XLP",
# #     'NEE',
# #     "FBT",
# #     'BKNG',
# #     "AAPL",
# #     "AMZN",
# #     "MSFT",
# #     "NVDA",
# #     "PEP",
# #     "ADBE",
# #     "AMGN",
# #     "COST",
# #     "FB",
# #     "GOOG",
# #     "GOOGL",
# #     'JNJ',
# #     'TSLA',
# #     'INTC',
# #     'UNH',
# #     'QCOM',
# #     'GILD',
# #     'NFLX',
# #     'CMCSA',
# #     'ORCL',
# #     'ATVI',
# #     'BABA',
# #     'NVS',
# #     'JD',
# #     'UN',
# #     'AZN',
# #     'GSK',
# #     'BP',
# #     'NTES',
# #     'BIDU',
# # ]
# assets = [
#     "AAPL",
#     "MSFT",
#     'AMZN',
#     'GOOGL',
#     'FB',
#     'V',
#     'JNJ',
#     "NVDA",
#     'NFLX',
#     'ADBE',
#     'INTC',
#     'TSLA',
#     'JD',
#     'DIS',
#     'BA',
#     'XOM',
#     'QCOM',
#     'QQQ'
# ]
# coins = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'ADA-USD', 'EOS-USD']
#
#
# #
# #
# # import itertools
# # from scipy.optimize import minimize
# #
# # pd.options.mode.chained_assignment = None
# # pd.set_option('display.max_columns', 10)
# # np.set_printoptions(suppress=True)
# #
# #
# # def cross_diff(w):
# #     num_assets = len(w)
# #     range_assets = np.arange(num_assets)
# #     comb_assets = np.asarray(list(itertools.combinations(range_assets, 2))).flatten()
# #     comb_assets = comb_assets.reshape([int(len(comb_assets) / 2), 2])
# #     s = np.asarray(w)[comb_assets]
# #     s = s[:, 0] - s[:, 1]
# #     s = np.power(s, 2)
# #     s = np.sum(s)
# #     return s
# #
# #
# # def corr(port, weights, cov_type='dist'):
# #     port['Port'] = np.dot(port.iloc[:, 0:].values, np.asarray(weights).reshape(-1, 1))
# #     if cov_type == 'pearson':
# #         cov_ = np.corrcoef(port.iloc[:, 0:].values, rowvar=False)[-1, :-1]
# #     elif cov_type == 'dist':
# #         dist_corr = get_dependence_matrix(port, dependence_method='distance_correlation').to_numpy()
# #         cov_ = dist_corr[-1, :-1]
# #     elif cov_type == 'determ':
# #         determ = covar(ret_df, returns_data_=True, cov_method='min_cov_determinant', delta_=0.35)
# #         min_cov_det = cov_to_corr(determ).to_numpy()
# #         cov_ = min_cov_det[-1, :-1]
# #     return cov_
# # #
# # #
# # # def calc_parity(port, weights, corr_):
# # #     port['Port'] = np.dot(port.iloc[:, 0:].values, np.asarray(weights).reshape(-1, 1))
# # #     sd_array = np.std(port.iloc[:, 0:].values, axis=0)
# # #     corr_array = corr_
# # #     mctr = np.multiply(np.multiply(weights, sd_array[:-1]), corr_array)
# # #     port.drop(columns=['Port'], inplace=True)
# # #     check = np.sum(mctr) # TODO НАХУЯ?
# # #     cross_diff_mctr = cross_diff(mctr)
# # #     std_mctr = np.sqrt(cross_diff_mctr)
# # #     params = dict()
# # #     params['sd_array'] = sd_array
# # #     params['corr_array'] = corr_array
# # #     params['mctr'] = mctr
# # #     params['std_mctr'] = std_mctr
# # #     params['check'] = check
# # #     return params
# # #
# # #
# # # def algo_optimization(port, init_weights, corr_):
# # #     # objective function
# # #     def f(opt_w):
# # #         # calculate target financial metric of this performance
# # #         params = calc_parity(port, opt_w, corr_)
# # #         # return target metric with negative sign to maximize it
# # #         # (opposite minimization)
# # #         return params['std_mctr']
# # #
# # #     # constrains
# # #     def constraint(x):
# # #         # the sum of all weights of opened (more the 0) positions should equal 1
# # #         # also add '-1' to execute maximization
# # #         return (1 - sum(x))
# # #
# # #     # add constrains to dictionary
# # #     con = ({'type': 'eq', 'fun': constraint})
# # #
# # #     # execute SLSQP optimization process
# # #     opt_w = np.asarray(init_weigths)
# # #     f(opt_w)
# # #     res = minimize(f, opt_w, constraints=con)
# # #
# # #     # after completing optimization minimize function returns dictionary with
# # #     # various information. We need:
# # #     # the value of objection function (multiply by -1 one if it was maximisation)
# # #     opt_param_value = 1 * res['fun']
# # #     # number or iterations was needed to complete optimization
# # #     opt_iter = res['nit']
# # #     # the array of optimized weights which give maximal sharpe
# # #     opt_weights = np.round(res['x'], 4)
# # #
# # #     # put this variables into dictionary:
# # #     opt_dict = ({'opt_param_value': opt_param_value,
# # #                  'opt_iter': opt_iter,
# # #                  'opt_weights': opt_weights})
# # #
# # #     return opt_dict
# #
# # path = os.path.join(YAHOO_PATH)
# # filename = 'coins.csv'
# #
# # asset_download(coins, start, end, path_=path, filename=filename, session_=session)
# #
# # _mom = momentum(path_=path, filename=filename)
# # ret_df = returns(file_path=path, filename=filename)
# #
# # # num_assets = ret_df.shape[1]
# # # init_weigths = np.ones(num_assets) / num_assets
# # #
# # # corr_ = corr(ret_df, init_weigths, cov_type='determ')
# # # result = algo_optimization(ret_df, init_weigths, corr_)
# # # print('opt_weights \n', result['opt_weights'])
# # # print('opt_param_value \n', result['opt_param_value'])
# # # print('@@@@ \n', calc_parity(ret_df, result['opt_weights']))
# #
# #
# # # Read in data.
# # stock_prices = pd.read_csv('port1_rp_port.csv', index_col='Date', parse_dates=True)
# # qqq_prices = pd.read_csv('qqq_rp_port.csv', index_col='Date', parse_dates=True)
# # giant_prices = pd.read_csv('all_rp_port.csv', index_col='Date', parse_dates=True)
# # coins_prices = pd.read_csv('all_coins.csv', index_col='Date', parse_dates=True)
# #
# # giant_pch = giant_prices.pct_change()
# # giant_pch.dropna(inplace=True)
# #
# # coins_pch = coins_prices.pct_change()
# # coins_pch.dropna(inplace=True)
# #
# # # Compute Buy and Hold with uniform weights as no weights are given.
# # port = BAH()
# # qqq = BAH()
# #
# # gp = EG(update_rule='GP', eta=2)
# # gp2 = EG(update_rule='GP', eta=1)
# # gp3 = EG(update_rule='GP', eta=1)
# #
# # # update_rule – (str) ‘MU’: Multiplicative Update, ‘GP’: Gradient Projection, ‘EM’: Expectation Maximization.
# # # eta – (float) Learning rate with range of [0, inf).
# # # Low rate indicates the passiveness of following the momentum and
# # # high rate indicates the aggressivness of following the momentum.
# #
# # ftrl = FTRL(beta=0.5)
# # # beta – (float) Constant to the regularization term.
# # # Typical ranges for interesting results include [0, 0.2], 1, and any high values.
# # # Low beta FTRL strategies are identical to FTL, and high beta indicates more regularization to return a uniform CRP.
# # # Depending on the dataset either 0.05 or 20 usually have the highest returns.
# #
# #
# # port.allocate(asset_prices=coins_prices, resample_by='D', weights=None, verbose=True)
# # # qqq.allocate(asset_prices=qqq_prices, resample_by='W', weights=None, verbose=True)
# #
# #
# # gp.allocate(asset_prices=coins_prices, resample_by='W', weights=None, verbose=True)
# # gp2.allocate(asset_prices=coins_prices, resample_by='W', weights=None, verbose=True)
# # gp3.allocate(asset_prices=coins_prices, resample_by='D', weights=None, verbose=True)
# #
# # ftrl.allocate(asset_prices=coins_prices, resample_by='W', weights=None, verbose=True)
# #
# # print('gp2.all_weights \n', gp2.all_weights)
# #
# # print('gp2.portfolio_return \n', gp2.portfolio_return)
# #
# #
# # plt.plot(port.portfolio_return, label='BUH')
# # # plt.plot(qqq.portfolio_return, label='QQQ')
# # # plt.plot(gp.portfolio_return, label='gp')
# # plt.plot(gp2.portfolio_return, label='gp2')
# # plt.plot(gp3.portfolio_return, label='gp3')
# # # plt.plot((ftrl.portfolio_return + gp2.portfolio_return)/2, label='Blend')
# # # plt.plot(ftrl.portfolio_return, label='ftrl')
# #
# # plt.legend()
# # plt.show()
# # plt.figure(figsize=(17, 7))
# # plt.show()
# #
# #
# # def get_coins_portfolio():
# #     closes = os.path.join(COINS_DATA, 'all_coins.csv')
# #     coins_prices = pd.read_csv(closes, index_col='date', parse_dates=True)
# #     coins_prices = coins_prices.iloc[20:]
# #
# #     btc = coins_prices.copy()
# #     btc.drop(columns=['TUSD', 'ADA', 'EOS'], inplace=True)
# #     alt = coins_prices.copy()
# #     alt.drop(columns=['ADA', 'EOS'], inplace=True)
# #
# #     # beta – (float) Constant to the regularization term.
# #     # Typical ranges for interesting results include [0, 0.2], 1, and any high values.
# #     # Low beta FTRL strategies are identical to FTL, and high beta indicates more regularization to return a uniform CRP.
# #     # Depending on the dataset either 0.05 or 20 usually have the highest returns.
# #     ftrl_port = FTRL(beta=2)
# #     alt_port = FTRL(beta=2)
# #     pamr1 = PAMR(optimization_method=1, epsilon=0.4, agg=20)
# #     pamr0 = PAMR(optimization_method=1, epsilon=0.4, agg=20)
# #     olmar1 = OLMAR(reversion_method=1, epsilon=10, window=20)
# #     # rmr = RMR(epsilon=10, n_iteration=100, window=20)
# #
# #     # Compute Buy and Hold with uniform weights as no weights are given.
# #     # bah_port = BAH()
# #     btc_port = BAH()
# #
# #     # bah_port.allocate(asset_prices=coins_prices, resample_by='D', weights=None, verbose=True)
# #     btc_port.allocate(asset_prices=btc, resample_by='D', weights=None, verbose=True)
# #     # ftrl_port.allocate(asset_prices=coins_prices, resample_by='D', weights=None, verbose=True)
# #     # alt_port.allocate(asset_prices=alt, resample_by='D', weights=None, verbose=True)
# #     # pamr1.allocate(asset_prices=coins_prices, resample_by='D', verbose=True)
# #     pamr0.allocate(asset_prices=alt, resample_by='D', verbose=True)
# #     olmar1.allocate(asset_prices=alt, resample_by='D', verbose=True)
# #     # rmr.allocate(asset_prices=alt, resample_by='D', verbose=True)
# #
# #
# #     # plt.plot((bah_port.portfolio_return - 1)*100, label='Buy and Hold')
# #     plt.plot((btc_port.portfolio_return - 1)*100, label='BTCUSD')
# #     # plt.plot((alt_port.portfolio_return - 1)*100, label='alt')
# #
# #     s1 = (olmar1.portfolio_return - 1)*100
# #     s2 = (pamr0.portfolio_return - 1)*100
# #     # s3 = (rmr.portfolio_return - 1)*100
# #
# #     # plt.plot((pamr0.portfolio_return - 1)*100, label='pamr0')
# #     # plt.plot((olmar1.portfolio_return - 1)*100, label='olmar1')
# #     # plt.plot((rmr.portfolio_return - 1)*100, label='rmr')
# #
# #     plt.plot(0.5*s1+0.5*s2, label='Mix3')
# #     print('olmar1_all_weights \n', olmar1.all_weights)
# #     print('pamr0_all_weights \n', pamr0.all_weights)
# #
# #     print('olmar1_portfolio_return \n', olmar1.portfolio_return)
# #     print('pamr0_portfolio_return \n', pamr0.portfolio_return)
# # #
# # #     import quantstats as qs
# # #     qs.reports.html(rets['port'], benchmark=rets['QQQ'], output=os.path.join(file_path, 'Test1.html'))
# # #
# # #
# # #
# # #
# # #
# # #     plt.legend()
# # #     plt.figure(figsize=(17, 7))
# # #     plt.show()
# # #
# # #
# # #
# # #
# # #
# # # def metrics(df_ticker_closes=None):
# # #     qs.extend_pandas()
# # #     closes = df_ticker_closes
# # #     closes.dropna(inplace=True)
# # #     print('Portfolio CAGR', qs.stats.cagr(closes))
# # #     print('Portfolio Ann.Volatility', qs.stats.volatility(closes))
# # #     print('Portfolio Drawdown', qs.stats.max_drawdown(closes))
# # #     print('Portfolio Sharpe', qs.stats.sharpe(closes))
# # #     print('Portfolio Sortino', qs.stats.sortino(closes))
# # #     print('Portfolio Expected Shortfall', qs.stats.expected_shortfall(closes))
# # #
# # #
# # #
# # #
# # #
# # rets['port'] = 0.1*rets['QLD'] + 0.09*rets['AAPL'] + 0.09*rets['AMZN'] + 0.09*rets['MSFT'] + 0.09*rets['NVDA'] + 0.09*rets['PEP']\
# #        + 0.09*rets['ADBE'] + 0.09*rets['AMGN'] + 0.09*rets['COST'] + 0.09*rets['FB'] + 0.09*rets['GOOG']
# # qs.reports.html(rets['port'], benchmark=rets['QQQ'], output=os.path.join(file_path, 'Test1.html'))
# #
# # file = '/home/gene/projects/nauvoo/all-weather-risk-parity/data/RP6_shrunk_cov-returns.csv'
# # # df = pd.read_csv(file, index_col='date', parse_dates=True)
# # title = 'RP6_black'
# # df = pd.read_csv(file)
# # portfolio = df.copy()
# # to_drop = portfolio[portfolio['key'] == 'benchmark'].index
# # portfolio.drop(to_drop, inplace=True)
# # portfolio['Return'] = (1 + portfolio['returns']) ** (1/portfolio['returns'].shift(1))-1
# # cols = [0, 2, 3]
# # portfolio.drop(portfolio.columns[cols], axis=1, inplace=True)
# # portfolio.dropna(inplace=True)
# # portfolio.to_csv(os.path.join(file_path, 'port_returns1.csv'), index=False)
# # stat = pd.read_csv(os.path.join(file_path, 'port_returns1.csv'), index_col='date', parse_dates=True)
# #
# # qs.reports.html(stat['Return'], benchmark=rets['QQQ'], title=f'{title}', output=os.path.join(file_path, f'{title}.html'))
