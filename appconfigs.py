import configparser
import os


class AppConfigs:
    """A class used to represent project properties."""
    SOURCE = "source"
    SOURCE_URL = "url"
    CITIES = "cities"
    START_YEAR = "start_year"
    REPORT = "report"
    DESTINATION_FOLDER = "destination_folder"

    def __init__(self):
        configfile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', 'properties.ini'))

        self.config = configparser.ConfigParser()
        self.config.read(configfile)

    def get_source_url(self):
        """Get the real estate source url."""

        return self.config.get(AppConfigs.SOURCE, AppConfigs.SOURCE_URL)

    def get_cities(self):
        """Get the real estate available cities"""
        cities = {}
        for city in self.config.options(AppConfigs.CITIES):
            cities[city] = self.config.get(AppConfigs.CITIES, city)

        return cities

    def get_start_year(self):
        """Get the reports start year."""

        return int(self.config.get(AppConfigs.SOURCE, AppConfigs.START_YEAR))

    def get_report_destination_folder(self):
        """Get the reports folder"""

        return os.path.join(os.path.dirname(__file__),
                            self.config.get(AppConfigs.REPORT, AppConfigs.DESTINATION_FOLDER))
