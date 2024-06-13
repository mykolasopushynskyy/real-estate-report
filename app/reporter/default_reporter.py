from datetime import datetime

import numpy as np

from app.parsed_report import ParsedReport
from appconfigs import AppConfigs
import plotly.express as px
import os
import pandas as pd

class RealEstateHTMLReporter:
    """A class used to generate reports."""

    def __init__(self, appconfig: AppConfigs):
        self.appconfig = appconfig

    def generate_report(self, reportData: ParsedReport):
        """A method used to generate real estate report."""
        configfile = os.path.abspath(os.path.join(self.appconfig.get_report_destination_folder(),
                                                  datetime.now().strftime('%m/%d/%Y') + ".html"))


        x = pd.to_datetime([np.datetime64(date) for record in reportData.records])
        fig = px.line(reportData, x="date", y=reportData.records,
                      hover_data={"date": "|%B %d, %Y"},
                      title='custom tick labels with ticklabelmode="period"')

        fig.update_xaxes(
            rangeslider_visible=True,
            dtick="M1",
            tickformat="%b\n%Y",
            ticklabelmode="period")

        fig.write_html(configfile, auto_open=True)
