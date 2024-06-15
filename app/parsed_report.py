class ParsedReport:
    """ A class used to represent report of prices divided on districts
        {
            "Date":      [date1,  date2,  ...]
            "District1": [price1, price2, ...]
            "District2": [price1, price2, ...]
            ...
        }
    """

    DATE_FIELD = "Date"

    def __init__(self):
        self.records = {
            ParsedReport.DATE_FIELD: []
        }

    def append(self, date, prices):
        """Appends row to report"""
        for district in prices:
            if district != ParsedReport.DATE_FIELD:
                if not (district in self.records):
                    self.records[district] = []
                self.records[district].extend(prices[district])

        self.records[ParsedReport.DATE_FIELD].append(date)

    def append_dates(self, dates: list):
        """Appends row to report"""
        self.append_row(ParsedReport.DATE_FIELD, dates)

    def append_row(self, key: str, dates: list):
        """Appends row to report"""
        if not (key in self.records):
            self.records[key] = []
        self.records[key].extend(dates)

    def append_all(self, report):
        """Appends reports together"""
        for key in report.records.keys():
            if not (key in self.records):
                self.records[key] = []
            self.records[key].extend(report.records[key])
