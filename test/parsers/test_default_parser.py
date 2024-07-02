import unittest
import os

from parsers.default_parser import RealEstateRawInfoParser
from test import read_file_data

TEST_DATA_FILENAME1 = os.path.join(os.path.dirname(__file__), 'test_parser_input_no_city.html')
TEST_DATA_FILENAME2 = os.path.join(os.path.dirname(__file__), 'test_parser_input_value_error.html')


class RealEstateRawInfoParserTest(unittest.TestCase):

    def test_parser_no_city_name(self):
        unit = RealEstateRawInfoParser()
        report = unit.parse("одеса", 2024, read_file_data(TEST_DATA_FILENAME1))

        self.assertEqual(len(report.records.keys()), 7)
        self.assertIn("одеса".capitalize(), report.records.keys())

    def test_parser_value_error(self):
        unit = RealEstateRawInfoParser()
        report = unit.parse("дніпропетровськ", 2018, read_file_data(TEST_DATA_FILENAME2))

        self.assertEqual(len(report.records.keys()), 10)
        self.assertIn("дніпропетровськ".capitalize(), report.records.keys())


if __name__ == '__main__':
    unittest.main()
