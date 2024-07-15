from consts import DATE_FIELD


class ParsedReport:
    """
    Class used to represent a time-series report of prices of city and city districts
    {
        "Date":      [date1,  date2,  ...]
        "District1": [price1, price2, ...]
        "District2": [price1, price2, ...]
        ...
    }
    """

    def __init__(self):
        """
        if __init__ method not take any parameters or not has any side effects please not add dockstring
        Init method of :class:`ParsedReport` class. Initializes the records with empty dates column.
        """

        self.records = {
            DATE_FIELD: []
        }

    def append_row(self, date, prices):
        """
        Appends row to report

        :param date: time of new row record
        :param prices: prices for each city districts
        """

        for district in prices:
            if district != DATE_FIELD:
                if not (district in self.records):
                    self.records[district] = []
                self.records[district].extend(prices[district])

        self.records[DATE_FIELD].append(date)

    def append_column(self, name: str, values: list):
        """
        Appends column to report

        :param name: district name
        :param values: prices
        """

        if not (name in self.records):
            self.records[name] = []
        self.records[name].extend(values)

    def extend(self, report):
        """
        Merge reports together

        :param report: report to extend
        """

        for key in report.records.keys():
            if not (key in self.records):
                self.records[key] = []
            self.records[key].extend(report.records[key])
