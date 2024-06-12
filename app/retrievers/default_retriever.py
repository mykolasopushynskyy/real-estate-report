import requests

from appconfigs import AppConfigs


class RealEstateRawInfoRetriever:
    """A class used to make calls to real estate source."""
    def __init__(self, appconfig: AppConfigs):
        self.appconfigs = appconfig

    def retrieve(self, year: int, month: int):
        """A class used to make calls to real estate source."""
        res = requests.post(self.appconfigs.get_source_url())
        return res.text
