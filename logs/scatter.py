import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def scatter():
    df = pd.read_csv('/home/gene/projects/upsilon_one/results/inspector/data.csv')
    sns.set(rc={'figure.facecolor': 'black', 'figure.edgecolor': 'black', 'xtick.color': 'white', 'ytick.color': 'white',
                'text.color': 'white', 'axes.labelcolor': 'white',
                'axes.facecolor': 'black', 'grid.color': '#17171a'})
    sns.set_context('paper', font_scale=1.1)
    # sns.set_context('talk', font_scale=1.1)
    sns.despine()
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=df.iloc[2], y=df.iloc[0], size=df.iloc[1],
                    alpha=0.75, legend=True, sizes=(20, 500), hue=df.iloc[1], markers=True, palette="Spectral")
    names = df.columns.tolist()

    for line in range(0, df.shape[1]):
        plt.text(df.iloc[2][line] + 0.1, df.iloc[0][line] + 0.1, names[line],
                 horizontalalignment='left', size='x-small', color='white', weight='semibold')

    plt.text(12, -2.7, 'Premium',
             horizontalalignment='left', size='small', color='white', weight='bold')
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    plt.xlabel("Average Monthly Risk (%)")
    plt.ylabel("Average Excess Return over Risk (%)")
    # plt.tight_layout()
    plt.suptitle('Risk-Premium Analysis', fontsize=25)
    plt.legend(loc='lower right')
    plt.savefig('/home/gene/projects/upsilon_one/results/inspector/data.png',
                facecolor='black', transparent=True, bbox_inches='tight')
    plt.show()

scatter()

# df = pd.DataFrame({
# 'x': [1, 1.1, 1.2, 2, 5],
# 'y': [5, 15, 7, 10, 2],
# 's': [10000,20000,30000,40000,50000],
# 'group': ['Stamford','Yale','Harvard','MIT','Cambridge']
# })
# print(df)