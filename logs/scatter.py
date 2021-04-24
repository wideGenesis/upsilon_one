import pandas as pd
import seaborn as sns

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

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


    # Generate fake data
    x = np.random.normal(size=1000)
    y = x * 3 + np.random.normal(size=1000)

    # Calculate the point density
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=100)
    plt.show()

scatter()

