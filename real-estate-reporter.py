#!/usr/bin/env python3

"""
Real estate reporter

usage: ./real-estate-reporter.py [-h] [-c Львів [Київ ...]] [--hide-districts [true | false]]

options:
  -h, --help           show help message and exit
  -c Львів [Київ ...], --cities Львів [Київ ...]
                       cities for report generation
  --hide-districts [true | false]
                       toggle off districts prices on diagram

"""
import logging
import progressbar
import argparse
import configs
import reporter.html_reporter as html_reporter
import retriever.default_retriever as retriever
import reporter.csv_reporter as csv_reporter
import parser.default_parser as parser

from parsed_report import ParsedReport

# logger
logger = logging.getLogger(__name__)

# progress bar variables names
CITY = "city"
YEAR = "year"


class App:
    """
    App class is implemented to create a structure of the application and contains mail business logic
    """

    def __init__(self, cl_args: argparse.Namespace):
        """
        Initialize the core structure of application

        - initializes application configs class
        - initializes HTML raw date retriever
        - initializes HTML real estate prices parsers
        - initializes CSV and HTML reporters

        :param cl_args: command-line arguments
        """
        self.configs = configs.AppConfigs(cl_args)
        self.retriever = retriever.RealEstateRawInfoRetriever(self.configs)
        self.parser = parser.RealEstateRawInfoParser(self.configs)
        self.html_reporter = html_reporter.RealEstateHTMLReporter(self.configs)
        self.csv_reporter = csv_reporter.RealEstateCSVReporter(self.configs)

        progressbar.streams.flush()
        progressbar.streams.wrap_stdout()

    def generate_report_for_city(self, city: str):
        """
        Generates full report for one region/city

        Calling API to retrieve information yearly starting from 2003 to current yar about some particular
        city(ies). store information in configs file or manual using the result is the parsed dictionary with
        time-series monthly data about prices by city districts Than the data is written to CSV file to keep raw
        information as well as into interactive HTML diagram which is useful for demos or presentation in
        human-readable form.

        :param city: The name of the city from configs
        :return: CSV and HTML reports absolute path's
        :rtype: tuple
        """
        parsed_report = ParsedReport()

        end_year = self.configs.get_current_year() + 1
        start_year = self.configs.get_start_year()

        widgets = [
            progressbar.Timer("%(elapsed)s"), " ",
            progressbar.GranularBar(markers=" ■", left="[", right="]"), " ",
            progressbar.Percentage(), " ",
            progressbar.Variable(YEAR, format="{formatted_value}", width=15), " ",
            progressbar.Variable(CITY, format="{formatted_value}", width=4)
        ]
        bar = progressbar.ProgressBar(widgets=widgets, enable_colors=True, term_width=75, redirect_stdout=True)
        bar.variables[YEAR] = f"[ %4s / %4s ]" % (start_year, str(end_year - 1))
        bar.variables[CITY] = city.capitalize()

        for year in bar(range(start_year, end_year)):
            html_page = self.retriever.retrieve(city, year)
            new_report = self.parser.parse(city, year, html_page)

            parsed_report.extend(new_report)

            bar.variables[YEAR] = f"[ %4s / %4s ]" % (year, str(end_year - 1))
            bar.variables[CITY] = city.capitalize()

        csv_report = self.csv_reporter.generate_report(city, parsed_report)
        bar.print("\t- CSV  report for city {0}: {1}".format(city.capitalize(),
                                                             configs.obfuscate_path(csv_report)))

        html_report = self.html_reporter.generate_report(city, parsed_report.records.keys(), csv_report)
        bar.print("\t- HTML report for city {0}: {1}".format(city.capitalize(),
                                                             configs.obfuscate_path(html_report)))

        bar.print()
        return csv_report, html_report


def main(app: App):
    """
    Run the main logic of application. Get the cities list from configs or args and starts to generate reports for
    each city one-by-one.
    """
    cities = set(app.configs.get_cities())
    allowed_cities = set(app.configs.get_cities_mappings().keys())

    # validate cities
    if not cities.issubset(allowed_cities):
        raise ValueError("Cities %s are not allowed" % (list(cities - allowed_cities)))

    sorted_cities = list(cities)
    sorted_cities.sort()
    logger.info("\nStarting price parsing for cities: {0}\n".format(sorted_cities))
    for city in cities:
        app.generate_report_for_city(city)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser("./real-estate-reporter.py")
    arg_parser.add_argument("-c", "--cities", nargs="+", default=[], required=False,
                            help="cities for report generation")
    arg_parser.add_argument("--hide-districts", default=None, required=False, type=str,
                            help="toggle off districts prices on diagram")

    # run application
    main(App(arg_parser.parse_args()))
