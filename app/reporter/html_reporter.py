from datetime import datetime

from app.consts import DATE_FIELD

import pandas as pd
import plotly.express as px
import cpi

from appconfigs import AppConfigs


class RealEstateHTMLReporter:
    """A class used to generate reports."""

    def __init__(self, appconfig: AppConfigs):
        self.appconfig = appconfig
        self.report_initial_date = datetime(self.appconfig.get_start_year(), 1, 1)

    def generate_report(self, city: str, report_file: str):
        """A method used to generate real estate report."""
        df = pd.read_csv(report_file)

        # Create inflation adjusted columns
        for column_name in df.head():
            if column_name != DATE_FIELD:
                df[column_name + " інфляція"] = df.apply(
                    lambda row: round(cpi.inflate(row[column_name], datetime.strptime(row[DATE_FIELD], "%Y-%m-%d"),
                                            to=self.report_initial_date)), axis=1
                )

        fig = px.line(df, x=DATE_FIELD, y=df.columns,
                      title=f"%s - вторинний ринок" % city.capitalize(), line_shape="spline")
        fig.update_layout(
            hovermode="x unified",
            legend_title_text='Район',
            legend=dict(
                yanchor="top",
                xanchor="left",
                bordercolor="Black",
                borderwidth=1,
                x=0,
                y=1
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
            title="Дата",
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
