from dash import html
import dash_bootstrap_components as dbc
from dash import Output, Input
from my_app.dash_app.create_charts import Chart
from my_app.dash_app.process_data import CrimeData

data = CrimeData()
TIME_LIST = ['2019/10', '2019/11', '2019/12', '2020/01', '2020/02', '2020/03', '2020/04', '2020/05', '2020/06',
             '2020/07', '2020/08', '2020/09', '2020/10', '2020/11', '2020/12', '2021/01', '2021/02', '2021/03',
             '2021/04', '2021/05', '2021/06', '2021/07', '2021/08', '2021/09']
chart_data = Chart(data)


def register_callbacks(dash_app):
    @dash_app.callback(Output("stats-card", "children"),
                       [Input("area-select", "value"), Input("year-line", "value"), Input("month-line", "value"),
                        Input("major-class-select", "value"), Input("minor-class-select", "value")])
    def render_output_panel(area_select, year, month, major, minor):
        time_index_select = time_calculation(year, month)
        data.process_data_for_area(major, area_select, time_index_select)
        if time_index_select == 25:
            time_select = ''
            time_last = ''
            month_text = "N/A"
            last_month_text = "N/A"
        else:
            if time_index_select == 1:
                time_last = ''
                last_month_text = "N/A"
            else:
                time_last = TIME_LIST[time_index_select - 2]
                last_month_text = "{:,.0f}%".format(data.compare_last_month)
            time_select = TIME_LIST[time_index_select - 1]
            month_text = "{:,.0f}%".format(data.compare_month_to_ave)
        if major is None or major == 'Total':
            major = 'Total'
            ratio_text = data.ratio_total
        else:
            ratio_text = "{:,.1f}%".format(data.ratio_total)
        if minor is None:
            minor = 'Total'
        card = dbc.Card(className="bg-dark text-light", children=[
            dbc.CardBody([
                html.H4(area_select, id="card-name", className="card-title"),
                html.Br()]),
            dbc.Row([
                dbc.Col(width=6, children=[
                    dbc.CardBody([
                        html.H6("Compare Total Crime Data in Borough to Average:", className="card-title"),
                        html.H4("{:,.0f}%".format(data.compare_to_ave), className=style_selection(data.compare_to_ave)),
                        html.Br()
                    ]),
                ]),
                dbc.Col(width=6, children=[
                    dbc.CardBody([
                        html.H6("Compared Selected Month (" + time_select + ') to Average:', className="card-title"),
                        html.H4(month_text, className=style_selection(data.compare_month_to_ave)),
                        html.Br()
                    ]),
                ]),
            ]),
            dbc.Row([
                dbc.Col(width=6, children=[
                ]),
                dbc.Col(width=6, children=[
                    dbc.CardBody([
                        html.H6("Compared to Last Month (" + time_last + '):', className="card-title"),
                        html.H4(last_month_text, className=style_selection(data.compare_last_month)),
                        html.Br()
                    ]),
                ]),
            ]),
            dbc.CardBody([
                html.H4(major + " - " + minor, id="card-name", className="card-title"),
                html.Br(),
                html.H6("Ratio of " + major + " Crime Number to Total", className="card-title"),
                html.H4(ratio_text, className="card-text text-info"),
                html.Br()]),

            dbc.CardLink("Project Github Link", href="https://github.com/ucl-comp0035/comp0034-cw1-i-Kaguramio674"),
        ])
        return card

    @dash_app.callback(Output("minor-class-select", "options"), [Input("major-class-select", "value")])
    def update_select(major):
        minor_list = chart_data.select_change(major)
        return [{"label": x, "value": x} for x in minor_list]

    @dash_app.callback(Output("line-chart", "figure"),
                       [Input("area-select", "value"), Input("major-class-select", "value"),
                        Input("minor-class-select", "value")])
    def update_line_chart(area_select, major, minor):
        fig_li = chart_data.create_line_chart(area_select, major, minor)
        return fig_li

    @dash_app.callback(Output("map", "figure"), [Input("year-line", "value"), Input("month-line", "value")])
    def update_map(year, month):
        time_select = time_calculation(year, month)
        figure = chart_data.create_map(time_select)
        return figure

    @dash_app.callback(Output("bar-chart", "figure"),
                       [Input("major-class-select", "value"), Input("minor-class-select", "value"),
                        Input("year-line", "value"),
                        Input("month-line", "value")])
    def update_bar_chart(major, minor, year, month):
        time_select = time_calculation(year, month)
        figure = chart_data.create_bar_chart(major, minor, time_select)
        return figure

    @dash_app.callback(Output("sun-chart", "figure"),
                       [Input("area-select", "value"), Input("major-class-select", "value"),
                        Input("year-line", "value"),
                        Input("month-line", "value")])
    def update_sun_chart(area_select, major, year, month):
        time_select = time_calculation(year, month)
        figure = chart_data.create_sun_chart(area_select, major, time_select)
        return figure

    def time_calculation(year, month):
        if year == 4:
            time_select = 25
        elif year == 1 and month < 10:
            time_select = 25
        elif year == 3 and month > 9:
            time_select = 25
        else:
            time_select = month + 12 * year - 21
        return time_select

    def style_selection(date):
        if date < 0:
            style = "card-text text-success"
        else:
            style = "card-text text-danger"
        return style
