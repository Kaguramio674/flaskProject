import json
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc
from dash import html
from my_app.dash_app.create_charts import Chart
from my_app.dash_app.process_data import CrimeData

# external_stylesheets = [dbc.themes.BOOTSTRAP]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
pd.options.mode.chained_assignment = None

with open("data/london.geojson") as f:
    london_geo = json.load(f)
crime_data = pd.read_csv('data/cleaned_dataset.csv')
Borough_data = pd.read_csv('data/Borough_dataset.csv')

data = CrimeData()
area = 'Barking and Dagenham'
time = 25
major_select = 'Total'
minor_select = 'Total'
data.process_data_for_area(major_select, area, time)

chart_data = Chart(data)
fig_line = chart_data.create_line_chart(area, major_select, minor_select)
fig_bar = chart_data.create_bar_chart(major_select, minor_select, time)
fig_sun = chart_data.create_sun_chart(area, major_select, time)
fig_map = chart_data.create_map(time)
options = chart_data.select_change(major_select)
TIME_LIST = ['2019/10', '2019/11', '2019/12', '2020/01', '2020/02', '2020/03', '2020/04', '2020/05', '2020/06',
             '2020/07', '2020/08', '2020/09', '2020/10', '2020/11', '2020/12', '2021/01', '2021/02', '2021/03',
             '2021/04', '2021/05', '2021/06', '2021/07', '2021/08', '2021/09']
month_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
month_dict = {}
for i in range(len(month_list)):
    month_dict[i + 1] = month_list[i]

layout = html.Div(children=[
    html.Br(),
    html.Div(
        dbc.Container([
            html.H1(children="Business Crime", className="display-3", style={"text-align": "center"}),
            html.Hr(className="my-2"),
            html.Div(
                children='Business Crime data in London: From Oct. 2019 to Sept.2021.',
                style={"text-align": "center"}
            ),
        ],
            style={'background-color': '#66b2ff'},
            className="h-100 p-12 text-dark rounded-3",
        )),
    dbc.Row([
        dbc.Col(width=4, children=[
            html.H4("Select Area"),
            dcc.Dropdown(id="area-select",
                         options=[{"label": x, "value": x} for x in data.area_list[:len(data.area_list) - 1]],
                         value='Barking and Dagenham'
                         ),
            html.Br(),
            dbc.Row([
                dbc.Col(width=6, children=[
                    html.H5("Select Major Class"),
                    dcc.Dropdown(id="major-class-select",
                                 options=[{"label": x, "value": x} for x in
                                          data.major_class_list[:len(data.major_class_list)]],
                                 value='Total')
                ]),
                dbc.Col(width=6, children=[
                    html.H5("Select Minor Class"),
                    html.Div(dcc.Dropdown(id="minor-class-select", value=None))
                ])
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(width=1, children=[
                    html.H5("Year:"),
                ]),
                dbc.Col(width=11, children=[
                    dcc.Slider(
                        id='year-line',
                        min=1,
                        max=4,
                        step=None,
                        marks={1: '2019', 2: '2020', 3: '2021', 4: 'Total'},
                        value=4,
                    ),
                ])]),
            dbc.Row([
                dbc.Col(width=1, children=[
                    html.H5("Month:"),
                ]),
                dbc.Col(width=11, children=[
                    dcc.Slider(
                        id='month-line',
                        min=1,
                        max=12,
                        step=None,
                        marks=month_dict,
                        value=len(month_list),
                    ),
                ])]),

            html.Br(),
            html.Div(id="stats-card")
        ]),

        dbc.Col(width=8, children=[
            dcc.Graph(id='line-chart', figure=fig_line),
            dcc.Graph(id='bar-chart', figure=fig_bar)
        ]),
    ]),
    dbc.Row([
        dbc.Col(width=4, children=[
            dcc.Graph(
                id='sun-chart',
                figure=fig_sun,
                style={'height': '50vh'}
            ),
        ]),
        dbc.Col(width=8, children=[
            dcc.Graph(
                id='map',
                figure=fig_map,
                style={'height': '50vh'}
            ),
        ]),
    ]),
    dbc.Row([
        dbc.Col(width=6, children=[]),
        dbc.Col(width=6, children=[
        ]),
    ])

])

