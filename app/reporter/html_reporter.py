import os

from app.parsed_report import ParsedReport

import pandas as pd
import plotly.express as px

from appconfigs import AppConfigs


class RealEstateHTMLReporter:
    """A class used to generate reports."""

    def __init__(self):
        pass

    def generate_report(self, report_file: str):
        """A method used to generate real estate report."""

        df = pd.read_csv(report_file)

        fig = px.line(df, x=ParsedReport.DATE_FIELD, y=df.columns, title='Ціни на житло', line_shape='spline')
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
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=5, label="5y", step="year", stepmode="backward"),
                    dict(count=10, label="10y", step="year", stepmode="backward"),
                    dict(count=20, label="20y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            tickformat="%b '%y",
            tickformatstops=[
                dict(dtickrange=["M1", "M12"], value="%b '%y"),
                dict(dtickrange=["M12", None], value="%b %Y")
            ]
        )

        html_report_file = report_file.replace(".csv", ".html")
        fig.write_html(html_report_file, auto_open=True)
        return html_report_file


if __name__ == '__main__':
    """Main method of application"""
    report_file = os.path.abspath(os.path.join(AppConfigs.PROJECT_DIR, 'reports', '13-06-2024.csv'))
    RealEstateHTMLReporter().generate_report(report_file)
