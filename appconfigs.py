import configparser
import os


class AppConfigs:
    """A class used to represent project properties."""
    SOURCE_SECTION = "source"
    SOURCE_URL = "url"

    def __init__(self):
        configfile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', 'properties.ini'))

        self.config = configparser.ConfigParser()
        self.config.read(configfile)

    def get_source_url(self):
        """Get the real estate source url."""

        return self.config.get(AppConfigs.SOURCE_SECTION, AppConfigs.SOURCE_URL)
