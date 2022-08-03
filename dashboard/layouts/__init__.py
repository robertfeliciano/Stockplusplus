from dash import Dash
from dash import dcc
from dash import html


def init(app: Dash):
    
    # Tab 0
    import dashboard.layouts.daily_info.callbacks as di_callbacks
    import dashboard.layouts.daily_info.layout as di_layout
    di_callbacks.register(app)
    tabs = [di_layout.build()]
    
    
    return html.Div(children=[
        html.H3("Welcome to Stock++",
                style = {
                    'textAlign': 'center',
                    'margin': '48px 0',
                    'fontFamily': 'system-ui'
                    }),
        dcc.Tabs(
            id = 'tabs',
            children = tabs,
            style = {
                'fontFamily': 'system-ui'
            },
            content_style = {
                'borderLeft': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'borderBottom': '1px solid #d6d6d6',
                'padding': '20px'
            },
            parent_style = {
                'maxWidth': '1000px',
                'margin': '0 auto'
            })
    ])