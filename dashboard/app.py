import dash
from dashboard import layouts

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

external_stylesheets = ['https://codepen.io/chriddyp/penbWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.title = "Robert's Stock Dashboard"
app.layout = layouts.init(app)


