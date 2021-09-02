from dash import Dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


from dashboard.api_requests import daily_info
from dashboard.json_parser import json_parser


def register(app: Dash):
    @app.callback(
        [Output('opening', 'children'),
         Output('closing', 'children')],
        [Input('ticker', 'value'),
         Input('date', 'date'),
         Input('submit-val', 'n_clicks')]
    )
    def find_price(ticker, date, n_clicks):
        if n_clicks == 0:
            raise PreventUpdate
        else:
            init_data = daily_info(ticker, date)
            prices = json_parser(init_data)
            
            opening = f'The opening price for {ticker} was {prices.get(ticker[0])[0]}'
            closing = f'The closing price for {ticker} was {prices.get(ticker[0])[1]}'
            
            n_clicks = 0
            return [opening, closing]