from dash import dash, dash_table, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import altair as alt
from datetime import date

alt.data_transformers.disable_max_rows()

# Read in data globally
data = pd.read_csv('../data/CA_youtube_nltk.csv', parse_dates=True, index_col=0)

# Setup app and layout/frontend
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Assistant:wght@300&display=swap",
        dbc.icons.FONT_AWESOME,
        dbc.themes.JOURNAL,
    ]
)

# Server
server = app.server

# Title
app.title = 'YouTube Trend Visualizer'

# HEADER
header = html.Div(
    id="app-header",
    children=[
        html.I(
            DashIconify(icon="mdi:youtube"),
            style={
                "color" : "#D80808",
                "font-size" : "2.6em"
            }
        ),
        html.H1(
            "YouTube Trend Visualizer",
            style={
                "display" : "inline",
                "font-size" : "2em",
                "margin-left" : "2px"
            }
        )
    ],
    style={"align" : "center", "margin-left" : 15}
)

# UNIVERSAL WIDGETS
date_picker = dcc.DatePickerRange(
    id="calendar",
    min_date_allowed=min(data['trending_date']),
    max_date_allowed=max(data['trending_date']),
    start_date=date(2020, 8, 11),
    end_date=date(2020, 8, 18),
    start_date_placeholder_text="Start Date",
    end_date_placeholder_text="End Date",
    clearable=True
)

cat_menu = dcc.Dropdown(
    id="category_filter",
    placeholder="Select categories",
    options=[
        {"label": i, "value": i} for i in sorted(data['categoryId'].unique())
    ],
    clearable=True,
    searchable=True,
    multi=True
)

video_badge = dbc.Button(
    [
        "Total Video Count: ",
        dbc.Badge(color="light", text_color="#D80808", id='video_count')
    ],
    disabled=True,
    style={"background-color": "#D80808", "opacity" : "100%"}
)

channel_badge = dbc.Button(
    [
        "Total Channel Count: ",
        dbc.Badge(color="light", text_color="#D80808", id='channel_count')
    ],
    disabled=True,
    style={"background-color": "#D80808", "opacity" : "100%"}
)

tools = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                html.H5("Trending Date Range:"),
                date_picker
            ],
            width=4),
            dbc.Col([
                html.H5("Categories:"),
                cat_menu
            ],
            width=3),
            dbc.Col([
                dbc.Row(video_badge),
                dbc.Row(channel_badge, style={"margin-top" : "2px"})
            ],
            width={"size": 3, "offset": 1})
        ],
        justify="center")
    ],
    style={
        "backgroundColor": "#F4F4F4",
        "padding": "20px 20px",
        "border-radius": "16px",
        "margin-bottom": "1rem",
        "border": "1px solid lightgray",
        "box-shadow": "0px 1px 4px 0px rgba(0, 0, 0, 0.1)"
    }
)

# TABLE FILTER
sort_table = dcc.Dropdown(
    id='table_filter',
    options=[
        {'label': 'Comments', 'value': 'comment_count'},
        {'label': 'Dislikes', 'value': 'dislikes'},
        {'label': 'Likes', 'value': 'likes'},
        {'label': 'Views', 'value': 'view_count'}
   ],
   value='view_count'
)

# DISCLAIMER
pop = dbc.Popover(
    "The most recent metrics (i.e. from the latest date that a video was trending) are displayed in this table.",
    body=True,
    target="table_filter",
    trigger="legacy"
)

# CHARTS / TABLE
polarity = dbc.Card(
    [
        dbc.CardHeader(
            html.H4("Polarity of Tags by Category", className="card-title", style={"color": "white"}),
            style={"background-color": "#D80808"}
        ),
        dbc.CardBody(
            dbc.Col([
                dcc.Loading(
                    id="loading-1",
                    type="circle",
                    children=html.Iframe(
                        id="polar_chart",
                        style={
                            "height": "22rem",
                            "width": "100%",
                            "border": "0",
                            "display": "flex",
                            "align-items": "center",
                            "justify-content": "center"
                            }
                        ),
                    color="#D80808"
                )
            ])
        )
    ],
    className="mb-3",
    style={
        "width": "90%",
        "margin-left": "auto",
        "border": "1px solid lightgray",
        "box-shadow": "0px 1px 4px 0px rgba(0, 0, 0, 0.1)"
    }
)

trends = dbc.Card(
    [
        dbc.CardHeader(
            html.H4("Trending Videos over Time", className="card-title", style={"color": "white"}),
            style={"background-color": "#D80808"}
        ),
        dbc.CardBody(
            dcc.Loading(
                id="loading-2",
                type="circle",
                children=html.Iframe(
                    id="trend_chart",
                    style={
                        "height": "22rem",
                        "width": "100%",
                        "border": "0",
                        "display": "block"
                        }
                    ),
                color="#D80808"
            )
        )
    ],
    className="mb-3",
    style={
        "width": "90%",
        "margin-right": "auto",
        "border": "1px solid lightgray",
        "box-shadow": "0px 1px 4px 0px rgba(0, 0, 0, 0.1)"
    }
)

table = dcc.Loading(
    id="loading-3",
    type="circle",
    children=dash_table.DataTable(
        id='table',
        page_size=10,
        filter_action="native",
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#FFD4D4',
        }
        ],
        style_header={
            'backgroundColor': '#D80808',
            'color': 'white',
            'fontWeight': 'bold',
            'fontSize': '25',
            'font-family': 'Assistant',
            'textAlign': 'center'
        },
        style_cell={
            'font-family': 'Assistant'
        },
        fill_width=False
    ),
    color="#D80808"
)

# LAYOUT
app.layout = html.Div(
    [
        header,
        html.Hr(),
        tools,
        dbc.Row(
            [
                dbc.Col(polarity),
                dbc.Col(trends)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Rank by:"),
                        sort_table,
                        pop
                    ],
                    width=2
                ),
                dbc.Col([
                    html.H4("Trending YouTube Video Metrics"),
                    table
                ], width=6)
            ],
            justify="center"
        ),
        html.Hr(),
        html.Footer(
            [
                'Created by Lauren Zung (Last Update: 2023-03-18)',
                dmc.Group(
                    [
                        dmc.Anchor(
                            dmc.ActionIcon(
                                DashIconify(icon="mdi:github", width=20),
                                size="lg",
                                variant="outline",
                                style={"color": "#D80808"}
                            ),
                            href="https://github.com/lzung/youtube_trends"
                        ),
                        dmc.Anchor(
                            dmc.ActionIcon(
                                DashIconify(icon="simple-icons:kaggle", width=20),
                                size="lg",
                                variant="outline",
                                style={"color": "#D80808"}
                            ),
                            href="https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset?datasetId=828106&sortBy=voteCount&select=CA_youtube_trending_data.csv"
                        ),
                        dmc.Anchor(
                            dmc.ActionIcon(
                                DashIconify(icon="mdi:linkedin", width=20),
                                size="lg",
                                variant="outline",
                                style={"color": "#D80808"}
                            ),
                            href="https://www.linkedin.com/in/lauren-zung/"
                        )
                    ],
                    style={'margin-top': 5}
                )
            ],
            style={'margin-bottom': '1rem', 'margin-left': 15}
        )
    ],
    style = {"margin" : "0"}
)

# HELPER FUNCTIONS
def date_filter(df, start_date, end_date):
    if start_date is None:
        start_date = min(df['trending_date'])
    if end_date is None:
        end_date = max(df['trending_date'])

    return df[(df['trending_date'] >= start_date) & (df['trending_date'] <= end_date)]

def polarity_chart(df):
    # Get most recent entries to avoid repeats
    filtered = df.sort_values(by=['trending_date'], ascending=False)
    filtered = filtered.groupby('video_id').first().reset_index()

    chart = alt.Chart(filtered).mark_bar().encode(
        x=alt.X('mean(vader_sentiment):Q', title="Average Polarity Score"),
        y=alt.Y('categoryId', sort='x', title="Category"),
        color=alt.Color('mean(vader_sentiment):Q', scale=alt.Scale(scheme='redyellowgreen', domain=[-1, 1]), title="Sentiment"),
        tooltip=[alt.Tooltip('count()', title='Number of Videos')]
    ).properties(
        width='container'
    )
    chart = chart.to_html().replace(
        "</head>",
        "<style>.vega-embed {width: 100%;}</style></head>",
    )
    return chart

def trend_chart(df):
    # Format x-axis depending on time frame
    if (pd.to_datetime(max(df['trending_date'])) - pd.to_datetime(min(df['trending_date']))).days < 75:
        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('trending_date:T', title="Date"),
            y=alt.Y('count():Q', title="Number of Videos"),
            color=alt.Color('categoryId', title='Category', scale=alt.Scale(scheme="category20")),
            tooltip=[
                alt.Tooltip('trending_date:T', title='Date'),
                alt.Tooltip('categoryId', title='Category'),
                alt.Tooltip('count():Q', title='Number of Videos')
            ]
        ).properties(
            width='container'
        )
    else:
        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('yearmonth(trending_date):O', title="Date"),
            y=alt.Y('count():Q', title="Number of Videos"),
            color=alt.Color('categoryId', title='Category'),
            tooltip=[
                alt.Tooltip('yearmonth(trending_date):O', title='Date'),
                alt.Tooltip('categoryId', title='Category'),
                alt.Tooltip('count():Q', title='Number of Videos')
            ]
        ).properties(
            width='container'
        )
    chart = chart.to_html().replace(
        "</head>",
        "<style>.vega-embed {width: 100%;}</style></head>",
    )
    return chart

def get_data_frame(df, filter):
    # Get most recent entries to avoid repeats
    filtered = df.sort_values(by=['trending_date'], ascending=False)
    filtered = filtered.groupby('video_id').first().reset_index()

    relevant_df = filtered[['title', 'channelTitle', 'categoryId', 'view_count', 'likes', 'dislikes', 'comment_count']]
    
    # Add rank by dropdown selection
    relevant_df.insert(0, 'Rank', relevant_df[filter].rank(method='min', ascending=False))
    relevant_df = relevant_df.sort_values(by=['Rank'])

    relevant_df.columns = ['Rank', 'Title', 'Channel Name', 'Category', 'Views', 'Likes', 'Dislikes', 'Comments']
    cols = [{"name": col, "id": col} for col in relevant_df.columns]
    dt = relevant_df.to_dict('records')

    return dt, cols

# Set up callbacks/backend
@app.callback(
    Output('video_count', 'children'),
    Output('channel_count', 'children'),
    Output('polar_chart', 'srcDoc'),
    Output('trend_chart', 'srcDoc'),
    Input('calendar', 'start_date'),
    Input('calendar', 'end_date'),
    Input('category_filter', 'value')
)
def chart_callback(start_date, end_date, category):
    # Filter for dates
    subset = date_filter(data, start_date, end_date)

    if category:
        subset = subset[subset['categoryId'].isin(category)]

    # Get number of videos
    vids = len(subset['video_id'].unique())

    # Get number of channels
    channels = len(subset['channelId'].unique())

    # Get polarity chart
    polar = polarity_chart(subset)

    # Get trend chart
    trend = trend_chart(subset)

    return vids, channels, polar, trend

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('calendar', 'start_date'),
    Input('calendar', 'end_date'),
    Input('category_filter', 'value'),
    Input('table_filter', 'value')
)
def table_callback(start_date, end_date, category, table_filter):
    # Filter for dates
    subset = date_filter(data, start_date, end_date)

    if category:
        subset = subset[subset['categoryId'].isin(category)]

    # Get data table
    datatable, columns = get_data_frame(subset, table_filter)

    return datatable, columns

if __name__ == '__main__':
    app.run_server(debug=True)
