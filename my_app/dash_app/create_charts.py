import json

import plotly.graph_objects as go
import plotly.express as px


class Chart:

    def __init__(self, data):
        self.data = data

    def select_change(self, select):
        crime_data = self.data.crime_data
        minor_class_list = crime_data.loc[crime_data['Major Class Description'] == select]

        minor_list = minor_class_list["Minor Class Description"].unique().tolist()
        return minor_list

    def create_line_chart(self, area, major, minor):
        if major is None or major == 'Total':
            major = 'Total'
            minor = 'Total'
            area_data = self.data.crime_borough
            index = 1
        elif minor is None or minor == 'Total':
            minor = 'Total'
            area_temp_data = self.data.classified_data.loc[self.data.classified_data['Major Class Description'] == major]
            area_data = area_temp_data.loc[area_temp_data['Borough'] == area]
            index = 2
        else:
            area_temp_data = self.data.crime_data.loc[self.data.crime_data['Minor Class Description'] == minor]
            area_data = area_temp_data.loc[area_temp_data['Borough'] == area]
            index = 3
        average_data = self.data.average_data
        layout = go.Layout(showlegend=True, plot_bgcolor="#ffffff")
        figure = go.Figure(layout=layout)

        area_chart = go.Scatter(x=self.data.TIME_LIST, y=area_data.iloc[-1, index:-1],
                                mode='lines',
                                name=area + '<br>' + 'Major Class: ' + major + '<br>' + 'Minor Class: ' + minor,
                                line=dict(color='firebrick', width=4))
        average_chart = go.Scatter(x=self.data.TIME_LIST, y=average_data.iloc[-1, 1:-1], mode='lines',
                                   name='<br>Average Crime Number <br>in London <br>',
                                   line=dict(color='lightgrey', dash='dash'))

        dtick = round(max(average_data.iloc[-1, index:len(average_data.iloc[-1, index:])].max(),
                          area_data.iloc[-1, index:len(area_data.iloc[-1, index:])].max()) / 600) * 100
        figure.add_trace(average_chart)
        figure.add_trace(area_chart)
        figure.update_layout(yaxis_title="Number of Crime",
                             title={
                                 'text': 'London Crime Data in <span style="font-size: 17px;color:#ff471a;font-weight:bold;">' + area
                                         + '</span><br>Major Class:' + '<span style="color:#ff471a;font-weight:bold;">'
                                         + major + '</span>   Minor Class:' + '<span style="color:#ff471a;font-weight:bold;">' + minor + '</span>',
                                 'x': 0.5,
                                 'xanchor': 'center',
                                 'yanchor': 'top'
                                 })
        figure.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#CDCDCD',
                            tick0=0.0, dtick=dtick)
        figure.update_xaxes(tickangle=90, showline=True, linewidth=2, linecolor='#CDCDCD')
        return figure

    def create_map(self, time):
        if time == 25:
            color = 'Total'
        else:
            color = self.data.TIME_LIST[time - 1]

        borough_data = self.data.borough_data
        token = 'pk.eyJ1Ijoid3V5dWhlbmcwIiwiYSI6ImNremNtMDhnNzFlYXIzMG8xczJuOWlrYWcifQ.dAQLDBZjbtTWmnL1Q8nOog'
        try:
            with open("data/london.geojson") as f:
                london_geo = json.load(f)
        except FileNotFoundError:
            with open("my_app/data/london.geojson") as f:
                london_geo = json.load(f)
        figure = px.choropleth_mapbox(
            data_frame=borough_data,
            geojson=london_geo,
            locations='Borough',
            color=color,
            featureidkey='properties.name',
            color_continuous_scale='ylOrRd',
        )
        figure.update_layout(
            mapbox_accesstoken=token,
            mapbox_style="light",
            mapbox_zoom=9,
            mapbox_center={"lat": 51.5107, "lon": -0.111},
            margin=dict(t=0, l=0, r=0, b=0)
        )
        return figure

    def create_bar_chart(self, major, minor, time_select):
        if time_select == 25:
            time = 'Total'
        else:
            time = self.data.TIME_LIST[time_select - 1]
        if major is None or major == 'Total':
            major = 'Total'
            minor = 'Total'
            bar_data = self.data.borough_data[['Borough', time]]
            bar_data = bar_data[:-1]
        else:
            if minor is None or minor == 'Total':
                minor = 'Total'
                temp_data = self.data.classified_data[['Borough','Major Class Description', time]]
                bar_data = temp_data.loc[temp_data['Major Class Description'] == major]
            else:
                temp_data = self.data.crime_data[['Borough','Minor Class Description', time]]
                bar_data = temp_data.loc[temp_data['Minor Class Description'] == minor]
        figure = px.bar(bar_data, x=bar_data['Borough'], y=time)
        figure.update_layout(
            barmode='stack',
            xaxis={'categoryorder': 'total descending'},
            yaxis_title="Number of Crime",
            title={'text': 'Borough Crime Data in ' + '<span style="color:#ff471a;font-weight:bold;">' +
                           time + '</span>' + ' With' + '<br>' + 'Major Class:' +
                           '<span style="color:#ff471a;font-weight:bold;">' + major + '</span>' + '   Minor Class:' +
                           '<span style="color:#ff471a;font-weight:bold;">' + minor + '</span>',
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'
                   })
        return figure

    def create_sun_chart(self, area, major, time_select):
        if area is None:
            area_data = self.data.crime_data.iloc[:-1, :]
        else:
            area_data = self.data.crime_data.loc[self.data.crime_data['Borough'] == area]
        if time_select == 25:
            time = 'Total'
        else:
            time = self.data.TIME_LIST[time_select - 1]
        time_data = area_data[['Major Class Description', 'Minor Class Description', time]]
        if major == 'Total' or major is None:
            crime_data = time_data
            fig_sun = px.sunburst(crime_data.iloc[:-1, :], path=['Major Class Description', 'Minor Class Description'],
                                  values=time)
        else:
            crime_data = time_data.loc[time_data['Major Class Description'] == major]
            fig_sun = px.sunburst(crime_data, path=['Major Class Description', 'Minor Class Description'],
                                  values=time)
        fig_sun.update_layout(margin=dict(t=0, l=0, r=0, b=10),
                              )
        fig_sun.update_traces(
            hovertemplate='<b>%{label} </b> <br>Number of Crime: %{value}<br>'
        )
        return fig_sun
