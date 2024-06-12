
class PriceRecord:
    """ A class used to represent price record by date and price """
    def __init__(self, date: str, price: int):
        self.date = date
        self.price = price

    def get_date(self):
        return self.date

    def get_price(self):
        return self.price


class ParsedReport:
    """ A class used to represent report of prices divided on districts
        {
            "district": [PriceRecord1, PriceRecord2, ...]
            ...
        }
    """
    def __init__(self):
        self.records = {}

    def append(self, district, date, price):
        if district in self.records:
            self.records[district].append(PriceRecord(date, price))
        else:
            self.records[district] = []
