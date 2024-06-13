class ParsedReport:
    """ A class used to represent report of prices divided on districts
        {
            "district": [PriceRecord1, PriceRecord2, ...]
            ...
        }
    """

    DATE_FIELD = "Date"

    def __init__(self):
        self.records = {
            ParsedReport.DATE_FIELD: []
        }

    def append(self, date, prices):
        for district in prices:
            if district != ParsedReport.DATE_FIELD:
                if not (district in self.records):
                    self.records[district] = []
                self.records[district].extend(prices[district])

        self.records[ParsedReport.DATE_FIELD].append(date)

    def append_all(self, report):
        for key in report.records.keys():
            if not (key in self.records):
                self.records[key] = []
            self.records[key].extend(report.records[key])
