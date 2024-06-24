import configparser
import os

SOURCE = "source"
SOURCE_URL = "url"
CITIES = "cities"
START_YEAR = "start_year"
REPORT = "report"
HIDE_DISTRICTS = "hide_districts"
DESTINATION_FOLDER = "destination_folder"
INFLATION_ADJUSTMENT_YEAR = "inflation_adjustment_year"

PROJECT_DIR = os.path.dirname(__file__)


def obfuscate_path(file_path: str):
    """
    Obfuscates the absolute path of project directory

    :param file_path: file path to obfuscate project absolute path
    :return:
    """
    return file_path.replace(PROJECT_DIR, "<project_path>")


class AppConfigs:
    """
    A class used to read project properties. Reads properties from config file.
    """

    def __init__(self):
        """
        Init method of :class:`AppConfigs` class. Reads config file and initializes config parser
        """
        configfile = os.path.abspath(os.path.join(PROJECT_DIR, 'resources', 'properties.ini'))

        self.config = configparser.ConfigParser()
        self.config.read(configfile)

    def get_source_url(self):
        """
        Get the real estate source url

        :return: real estate source url
        :rtype: str
        """

        return self.config.get(SOURCE, SOURCE_URL)

    def get_cities(self):
        """
        Get the real estate available cities

        :return: mapping between cities and retriever url city id
        :rtype: dict
        """
        cities = {}
        for city in self.config.options(CITIES):
            cities[city] = self.config.get(CITIES, city)

        return cities

    def get_start_year(self):
        """
        Get the reports start year

        :return: start year of report generation
        :rtype: int
        """

        return int(self.config.get(SOURCE, START_YEAR))

    def get_inflation_adjustment_year(self):
        """Get the year for inflation adjustment
        :rtype: int
        """

        return int(self.config.get(SOURCE, INFLATION_ADJUSTMENT_YEAR))

    def hide_districts(self):
        """
        Hide city districts on final diagram

        :return: config to show/hide districts on final diagram
        :rtype: bool
        """

        return bool(self.config.get(REPORT, HIDE_DISTRICTS))

    def get_report_destination_folder(self):
        """
        Get the reports folder

        :return: absolute path reports folder
        :rtype: str
        """

        return os.path.join(os.path.dirname(__file__), self.config.get(REPORT, DESTINATION_FOLDER))
