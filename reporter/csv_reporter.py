import csv
import os
import cpi
import logging

from datetime import datetime

from cpi.errors import CPIObjectDoesNotExist

from parsed_report import ParsedReport
from configs import AppConfigs, DATE_FIELD

# logger
logger = logging.getLogger(__name__)


class RealEstateCSVReporter:
    """
    A class used to generate CSV reports.
    """

    def __init__(self, configs: AppConfigs):
        """
        Init method of :class:`RealEstateCSVReporter` class. Initializes a date to be used for inflation adjustment

        :param configs: application configs
        """
        self.configs = configs
        self.inflate_to = datetime(self.configs.get_inflation_adjustment_year(), 1, 1)

    def generate_report(self, city: str, report_data: ParsedReport):
        """
        A method used to generate real estate report.

        :param city: name of city for report
        :param report_data: city report date
        :return: CSV report file path
        :rtype: str
        """
        fields = []
        for field in report_data.records.keys():
            fields.append(field)
            if field != DATE_FIELD:
                fields.append(field + " інфл.")

        report_file = "%s-%02d-%d.csv" % (city, self.configs.get_current_month(), self.configs.get_current_year())
        report_file = os.path.abspath(os.path.join(self.configs.get_report_destination_folder(), report_file))

        with open(report_file, 'w') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            for i in range(0, len(report_data.records[DATE_FIELD])):
                row = {}

                for district in report_data.records.keys():
                    try:
                        row[district] = report_data.records[district][i]
                        if district != DATE_FIELD:
                            district_adj = district + " інфл."
                            value_adj = cpi.inflate(report_data.records[district][i],
                                                    datetime.strptime(row[DATE_FIELD], "%Y-%m-%d"),
                                                    to=self.inflate_to)
                            row[district_adj] = round(value_adj)
                    except CPIObjectDoesNotExist as e:
                        # Inflation data is absent for this time period
                        row[district_adj] = None
                    except TypeError as e:
                        logger.error("Can't parse price value: ", e)
                    except IndexError as e:
                        logger.error("Can't parse html page: ", e)

                writer.writerow(row)
                csvfile.flush()

        return report_file
