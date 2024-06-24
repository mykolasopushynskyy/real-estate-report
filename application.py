import progressbar
import app_configs as appconfigs
import app.retrievers.default_retriever as retrievers
import app.parsers.default_parser as parsers
import app.reporter.html_reporter as html_reporters
import app.reporter.csv_reporter as csv_reporters

from datetime import datetime
from app.parsed_report import ParsedReport

# progress bar variables names
CITY = "city"
YEAR = "year"


class App:
    """
    App class is implemented to create a structure of the application and contains mail business logic
    """

    def __init__(self):
        """
        Initialize the core structure of application

        - initializes application configs class
        - initializes HTML raw date retriever
        - initializes HTML real estate prices parsers
        - initializes CSV and HTML reporters
        """
        self.appconfigs = appconfigs.AppConfigs()
        self.retriever = retrievers.RealEstateRawInfoRetriever(self.appconfigs)
        self.parser = parsers.RealEstateRawInfoParser()
        self.html_reporter = html_reporters.RealEstateHTMLReporter()
        self.csv_reporter = csv_reporters.RealEstateCSVReporter(self.appconfigs)

        progressbar.streams.flush()
        progressbar.streams.wrap_stdout()

    def generate_report_for_city(self, city: str):
        """
        Generates full report for one region/city

        We are calling api to retrieve information yearly starting from 2003 to current yar about some particular
        city(ies) we store information in configs file or manual using The result is the parsed dictionary with
        time-series monthly data about prices by city districts Than the data is written to CSV file to keep raw
        information as well as into interactive HTML diagram which is useful for demos or presentation in
        human-readable form.

        :param city: The name of the city from configs
        :return: CSV and HTML reports absolute path's
        :rtype: tuple
        """
        parsed_report = ParsedReport()

        end_year = datetime.now().year + 1
        start_year = self.appconfigs.get_start_year()

        widgets = [
            progressbar.Timer("%(elapsed)s"), " ",
            progressbar.GranularBar(markers=" ━", left="[", right="]"), " ",
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
        bar.print("\t- CSV  report for city {0}: {1}".format(city.capitalize(), self.obfuscate_path(csv_report)))
        html_report = self.html_reporter.generate_report(city, parsed_report.records.keys(), csv_report)
        bar.print("\t- HTML report for city {0}: {1}".format(city.capitalize(), self.obfuscate_path(html_report)))

        bar.print()

        return csv_report, html_report

    def run(self, cities=None):
        """
        Run the main logic of application. Get the cities list from configs and starts to generate reports for each
        city one-by-one.
        """
        if cities is None or len(cities) == 0:
            cities = list(self.appconfigs.get_cities().keys())

        print("\nStarting price parsing for cities: {0}\n".format(cities))
        for city in cities:
            self.generate_report_for_city(city)


if __name__ == '__main__':
    """Main method of application"""
    App().run(["львів"])
