# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

# portfolio_args['port_id'] = 'test_stacks_only'
# portfolio_args['is_aliased'] = False
# portfolio_args['etf_only'] = False
# portfolio_args['stacks_only'] = True
# portfolio_args['cor_perc'] = 0.99
# portfolio_args['sat_perc'] = 0.01
# # ********************* TEST STOCKS ONLY *********************
# portfolio_args['sat_alloctor_start_date'] = alloctor_start_date
# portfolio_args['sat_allocator_end_date'] = allocator_end_date
# portfolio_args['sat_selector_start_date'] = selector_start_date
# portfolio_args['sat_selector_end_date'] = selector_end_date
# portfolio_args['sat_etf_list'] = None
# # portfolio_args['sat_cap_filter'] = 20000000000
# portfolio_args['sat_cap_filter'] = '35%'
# portfolio_args['sat_assets_to_hold'] = 10
# portfolio_args['sat_cov_method'] = 'mcd'
# portfolio_args['sat_herc'] = False
# portfolio_args['sat_linkage_'] = 'ward'
# portfolio_args['sat_risk_measure_'] = 'standard_deviation'
# portfolio_args['sat_graphs_show'] = False
# portfolio_args['sat_selector_type'] = 21
# portfolio_args['sat_selector_adjustment'] = False
# portfolio_args['sat_selector_p1'] = 21
# portfolio_args['sat_selector_p2'] = 63
# portfolio_args['sat_selector_c_p1'] = 1
# portfolio_args['sat_selector_c_p2'] = 6
#
# portfolio_args['sat_cap_weight'] = 0.8
# compare_ticker = "QQQ"

app.layout = html.Div([
    html.Label('Dropdown'),

    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF'],
        multi=True
    ),

    html.Label('Radio Items'),
    dcc.RadioItems(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    # html.Label('Checkboxes'),
    # dcc.Checklist(
    #     options=[
    #         {'label': 'New York City', 'value': 'NYC'},
    #         {'label': u'Montréal', 'value': 'MTL'},
    #         {'label': 'San Francisco', 'value': 'SF'}
    #     ],
    #     values=['MTL', 'SF']
    # ),

    html.Label('Text Input'),
    dcc.Input(value='MTL', type='text'),

    html.Label('Rate'),
    dcc.Input(id='rate', value=0, type='number', min=0, max=1, step=0.1),

    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),
], style={'columnCount': 2})

if __name__ == '__main__':
    app.run_server(debug=True)