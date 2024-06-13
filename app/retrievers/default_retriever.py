import requests

from appconfigs import AppConfigs

REGION = '0'
OBLAST = 'regs_248'


class RealEstateRawInfoRetriever:
    """A class used to make calls to real estate source."""

    def __init__(self, appconfig: AppConfigs):
        self.appconfigs = appconfig

    def retrieve(self, year: int, month: int):
        """A class used to make calls to real estate source."""
        url = "http://www.svdevelopment.com/ua/web/flat_costs/"

        date = "%s-%02d-01" % (year, month)

        payload = (
                'st%5Bact%5D=stat&st%5Boblast%5D=' + OBLAST + (
                '&st%5Bregion%5D=' + REGION + ('&st%5Bdate1%5D=' + date + ('&st%5Bdate2%5D=' + date))))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
