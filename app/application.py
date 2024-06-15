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
        """Initialize the structure of application"""
        self.appconfigs = appconfigs.AppConfigs()
        self.retriever = retrievers.RealEstateRawInfoRetriever(self.appconfigs)
        self.parser = parsers.RealEstateRawInfoParser()
        self.html_report = html_reporters.RealEstateHTMLReporter()
        self.csv_report = csv_reporters.RealEstateCSVReporter(self.appconfigs)

    def generate_report_for_city(self, city: str):
        """Generates report for one region/city"""
        parsed_report = ParsedReport()

        end_year = datetime.now().year + 1
        start_year = self.appconfigs.get_start_year()

        s1 = "·■"
        widgets = [
            city.capitalize(),
            " [ ", progressbar.Variable("year", format="{formatted_value}", width=4), " / ", str(end_year - 1), " ] ",
            progressbar.Percentage(), " ",

            progressbar.GranularBar(markers=s1, left="[", right="]")
        ]
        bar = progressbar.ProgressBar(widgets=widgets, enable_colors=True, term_width=75)
        for year in bar(range(start_year, end_year)):
            bar.variables["year"] = year
            html_page = self.retriever.retrieve(city, year)
            new_report = self.parser.parse(city, year, html_page)

            parsed_report.append_all(new_report)

        csv_report = self.csv_report.generate_report(city, parsed_report)
        bar.print("\tCSV report for city {0}: {1}".format(city.capitalize(), csv_report))
        html_report = self.html_report.generate_report(csv_report)
        bar.print("\tHTML report for city {0}: {1}".format(city.capitalize(), html_report))

        bar.print()

        return csv_report, html_report

    def run(self, cities=None):
        """Run the main logic of application"""
        cities = ["одеса", "львів"]

        if cities is None:
            cities = list(self.appconfigs.get_cities().keys())

        print()
        print("Starting price parsing for cities: {0}".format(cities))
        for city in cities:
            self.generate_report_for_city(city)


if __name__ == '__main__':
    """Main method of application"""

    App().run()
