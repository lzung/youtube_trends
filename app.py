from dash import dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import pandas as pd
import altair as alt
import plotly.express as px

# Read in data globally
data = pd.read_csv('data/CA_youtube_trending_data_processed.csv', parse_dates=True)

# Setup app and layout/frontend
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Assistant:wght@300&display=swap",
        dbc.icons.FONT_AWESOME,
        dbc.themes.JOURNAL,
    ],
    compress=True,
)

header = html.Div(
    id="app-header",
    children=[
        html.I(DashIconify(icon="mdi:youtube"), style={"color" : "#D80808", "font-size" : "2.6em"}),
        html.H1("YouTube Trend Visualizer", style={"display" : "inline", "font-size" : "2em", "margin-left" : "2px"})
    ],
    style={"align" : "center", "margin-left" : 15}
)

date_picker = dcc.DatePickerRange(
    id="calendar",
    min_date_allowed=min(data['trending_date']),
    max_date_allowed=max(data['trending_date']),
    start_date_placeholder_text="Start Date",
    end_date_placeholder_text="End Date",
    clearable=True
)

video_badge = dbc.Button(
    [
        "Total Video Count: ",
        dbc.Badge(color="light", text_color="primary", id='video_count')
    ],
    disabled=True
)

channel_badge = dbc.Button(
    [
        "Total Channel Count: ",
        dbc.Badge(color="light", text_color="primary", id='channel_count')
    ],
    disabled=True
)


navbar = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                html.H5("Trending Date Range:"),
                date_picker
            ]),
            dbc.Col([
                dbc.Row(video_badge),
                dbc.Row(channel_badge, style={"margin-top" : "2px"})
            ])
        ])
    ]
)


app.layout = html.Div(
    [
        header,
        html.Hr(),
        navbar
    ],
    style = {"margin" : "0"}
)

def date_filter(df, start_date, end_date):
    if start_date is None:
        start_date = min(data['trending_date'])
    if end_date is None:
        end_date = min(data['trending_date'])
    
    return df[(df['trending_date'] > start_date) & (df['trending_date'] < end_date)]

# Set up callbacks/backend
@app.callback(
    Output('channel_count', 'children'),
    Output('video_count', 'children'),
    Input('calendar', 'start_date'),
    Input('calendar', 'end_date'))
def main_callback(start_date, end_date):
    # Filter for dates
    subset = date_filter(data, start_date, end_date)

    # Get number of videos
    vids = len(subset['video_id'].unique())

    # Get number of channels
    channels = len(subset['channelId'].unique())

    return vids, channels


if __name__ == '__main__':
    app.run_server(debug=True)

 