import unittest
import os

from app.parsers.default_parser import RealEstateRawInfoParser

TEST_DATA1_FILENAME = os.path.join(os.path.dirname(__file__), 'test_parser_input_no_city.html')
TEST_DATA2_FILENAME = os.path.join(os.path.dirname(__file__), 'test_parser_input_value_error.html')


class RealEstateRawInfoParserTest(unittest.TestCase):

    def setUp(self):
        self.testfile1 = open(TEST_DATA1_FILENAME, "rb")
        self.testdata1 = self.testfile1.read()
        self.testfile2 = open(TEST_DATA2_FILENAME, "rb")
        self.testdata2 = self.testfile2.read()

    def tearDown(self):
        self.testfile1.close()
        self.testfile2.close()

    def test_parser_no_city_name(self):
        unit = RealEstateRawInfoParser()
        report = unit.parse("одеса", 2024, str(self.testdata1))
        self.assertEqual(len(report.records.keys()), 7)

    def test_parser_value_error(self):
        unit = RealEstateRawInfoParser()
        report = unit.parse("дніпропетровськ", 2018, str(self.testdata2))
        self.assertEqual(len(report.records.keys()), 10)

if __name__ == '__main__':
    unittest.main()
