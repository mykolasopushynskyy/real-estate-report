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

        for year in range(start_year, end_year):
            widgets = [
                str(year),
                " [ ", progressbar.SimpleProgress(), " ] ",
                progressbar.Percentage(), " ",
                progressbar.GranularBar()
            ]

            bar = progressbar.ProgressBar(widgets=widgets, enable_colors=True, )
            for month in bar(range(1, 13 if year != datetime.now().year else datetime.now().month)):
                html_page = self.retriever.retrieve(city, year, month)
                new_report = self.parser.parse(city, html_page)

                parsed_report.append_all(new_report)

            bar.finish()

        print()
        csv_report = self.csv_report.generate_report(city, parsed_report)
        print("CSV report generated for city {0}: {1}".format(city, csv_report))
        html_report = self.html_report.generate_report(csv_report)
        print("HTML report generated for city {0}: {1}".format(city, html_report))

        return csv_report, html_report

    def run(self, cities=None):
        """Run the main logic of application"""
        if cities is None:
            cities = self.appconfigs.get_cities()

        for city in cities:
            print("Starting price parsing for city: [ {0} ]".format(city))
            self.generate_report_for_city(city)
            print("Finished price parsing for city: [ {0} ]".format(city))


if __name__ == '__main__':
    """Main method of application"""
    cities_to_discover = ["київ"]
    App().run(cities_to_discover)
