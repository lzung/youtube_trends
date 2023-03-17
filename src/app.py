from dash import dash, dash_table, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import pandas as pd
import altair as alt

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

# HEADER
header = html.Div(
    id="app-header",
    children=[
        html.I(DashIconify(icon="mdi:youtube"), style={"color" : "#D80808", "font-size" : "2.6em"}),
        html.H1("YouTube Trend Visualizer", style={"display" : "inline", "font-size" : "2em", "margin-left" : "2px"})
    ],
    style={"align" : "center", "margin-left" : 15}
)

# UNIVERSAL WIDGETS
date_picker = dcc.DatePickerRange(
    id="calendar",
    min_date_allowed=min(data['trending_date']),
    max_date_allowed=max(data['trending_date']),
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
    style={"background-color": "#D80808"}
    
)

channel_badge = dbc.Button(
    [
        "Total Channel Count: ",
        dbc.Badge(color="light", text_color="#D80808", id='channel_count')
    ],
    disabled=True,
    style={"background-color": "#D80808"}
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
    ]
)

# CHARTS
polarity = dbc.Card(
    [
        dbc.CardHeader(html.H4("Polarity of Tags by Category", className="card-title")),
        dbc.CardBody(
            dbc.Col([
                dcc.Loading(
                    id="loading-1",
                    type="circle",
                    children=html.Iframe(
                        id="polar_chart",
                        style={
                            "height": "25rem",
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
        "margin-left": "auto"
        }
)

trends = dbc.Card(
    [
        dbc.CardHeader(html.H4("Trending Videos over Time", className="card-title")),
        dbc.CardBody(
            dcc.Loading(
                id="loading-2",
                type="circle",
                children=html.Iframe(
                    id="trend_chart",
                    style={
                        "height": "25rem",
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
        "margin-right": "auto"
        }
)

table = dcc.Loading(
    id="loading-3",
    type="circle",
    children=dash_table.DataTable(
        id='table',
        page_size=10,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),
    color="#D80808"
)

app.layout = html.Div(
    [
        header,
        html.Hr(),
        tools,
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(polarity),
                dbc.Col(trends)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(table)
            ]
        )
    ],
    style = {"margin" : "0"}
)

def date_filter(df, start_date, end_date):
    if start_date is None:
        start_date = min(df['trending_date'])
    if end_date is None:
        end_date = max(df['trending_date'])

    return df[(df['trending_date'] >= start_date) & (df['trending_date'] <= end_date)]

def polarity_chart(df):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('mean(vader_sentiment):Q', title="Average Polarity Score"),
        y=alt.Y('categoryId', sort='x', title="Category"),
        color=alt.Color('mean(vader_sentiment):Q', scale=alt.Scale(scheme='redyellowgreen', domain=[-1, 1]), title="Sentiment")
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
    if (pd.to_datetime(max(df['trending_date'])) - pd.to_datetime(min(df['trending_date']))).days >= 30:
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('yearmonth(trending_date):O', title="Date"),
            y=alt.Y('count():Q', title="Number of Videos"),
            color=alt.Color('categoryId')
        ).properties(
            width='container'
        )
    elif (pd.to_datetime(max(df['trending_date'])) - pd.to_datetime(min(df['trending_date']))).days < 30:
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('trending_date:T', title="Date"),
            y=alt.Y('count():Q', title="Number of Videos"),
            color=alt.Color('categoryId', title='Category')
        ).properties(
            width='container'
        )
    else:
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('monthdate(trending_date):O', title="Date"),
            y=alt.Y('count():Q', title="Number of Videos"),
            color=alt.Color('categoryId')
        ).properties(
            width='container'
        )
    chart = chart.to_html().replace(
        "</head>",
        "<style>.vega-embed {width: 100%;}</style></head>",
    )
    return chart

def get_data_frame(df):
    # Get most recent entries
    filtered = df.sort_values(by=['trending_date'], ascending=False)
    filtered = filtered.groupby('videoId').first().reset_index()

    relevant_df = filtered[['title', 'channelTitle', 'categoryId', 'view_count', 'likes', 'dislikes', 'comment_count']]
    
    # Add rank by number of views
    relevant_df.insert(0, 'Rank', relevant_df['view_count'].rank(ascending=False))
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
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('calendar', 'start_date'),
    Input('calendar', 'end_date'),
    Input('category_filter', 'value')
)
def main_callback(start_date, end_date, category):
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

    # Get data table
    datatable, columns = get_data_frame(subset)

    return vids, channels, polar, trend, datatable, columns

if __name__ == '__main__':
    app.run_server(debug=True)
