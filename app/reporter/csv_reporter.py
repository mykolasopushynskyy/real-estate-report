import csv
import os
from datetime import datetime

from app.consts import DATE_FIELD
from app.parsed_report import ParsedReport
from appconfigs import AppConfigs


class RealEstateCSVReporter:
    """A class used to generate reports."""

    def __init__(self, appconfig: AppConfigs):
        self.appconfig = appconfig

    def generate_report(self, city: str, report_data: ParsedReport):
        """A method used to generate real estate report."""
        fields = list(report_data.records.keys())

        report_file = os.path.abspath(os.path.join(self.appconfig.get_report_destination_folder(),
                                                   city + "-" + datetime.now().strftime('%d-%m-%Y') + ".csv"))

        with open(report_file, 'w') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            for i in range(0, len(report_data.records[DATE_FIELD])):
                row = {}

                for district in fields:
                    try:
                        row[district] = report_data.records[district][i]
                    except TypeError:
                        print("Parsing error")
                    except IndexError:
                        print("Parsing error")

                writer.writerow(row)
                csvfile.flush()

        return report_file
