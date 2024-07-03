import unittest
import os
from unittest.mock import Mock, MagicMock

from consts import DATE_FIELD
from parser.default_parser import RealEstateRawInfoParser
from test import read_file_data

TEST_DATA_FILENAME1 = os.path.join(os.path.dirname(__file__), "test_parser_input_no_city.html")
TEST_DATA_FILENAME2 = os.path.join(os.path.dirname(__file__), "test_parser_input_value_error.html")
CURRENT_YEAR = 2024
CURRENT_MONTH = 6


class RealEstateRawInfoParserTest(unittest.TestCase):

    def test_parser_no_city_name(self):
        config = Mock()
        config.get_current_year = MagicMock(return_value=CURRENT_YEAR)
        config.get_current_month = MagicMock(return_value=CURRENT_MONTH)

        unit = RealEstateRawInfoParser(config)
        report = unit.parse("одеса", 2024, read_file_data(TEST_DATA_FILENAME1))

        self.assertEqual(len(report.records.keys()), 7)
        self.assertEqual(len(report.records[DATE_FIELD]), 5)
        self.assertIn("одеса".capitalize(), report.records.keys())

    def test_parser_value_error(self):
        config = Mock()
        config.get_current_year = MagicMock(return_value=CURRENT_YEAR)
        config.get_current_month = MagicMock(return_value=CURRENT_MONTH)

        unit = RealEstateRawInfoParser(config)
        report = unit.parse("дніпропетровськ", 2018, read_file_data(TEST_DATA_FILENAME2))

        self.assertEqual(len(report.records.keys()), 10)
        self.assertEqual(len(report.records[DATE_FIELD]), 12)
        self.assertIn("дніпропетровськ".capitalize(), report.records.keys())


if __name__ == '__main__':
    unittest.main()
