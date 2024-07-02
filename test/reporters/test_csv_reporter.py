import unittest
from consts import DATE_FIELD
from parsed_report import ParsedReport
from unittest.mock import patch, MagicMock, mock_open, Mock, call
from reporter.csv_reporter import RealEstateCSVReporter

USER_DESTINATION_REPORT = "/user/destination/report"
INFLATION_ADJUSTMENT_YEAR = 2003
CURRENT_YEAR = 2024
CURRENT_MONTH = 1

PARSED_REPORT = ParsedReport()
PARSED_REPORT.append_column(DATE_FIELD, [
    "2003-01-01",
    "2004-02-02",
    "2005-03-03"
])
PARSED_REPORT.append_column("Львів", [1000, 1100, 1200])


class TestRealEstateCSVReporter(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open())
    def test_csv_write_file_successful(self, mock_open_file):
        config = Mock()
        config.get_report_destination_folder = MagicMock(return_value=USER_DESTINATION_REPORT)
        config.get_inflation_adjustment_year = MagicMock(return_value=INFLATION_ADJUSTMENT_YEAR)
        config.get_current_year = MagicMock(return_value=CURRENT_YEAR)
        config.get_current_month = MagicMock(return_value=CURRENT_MONTH)
        unit = RealEstateCSVReporter(config)

        unit.generate_report("львів", PARSED_REPORT)

        mock_open_file.assert_called_once_with(USER_DESTINATION_REPORT + "/львів-01-2024.csv", 'w')
        mock_open_file.return_value.__enter__().write.assert_has_calls(
            [call("Date,Львів,Львів інфл.\r\n"),
             call("2003-01-01,1000,1000\r\n"),
             call("2004-02-02,1100,1073\r\n"),
             call("2005-03-03,1200,1128\r\n")]
        )


if __name__ == '__main__':
    unittest.main()
