import pandas as pd
import quantstats as qs
import pdfkit


def quantstats_pdf(closes_df=None, bench_df=None, filename=None, title=None):
    df = pd.read_csv(closes_df, index_col='Date', parse_dates=True)
    df = df['Aggressive']
    bench_df = pd.read_csv(bench_df, index_col='Date', parse_dates=True)
    # stock_closes = qs.utils.download_returns('AMZN')
    print(df.describe())
    # print(stock_closes.head())
    qs.reports.html(returns=df, benchmark=bench_df, output=f'{filename}.html', title=title)
    pdfkit_options = {
                'margin-top': '0.1',
                'margin-right': '0.1',
                'margin-bottom': '0.1',
                'margin-left': '0.1',
                'encoding': 'UTF-8',
                'page-size': 'a4',
                'page-height': '10in',
                'page-width': '7.12in',
                'dpi': 96,
                'title': 'Parking Portfolio',
    }

    pdfkit.from_file(f'{filename}.html', f'{filename}.pdf', options=pdfkit_options)
    print('Stat pdf has been converted')


quantstats_pdf(closes_df='aggressive.csv', bench_df='QQQ_AGGRESSIVE.csv', filename='aggressive', title='Aggressive')