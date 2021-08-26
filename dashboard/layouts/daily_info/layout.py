import dash_core_components as dcc
import dash_html_components as html
from datetime import date

def build():
    return dcc.Tab(label='Daily Info', children=[
        html.H3("Input a stock ticker to find the price!"),
        html.Div([
            "Ticker: ",
            dcc.Input(id='ticker', type='text'),
            "API Key: ",
            dcc.Input(id='api_key', type='text')
            ]),
        html.Div([
            dcc.DatePickerSingle(
                id='date',
                min_date_allowed = date(1995, 8, 5),
                max_date_allowed = date(2024, 6, 1),
                initial_visible_month = date(2021, 8, 5),
                date = date(2021, 8, 20)
            ),
            html.Button('Enter', id='submit-val', n_clicks=0),
        ]),
        html.Div([
             html.P(id='opening'),
             html.P(id='closing')
        ])
    ])