import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

bench = pd.read_csv('http://raw.githubusercontent.com/umachkaalex/data/master/QQQ.csv')

symm1 = (bench['Close'] - bench['Close'].shift(21))/bench['Close'].shift(21)
Std = bench['Close'].pct_change().rolling(21).std()
bench['std'] = Std

# bench['Ranked_mom'] = symm1.rank()
bench['Ranked_mom_perc'] = symm1.rank(pct=True)

# bench['Ranked_std'] = Std.rank()
bench['Ranked_std_perc'] = Std.rank(pct=True, ascending=False)
bench['level'] = 0.5
bench['RS/STD_RANK'] = 0.5*bench['Ranked_mom_perc'] + 0.5*bench['Ranked_std_perc']

bench.dropna(inplace=True)
bench.tail(5)

plt.figure(figsize=(20, 12))

fig, axs = plt.subplots(2, figsize=(10, 6))

# axs[0].plot(bench['Date'], bench['Close'])
# axs[1].plot(bench['Date'], bench['RS/STD_RANK'])
axs[0].plot(bench['Close'][4500:])
axs[1].plot(bench['RS/STD_RANK'][4500:])
axs[1].plot(bench['Ranked_mom_perc'][4500:])
axs[1].plot(bench['level'][4500:])
plt.show()