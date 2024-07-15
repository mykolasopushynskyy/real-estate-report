import collections

from configs import AppConfigs, HTML_PARSER, DATE_FIELD
from bs4 import BeautifulSoup
from parsed_report import ParsedReport

FULL_TABLE_LENGTH = 14

collections.Callable = collections.abc.Callable


class RealEstateRawInfoParser:
    """
    A class used to make calls to real estate source and parse the HTML results from site.
    """

    def __init__(self, configs: AppConfigs):
        """
        Init method of :class:`RealEstateRawInfoParser` class

        :param configs: application configs
        """
        self.configs = configs

    def parse(self, city: str, year: int, html: str):
        """
        A class used to make calls to real estate source.

        :param city: name of city
        :param year: year to parse current year
        :param html: raw HTML to parse
        :return: report with parsed data
        :rtype: ParsedReport
        """
        result = ParsedReport()
        soup = BeautifulSoup(html, HTML_PARSER)

        # Retrieve table data
        prices_table = (soup.find("table", {"class": "tHH"})
                        .findChildren("tr", {"class": "vals"}))

        dates = []
        districts = {}
        month_to_parse = 13 if year != self.configs.get_current_year() else self.configs.get_current_month()
        for month in range(1, month_to_parse):
            date = (soup.find_all("table", class_="tHH")[0]
            .find_all_next("tr", class_="headHH2")[0]
            .find_all_next("td")[month]).text.split(".")

            dates.append(date[1] + "-" + date[0] + "-01")

            # Form a finalized report
            for row in prices_table:
                string_data = row.findChildren("td")

                district = str(string_data[0].text).capitalize()
                if district != "" or len(string_data) == FULL_TABLE_LENGTH and string_data[1].text.strip() != "-":
                    if district == "":
                        district = city.capitalize()
                    try:
                        price = int(string_data[month].text.strip().strip("$"))
                        if not (district in districts.keys()):
                            districts[district] = []
                        districts[district].append(price)
                    except ValueError as e:
                        districts[district].append(0)

        for district in districts:
            result.append_column(district, districts[district])

        result.append_column(DATE_FIELD, dates)
        return result
