import os
import quantstats as qs
import pdfkit

stock = 'FB'
bench = 'QQQ'
stock_closes = qs.utils.download_returns(f'{stock}')
bench_closes = qs.utils.download_returns(f'{bench}')
qs.reports.html(returns=stock_closes, benchmark=bench_closes, output=f'{stock}.html',
                title='Upsilon Parking Strategy')

pdfkit_options = {
            'margin-top': '0.1',
            'margin-right': '0.1',
            'margin-bottom': '0.1',
            'margin-left': '0.1',
            'encoding': 'UTF-8',
            'page-size': 'a4',
            'page-height': '10in',
            'page-width': '7.12in',
            # 'no-outline': None,
            'dpi': 96,
            'disable-smart-shrinking': '',
            'title': 'Parking Portfolio',
}


pdfkit.from_file(f'/home/gene/projects/upsilon_one/quantstats/FB.html',
                 f'/home/gene/projects/upsilon_one/quantstats/FB.pdf', options=pdfkit_options)