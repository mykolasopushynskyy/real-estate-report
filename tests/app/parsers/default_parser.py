import unittest
import os

from app.parsers.default_parser import RealEstateRawInfoParser

TEST_DATA_FILENAME = os.path.join(os.path.dirname(__file__), 'test_parser_input.html')

class RealEstateRawInfoParserTest(unittest.TestCase):

    def setUp(self):
        self.testfile = open(TEST_DATA_FILENAME, "rb")
        self.testdata = self.testfile.read()

    def tearDown(self):
        self.testfile.close()

    def test_parser(self):
        unit = RealEstateRawInfoParser()
        unit.parse(str(self.testdata))


if __name__ == '__main__':
    unittest.main()
