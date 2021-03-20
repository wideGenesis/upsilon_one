from quotes.portfolios.sql_queries import get_portfolio_returns_df
from datetime import date
import pandas as pd
import quantstats as qs
import pdfkit
from datetime import date, timedelta


def quantstats_pdf(port_rets_df=None, bench=None, filename=None, title=None):
    df = qs.utils.download_returns(bench, period='max')
    # mom1 = ((df1[col].iloc[-1] - df1[col].iloc[0]) / df1[col].iloc[0])

    qs.reports.html(returns=port_rets_df, benchmark=df, output=f'{filename}.html', title=title)
    # pdfkit_options = {
    #             'margin-top': '0.1',
    #             'margin-right': '0.1',
    #             'margin-bottom': '0.1',
    #             'margin-left': '0.1',
    #             'encoding': 'UTF-8',
    #             'page-size': 'a4',
    #             'page-height': '10in',
    #             'page-width': '7.12in',
    #             'dpi': 96,
    #             'title': 'Parking Portfolio',
    # }
    #
    # pdfkit.from_file(f'{filename}.html', f'{filename}.pdf', options=pdfkit_options)
    print('Stat pdf has been converted')


def create_pdf():
    parking = get_portfolio_returns_df('parking', start_date=None, end_date=date.today())
    allweather = get_portfolio_returns_df('allweather', start_date=None, end_date=date.today())
    balanced = get_portfolio_returns_df('balanced', start_date=None, end_date=date.today())
    aggressive = get_portfolio_returns_df('aggressive', start_date=None, end_date=date.today())
    leveraged = get_portfolio_returns_df('leveraged', start_date=None, end_date=date.today())

    elastic = get_portfolio_returns_df('elastic', start_date=None, end_date=date.today())
    yolo = get_portfolio_returns_df('yolo', start_date=None, end_date=date.today())

    quantstats_pdf(port_rets_df=parking, bench='TLT', filename='parking', title='Parking Strategy')
    quantstats_pdf(port_rets_df=allweather, bench='SPY', filename='allweather', title='All Weather Strategy')
    quantstats_pdf(port_rets_df=balanced, bench='QQQ', filename='balanced', title='Balanced Strategy')
    quantstats_pdf(port_rets_df=aggressive, bench='QQQ', filename='aggressive', title='Aggressive Strategy')
    quantstats_pdf(port_rets_df=leveraged, bench='QQQ', filename='leveraged', title='Leveraged Strategy')

    quantstats_pdf(port_rets_df=elastic, bench='QQQ', filename='elastic', title='Elastic Strategy')
    quantstats_pdf(port_rets_df=yolo, bench='SPY', filename='yolo', title='Yolo Strategy')

    # elastic.to_csv('elastic.csv')
    # yolo.to_csv('yolo.csv')

# parking = get_portfolio_returns_df('parking', start_date=None, end_date=date.today())
# allweather = get_portfolio_returns_df('allweather', start_date=None, end_date=date.today())
# balanced = get_portfolio_returns_df('balanced', start_date=None, end_date=date.today())
# aggressive = get_portfolio_returns_df('aggressive', start_date=None, end_date=date.today())
# leveraged = get_portfolio_returns_df('leveraged', start_date=None, end_date=date.today())
# elastic = get_portfolio_returns_df('elastic', start_date=None, end_date=date.today())
# yolo = get_portfolio_returns_df('yolo', start_date=None, end_date=date.today())

# quantstats_pdf(port_rets_df=parking, bench='TLT', filename='parking', title='Parking Strategy')
# quantstats_pdf(port_rets_df=allweather, bench='SPY', filename='allweather', title='All Weather Strategy')
# quantstats_pdf(port_rets_df=balanced, bench='QQQ', filename='balanced', title='Balanced Strategy')
# quantstats_pdf(port_rets_df=allweather, bench='QQQ', filename='aggressive', title='Aggressive Strategy')
# quantstats_pdf(port_rets_df=balanced, bench='QQQ', filename='leveraged', title='Leveraged Strategy')
#
# quantstats_pdf(port_rets_df=elastic, bench='QQQ', filename='elastic', title='Elastic Strategy')
# quantstats_pdf(port_rets_df=yolo, bench='SPY', filename='yolo', title='Yolo Strategy')


# sac_parking = get_portfolio_returns_df('sac_parking', start_date=None, end_date=date.today())
# sac_balanced = get_portfolio_returns_df('sac_balanced', start_date=None, end_date=date.today())
# sac_growth = get_portfolio_returns_df('sac_growth', start_date=None, end_date=date.today())
#
# quantstats_pdf(port_rets_df=sac_parking, bench='TLT', filename='sac_parking', title='Parking Strategy')
# quantstats_pdf(port_rets_df=sac_balanced, bench='SPY', filename='sac_balanced', title='Balanced Strategy')
# quantstats_pdf(port_rets_df=sac_growth, bench='SPY', filename='sac_growth', title='Growth Strategy')

def html_pdf(filename=None, title=None):
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

html_pdf(filename='parking', title='Parking Strategy')
html_pdf(filename='allweather', title='All Weather Strategy')
html_pdf(filename='balanced', title='Balanced Strategy')
html_pdf(filename='aggressive', title='Aggressive Strategy')
html_pdf(filename='leveraged', title='Leveraged Strategy')

html_pdf(filename='elastic', title='Elastic Strategy')
html_pdf(filename='yolo', title='Yolo Strategy')