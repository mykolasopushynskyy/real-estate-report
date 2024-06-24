import requests

from configs import AppConfigs


class RealEstateRawInfoRetriever:
    """
    A class used to make calls to real estate source.
    """

    REGION = "0"

    def __init__(self, configs: AppConfigs):
        """
        Init method of :class:`RealEstateRawInfoRetriever` class

        :param configs: application configs
        """
        self.configs = configs

    def retrieve(self, city: str, year: int):
        """
        A class used to make calls to real estate source. The website URL is located in configs.

        :param city: city used to retrieve real estate information
        :param year: year for which real estate prices are retrieved
        :return: raw HTML page
        :rtype: str
        """
        url = self.configs.get_source_url()

        date1 = "%s-01-01" % year
        date2 = "%s-01-01" % (year + 1)

        city_reg = self.configs.get_cities()[city]

        payload = (
                "st%5Bact%5D=stat&st%5Boblast%5D=" + city_reg + (
                "&st%5Bregion%5D=" + RealEstateRawInfoRetriever.REGION +
                ("&st%5Bdate1%5D=" + date1 + ("&st%5Bdate2%5D=" + date2))))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
