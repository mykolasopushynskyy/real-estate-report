import requests

from appconfigs import AppConfigs


class RealEstateRawInfoParser:
    """A class used to make calls to real estate source."""
    def __init__(self, configs: AppConfigs):
        self.configs = configs

    def parse(self):
        """A class used to make calls to real estate source."""
        res = requests.post(self.configs.get_source_url())
        return res.text
