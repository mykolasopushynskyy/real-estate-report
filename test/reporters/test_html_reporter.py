import os
import re
import unittest
from unittest.mock import Mock, MagicMock

from reporter.html_reporter import brighter_color, ColorIterator, RealEstateHTMLReporter, get_report_file_path
from test import read_file_data

DATA_FILE = os.path.join(os.path.dirname(__file__), "львів-06-2024.csv")
EXPECTED_REPORT_FILE = os.path.join(os.path.dirname(__file__), "львів-06-2024-expected.html")
ACTUAL_REPORT_FILE = os.path.join(os.path.dirname(__file__), "львів-06-2024.html")

CITY = "львів"
EXPECTED_REPORT = read_file_data(EXPECTED_REPORT_FILE, encoding="utf-8")
DISTRICTS = ["Львів", "Галицкий", "Залізничний", "Личаківський", "Сихівський", "Франківський", "Шевченківський"]


def replace_plotly_uuid(text: str):
    hash_id = re.search(r'div id="([a-f0-9\-]{36})"', text).group(1)
    return text.replace(hash_id, "dummy-id")


class TestBrighterColor(unittest.TestCase):
    def test_brighter_color(self):
        self.assertEqual(brighter_color("#4421af"), "#816ac9")
        self.assertEqual(brighter_color("#000000"), "#545454")
        self.assertEqual(brighter_color("#ffffff"), "#ffffff")


class TestColorIterator(unittest.TestCase):
    def setUp(self):
        self.color_iterator = ColorIterator()

    def test_iter(self):
        iterator = iter(self.color_iterator)
        self.assertEqual(next(iterator), {'dark': '#4421af', 'bright': '#816ac9'})
        self.assertEqual(next(iterator), {'dark': '#ea5545', 'bright': '#f08d82'})
        self.assertEqual(next(iterator), {'dark': '#f46a9b', 'bright': '#f79bbc'})


class TestRealEstateHTMLReporter(unittest.TestCase):

    def test_generate_report(self):
        config = Mock()
        config.hide_districts = MagicMock(return_value=False)
        unit = RealEstateHTMLReporter(config)

        report_file = unit.generate_report(CITY, DISTRICTS, DATA_FILE)

        actual_report = read_file_data(ACTUAL_REPORT_FILE, encoding="utf-8")
        self.assertEqual(report_file, ACTUAL_REPORT_FILE)
        self.assertEqual(replace_plotly_uuid(actual_report), replace_plotly_uuid(EXPECTED_REPORT))

    def tearDown(self):
        if os.path.exists(ACTUAL_REPORT_FILE):
            os.remove(ACTUAL_REPORT_FILE)


if __name__ == '__main__':
    unittest.main()
