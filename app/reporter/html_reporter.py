from datetime import datetime

import cpi
import pandas as pd
import plotly.graph_objects as go
import webcolors
from _plotly_utils.colors.qualitative import Plotly
from webcolors import IntegerRGB

from app.consts import DATE_FIELD
from appconfigs import AppConfigs


class ColorIterator:
    """Class to iterate the Plotly palette and get the combination of palette color and brighter version of the
    same color"""

    def __init__(self):
        self.i = 0
        self.g10_colors = [dict(dark=value, bright=self.brighter_color(value)) for value in Plotly]

    def brighter_color(self, value):
        r, g, b = webcolors.hex_to_rgb(value)
        r = int(r + (255 - r) * 0.33)
        g = int(g + (255 - g) * 0.33)
        b = int(b + (255 - b) * 0.33)

        return webcolors.rgb_to_hex(webcolors.normalize_integer_triplet(IntegerRGB(red=r, green=g, blue=b)))

    def next_g10(self):
        self.i = self.i + 1
        return self.g10_colors[(self.i % len(self.g10_colors)) - 1]


class RealEstateHTMLReporter:
    """A class used to generate reports."""

    def __init__(self, appconfig: AppConfigs):
        self.appconfig = appconfig
        self.report_initial_date = datetime(self.appconfig.get_start_year(), 1, 1)

    def generate_report(self, city: str, report_file: str):
        """A method used to generate real estate report."""
        df = pd.read_csv(report_file)
        city = city.capitalize()
        fig = go.Figure()
        color_iterator = ColorIterator()

        # Create inflation adjusted columns
        for column_name in df.head():
            if column_name != DATE_FIELD:
                district = column_name
                district_adj = column_name + " інфл."
                toggled = None if district == city else "legendonly"
                width = 2 if district == city else 1

                df[district_adj] = df.apply(
                    lambda row: round(cpi.inflate(row[column_name],
                                                  datetime.strptime(row[DATE_FIELD], "%Y-%m-%d"),
                                                  to=self.report_initial_date)), axis=1
                )

                color = color_iterator.next_g10()

                go_district = go.Scatter(name=district, visible=toggled, legendgroup=district,
                                         x=df[DATE_FIELD],
                                         y=df[district], mode='lines',
                                         line=dict(dash="solid", shape="spline", color=color["dark"], width=width))

                go_district_adj = go.Scatter(name=district_adj, visible=toggled, legendgroup=district,
                                             x=df[DATE_FIELD],
                                             y=df[district_adj], mode='lines',
                                             line=dict(dash="3px", shape="spline", color=color["bright"], width=width))

                fig.add_trace(go_district)
                fig.add_trace(go_district_adj)

        fig.update_layout(
            title=f"%s - вторинний ринок" % city,
            hovermode="x unified",
            legend=dict(
                bordercolor="Black",
                borderwidth=1,
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="left",
                x=0
            )
        )
        fig.update_traces(
            hovertemplate="<br>".join([
                "%{y}$"
            ])
        )
        fig.update_yaxes(
            title="Ціна, дол. США"
        )
        fig.update_xaxes(
            ticks="outside",
            ticklabelmode="period",
            tickcolor="black",
            ticklen=10,
            minor=dict(
                ticklen=4,
                griddash="dot",
                gridcolor="white"),
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1р", step="year", stepmode="backward"),
                    dict(count=5, label="5р", step="year", stepmode="backward"),
                    dict(count=10, label="10р", step="year", stepmode="backward"),
                    dict(count=20, label="20р", step="year", stepmode="backward"),
                    dict(label="ввесь час", step="all")
                ])
            ),
            tickformat="%b '%y",
            tickformatstops=[
                dict(dtickrange=["M1", "M12"], value="%b '%y"),
                dict(dtickrange=["M12", None], value="%b %Y")
            ]
        )

        html_report_file = report_file.replace(".csv", ".html")
        fig.write_html(html_report_file, auto_open=False)
        return html_report_file
