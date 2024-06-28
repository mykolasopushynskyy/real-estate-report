import jinja2
import requests

from configs import AppConfigs

REGION = "0"


class RealEstateRawInfoRetriever:
    """
    A class used to make calls to real estate source.
    """

    def __init__(self, configs: AppConfigs):
        """
        Init method of :class:`RealEstateRawInfoRetriever` class

        :param configs: application configs
        """
        self.configs = configs
        self.env = jinja2.Environment()
        self.template = self.env.from_string("st%5Bact%5D=stat&st%5Boblast%5D={{city_reg}}&st%5Bregion%5D={{region}}"
                                             "&st%5Bdate1%5D={{from_date}}&st%5Bdate2%5D={{to_date}}")

    def retrieve(self, city: str, year: int):
        """
        A class used to make calls to real estate source. The website URL is located in configs.

        :param city: city used to retrieve real estate information
        :param year: year for which real estate prices are retrieved
        :return: raw HTML page
        :rtype: str
        """
        url = self.configs.get_source_url()

        from_date = "%s-01-01" % year
        to_date = "%s-01-01" % (year + 1)

        city_reg = self.configs.get_cities_mappings()[city]
        payload = self.template.render(city_reg=city_reg, region=REGION, from_date=from_date, to_date=to_date)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
