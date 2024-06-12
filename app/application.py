import appconfigs as appconfigs
import app.retrievers.default_retriever as retrievers
import app.parsers.default_parser as parsers
import app.reporter.default_reporter as reporters


class App:
    """App class to create a structure of the application"""

    def __init__(self):
        """Initialize the structure of application"""
        self.appconfigs = appconfigs.AppConfigs()
        self.retriever = retrievers.RealEstateRawInfoRetriever(self.appconfigs)
        self.parser = parsers.RealEstateRawInfoParser()
        self.reporter = reporters.RealEstateCSVReporter()

    def run(self):
        """Run the main logic of application"""
        pass


if __name__ == '__main__':
    """Main method of application"""

    application = App()
    application.run()
