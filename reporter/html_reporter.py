import pandas as pd
import plotly.graph_objects as go
import webcolors

from configs import AppConfigs
from webcolors import IntegerRGB
from consts import DATE_FIELD

COLOR_PALETTE = ("#4421af", "#ea5545", "#f46a9b", "#ef9b20", "#50e991", "#87bc45", "#1a53ff", "#b33dc6", "#e60049",
                 "#0bb4ff", "#9b19f5", "#ffa300", "#dc0ab4", "#00bfa0")


def brighter_color(value):
    """
    Make color brighter from color derived from input color.

    :param value: hex color representation
    :return: hex code of brighter color
    :rtype: str
    """
    r, g, b = webcolors.hex_to_rgb(value)
    r = int(r + (255 - r) * 0.33)
    g = int(g + (255 - g) * 0.33)
    b = int(b + (255 - b) * 0.33)

    return webcolors.rgb_to_hex(webcolors.normalize_integer_triplet(IntegerRGB(red=r, green=g, blue=b)))


def get_report_file_path(data_file):
    """
    Gets report file name out of data file name

    :param data_file: data file absolute path
    :return: report file name
    :rtype: str
    """
    return data_file.replace(".csv", ".html")


class ColorIterator:
    """
    Class to iterate the Plotly palette and get the combination of palette color and brighter version of the same color.
    """

    def __init__(self):
        """
        Init method of :class:`ColorIterator` class. Initializes a color palette for diagram with original and bright
        color version.
        """
        self.i = 0
        self.colors = [dict(dark=value, bright=brighter_color(value)) for value in COLOR_PALETTE]

    def __iter__(self):
        """
        Iter method of :class:`ColorIterator` class. Returns iterator
        """
        self.i = 0
        return self

    def __next__(self):
        """
        Return next color of palette

        :return: next palette color
        :rtype: dict
        """
        self.i = self.i + 1
        return self.colors[(self.i % len(self.colors)) - 1]


class RealEstateHTMLReporter:
    """
    A class used to generate HTML Plotly reports.
    """

    def __init__(self, configs: AppConfigs):
        """
        Init method of :class:`RealEstateHTMLReporter` class.

        :param configs: application configs
        """
        self.config = configs

    def generate_report(self, city: str, districts: list, data_file: str):
        """
        A method used to generate real estate HTML diagram report.

        :param city: city of report
        :param districts: city districts of report
        :param data_file: file of CSV data to build diagram
        :return: HTML report file path
        :rtype: str
        """
        df = pd.read_csv(data_file)
        city = city.capitalize()
        fig = go.Figure()
        color_iterator = ColorIterator()

        # Create inflation adjusted columns
        for column_name in districts:
            if column_name != DATE_FIELD:
                district = column_name
                district_adj = column_name + " інфл."

                toggled = None if district == city or (not self.config.hide_districts()) else "legendonly"
                width = 2

                color = next(color_iterator)

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
                orientation="h",
                yanchor="bottom",
                xanchor="left",
                x=0,
                y=-0.5,
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

        html_report_file = data_file.replace(".csv", ".html")
        fig.write_html(html_report_file, auto_open=False)
        return html_report_file
