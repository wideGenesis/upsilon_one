from quotes.portfolios.sql_queries import get_portfolio_returns_df
from datetime import date
import pandas as pd
import quantstats as qs
import pdfkit


def quantstats_pdf(port_rets_df=None, bench='QQQ', filename=None, title=None):
    df = qs.utils.download_returns(bench, period='10y')
    #
    # print(port_rets_df.index)
    # print(port_rets_df)
    # print(df.index)
    # print(df)


    # mom1 = ((df1[col].iloc[-1] - df1[col].iloc[0]) / df1[col].iloc[0])
    bench_df = qs.utils.download_returns(bench, period='10y')

    qs.reports.html(returns=port_rets_df, benchmark=bench_df, output=f'{filename}.html', title=title)
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

x = get_portfolio_returns_df('aggressive', start_date=None, end_date=date.today())

quantstats_pdf(port_rets_df=x, bench='QQQ', filename='aggressive', title='Aggressive')
# print(x)

# Date,Aggressive
# 1/31/08,-0.0636
# 2/29/08,-0.0091
# 3/31/08,0.0092