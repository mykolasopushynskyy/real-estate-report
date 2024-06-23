import configparser
import os

SOURCE = "source"
SOURCE_URL = "url"
CITIES = "cities"
START_YEAR = "start_year"
REPORT = "report"
DESTINATION_FOLDER = "destination_folder"
INFLATION_ADJUSTMENT_YEAR = "inflation_adjustment_year"

PROJECT_DIR = os.path.dirname(__file__)

class AppConfigs:
    """A class used to represent project properties. Reads properties from config file ./resources/properties.ini"""

    def __init__(self):
        configfile = os.path.abspath(os.path.join(PROJECT_DIR, 'resources', 'properties.ini'))

        self.config = configparser.ConfigParser()
        self.config.read(configfile)

    def get_source_url(self):
        """Get the real estate source url."""

        return self.config.get(SOURCE, SOURCE_URL)

    def get_cities(self):
        """Get the real estate available cities"""
        cities = {}
        for city in self.config.options(CITIES):
            cities[city] = self.config.get(CITIES, city)

        return cities

    def get_start_year(self):
        """Get the reports start year."""

        return int(self.config.get(SOURCE, START_YEAR))

    def get_inflation_adjustment_year(self):
        """Get the reports start year."""

        return int(self.config.get(SOURCE, INFLATION_ADJUSTMENT_YEAR))

    def get_report_destination_folder(self):
        """Get the reports folder"""

        return os.path.join(os.path.dirname(__file__), self.config.get(REPORT, DESTINATION_FOLDER))
