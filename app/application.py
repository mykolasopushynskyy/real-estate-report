import progressbar

import appconfigs as appconfigs
import app.retrievers.default_retriever as retrievers
import app.parsers.default_parser as parsers
import app.reporter.html_reporter as html_reporters
import app.reporter.csv_reporter as csv_reporters

from datetime import datetime

from app.parsed_report import ParsedReport


class App:
    """App class to create a structure of the application"""

    def __init__(self):
        """Initialize the structure of application

        - initializes application configs class
        - initializes retriever parsers and reporters

        Methods
        -------
        generate_report_for_city(city: str):
            Generates report for one region/city
        run(cities: list):
            Get the cities list from configs and starts to generate reports for each city one-by-one
        """
        self.appconfigs = appconfigs.AppConfigs()
        self.retriever = retrievers.RealEstateRawInfoRetriever(self.appconfigs)
        self.parser = parsers.RealEstateRawInfoParser()
        self.html_reporter = html_reporters.RealEstateHTMLReporter()
        self.csv_reporter = csv_reporters.RealEstateCSVReporter(self.appconfigs)

    def generate_report_for_city(self, city: str):
        """ Generates report for one region/city

        We are calling api to retrieve information yearly starting from 2003 to current yar
        about some particular city(ies) we store information in configs file or manual using
        The result is the parsed dictionary with time-series monthly data about prices by city districts
        Than the data is written to CSV file to keep raw information as well as into
        interactive HTML diagram which is useful for demos or presentation in human-readable form.

        Parameters
        ----------
        city : str
            The name of the city
        """
        parsed_report = ParsedReport()

        end_year = datetime.now().year + 1
        start_year = self.appconfigs.get_start_year()

        widgets = [
            city.capitalize(),
            " [ ", progressbar.Variable("year", format="{formatted_value}", width=4), " / ", str(end_year - 1), " ] ",
            progressbar.Percentage(), " ",
            progressbar.GranularBar(markers="·■", left="[", right="]")
        ]
        bar = progressbar.ProgressBar(widgets=widgets, enable_colors=True, term_width=75)
        for year in bar(range(start_year, end_year)):
            bar.variables["year"] = year
            html_page = self.retriever.retrieve(city, year)
            new_report = self.parser.parse(city, year, html_page)

            parsed_report.append_all(new_report)

        csv_report = self.csv_reporter.generate_report(city, parsed_report)
        bar.print("\t├─CSV report for city {0}: {1}".format(city.capitalize(), csv_report))
        html_report = self.html_reporter.generate_report(csv_report)
        bar.print("\t└─HTML report for city {0}: {1}".format(city.capitalize(), html_report))

        bar.print()

        return csv_report, html_report

    def run(self, cities=None):
        """Run the main logic of application

        Get the cities list from configs and starts to generate reports for each city one-by-one
        """
        if cities is None:
            cities = list(self.appconfigs.get_cities().keys())

        print()
        print("Starting price parsing for cities: {0}".format(cities))
        for city in cities:
            self.generate_report_for_city(city)


if __name__ == '__main__':
    """Main method of application"""
    App().run()
