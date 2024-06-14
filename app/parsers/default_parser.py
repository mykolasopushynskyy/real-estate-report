import collections

collections.Callable = collections.abc.Callable
from bs4 import BeautifulSoup
from app.parsed_report import ParsedReport

HTML_PARSER = "html.parser"


class RealEstateRawInfoParser:
    """A class used to make calls to real estate source."""

    def __init__(self):
        pass

    def parse(self, city: str, html: str):
        """A class used to make calls to real estate source."""
        result = ParsedReport()
        soup = BeautifulSoup(html, HTML_PARSER)

        # Retrieve table data
        prices_table = (soup.find("table", {"class": "tHH"})
                        .findChildren("tr", {"class": "vals"}))
        date = (soup.find_all("table", class_="tHH")[0]
            .find_all_next("tr", class_="headHH2")[0]
            .find_all_next("td")[1]).text.split(".")
        date = date[2] + "-" + date[1] + "-" + date[0]

        # Form a finalized report
        prices = {}
        for data in prices_table:
            string_data = data.findChildren("td")
            if len(string_data) == 2 and string_data[1].text.strip() != "-":
                district = string_data[0].text
                price = int(string_data[1].text.strip().strip("$"))
                if district == '':
                    district = city.capitalize()
                if not (district in prices):
                    prices[district] = []
                prices[district].append(price)

        result.append(date, prices)

        return result
