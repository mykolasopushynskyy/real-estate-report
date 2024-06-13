import appconfigs as appconfigs
import app.retrievers.default_retriever as retrievers
import app.parsers.default_parser as parsers
import app.reporter.default_reporter as reporters

from app.parsed_report import ParsedReport


class App:
    """App class to create a structure of the application"""

    def __init__(self):
        """Initialize the structure of application"""
        self.appconfigs = appconfigs.AppConfigs()
        self.retriever = retrievers.RealEstateRawInfoRetriever(self.appconfigs)
        self.parser = parsers.RealEstateRawInfoParser()
        self.reporter = reporters.RealEstateHTMLReporter(self.appconfigs)

    def run(self):
        """Run the main logic of application"""
        parsed_report = ParsedReport()

        end_year = 2004  # datetime.now().year
        for year in range(self.appconfigs.get_start_year(), end_year):
            for month in range(1, 13):
                html_page = self.retriever.retrieve(year, month)
                new_report = self.parser.parse(html_page)

                parsed_report.append_all(new_report)

        self.reporter.generate_report(parsed_report)


if __name__ == '__main__':
    """Main method of application"""
    App().run()
