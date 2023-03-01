from dash import dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
from vega_datasets import data

# data = pd.read_csv('data/CA_youtube_trending_data_processed.csv')

# Read in global data
cars = data.cars()

# Setup app and layout/frontend
app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.DARKLY])
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    html.Div(
        id='mean-x-div'),
    dcc.Dropdown(
        id='xcol-widget',
        value='Horsepower',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in cars.columns]),
    dcc.Dropdown(
        id='ycol-widget',
        value='Displacement',
        options=[{'label': col, 'value': col} for col in cars.columns])])

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Output('mean-x-div', 'children'),  # This is the ID of our new output Div
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(cars).mark_point().encode(
        x=xcol,
        y=ycol,
        tooltip='Horsepower').interactive()
    return chart.to_html(), f'The mean of {xcol} is {cars[xcol].mean().round(1)}'

if __name__ == '__main__':
    app.run_server(debug=True)
 