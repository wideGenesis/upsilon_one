import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#
# def momentum(df_=None, p1=21, p2=63):
#     window = df_.shape[0]
#     columns = df_.columns.tolist()
#     mom_df = df_.copy()
#     for col in columns:
#         rets = df_[col].pct_change()
#         rets = rets[~np.isnan(rets)]
#         # lwma Weighting
#         weights_1 = np.arange(1, p1 + 1)
#         weights_2 = np.arange(1, p2 + 1)
#         mom_1 = rets.rolling(p1).apply(lambda x: np.dot(x, weights_1) / weights_1.sum())
#         mom_2 = rets.rolling(p2).apply(lambda x: np.dot(x, weights_2) / weights_2.sum())
#         # Z-Score
#         zs_1 = (mom_1 - mom_1.rolling(window-p2).mean()) / mom_1.rolling(window-p2).std()
#         zs_2 = (mom_2 - mom_2.rolling(window-p2).mean()) / mom_2.rolling(window-p2).std()
#         mom_df[col] = 0.5 * zs_1 + 0.5 * zs_2
#     mom_df.dropna(inplace=True)
#     mom_df.drop_duplicates(inplace=True)
#     print(mom_df.tail(10))
#     plt.figure(figsize=(20, 12))
#     fig, axs = plt.subplots(2, figsize=(10, 6))
#     axs[0].plot(mom_df['QQQ'])
#     axs[1].plot(mom_df['TLT'])
#     plt.show()
#
#
# df = pd.read_csv('https://raw.githubusercontent.com/wideGenesis/files/main/dataf.csv', parse_dates=True, index_col='Unnamed: 0')
#
# momentum(df_=df)
# # bench['Ranked_mom'] = symm1.rank()
# bench['Ranked_mom_perc'] = symm1.rank(pct=True)
# bench['Ranked_std_perc'] = Std.rank(pct=True, ascending=False)
# bench['RS/STD_RANK'] = 0.5*bench['Ranked_mom_perc'] + 0.5*bench['Ranked_std_perc']
# bench.dropna(inplace=True)




























