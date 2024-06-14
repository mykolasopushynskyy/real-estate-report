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

    def run(self):
        """Run the main logic of application"""
        parsed_report = ParsedReport()

        end_year = datetime.now().year + 1
        for year in range(self.appconfigs.get_start_year(), end_year):
            for month in range(1, 13 if year != datetime.now().year else datetime.now().month):
                html_page = self.retriever.retrieve(year, month)
                new_report = self.parser.parse(html_page)

                parsed_report.append_all(new_report)
                print(f"Parsed: %s %s" % (year, month))

        report_file = self.csv_report.generate_report(parsed_report)
        self.html_report.generate_report(report_file)


if __name__ == '__main__':
    """Main method of application"""
    App().run()
