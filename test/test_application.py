import unittest
import argparse
from unittest.mock import MagicMock, patch
from io import StringIO
from application import App, main


class TestApp(unittest.TestCase):
    def setUp(self):
        self.mock_args = argparse.Namespace(cities=['New York', 'Los Angeles'], hide_districts=None)

        # Mock dependencies
        self.mock_configs = MagicMock()
        self.mock_retriever = MagicMock()
        self.mock_parser = MagicMock()
        self.mock_html_reporter = MagicMock()
        self.mock_csv_reporter = MagicMock()

        # Create an instance of App with mocked dependencies
        self.app = App(self.mock_args)
        self.app.configs = self.mock_configs
        self.app.retriever = self.mock_retriever
        self.app.parser = self.mock_parser
        self.app.html_reporter = self.mock_html_reporter
        self.app.csv_reporter = self.mock_csv_reporter

    def test_generate_report_for_city(self):
        # Mock return values
        self.mock_configs.get_current_year.return_value = 2024
        self.mock_configs.get_start_year.return_value = 2003
        self.mock_configs.get_cities.return_value = ['New York']
        self.mock_configs.get_cities_mappings.return_value = {'New York': 'NY', 'Los Angeles': 'LA'}

        # Mock methods and attributes of ParsedReport
        mock_parsed_report = MagicMock()
        mock_parsed_report.records.keys.return_value = ['data1', 'data2']
        self.app.generate_report_for_city('New York')

        # Assert calls were made correctly
        self.assertEqual(self.mock_retriever.retrieve.call_count, 22)  # Assuming 22 years between 2003 and 2024
        self.assertEqual(self.mock_parser.parse.call_count, 22)
        self.assertEqual(self.mock_csv_reporter.generate_report.call_count, 1)
        self.assertEqual(self.mock_html_reporter.generate_report.call_count, 1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):
        # Mock return values
        self.mock_configs.get_cities.return_value = ['New York', 'Los Angeles']
        self.mock_configs.get_cities_mappings.return_value = {'New York': 'reg_0', 'Los Angeles': 'reg_1'}

        # Mock calls to generate_report_for_city
        self.app.generate_report_for_city = MagicMock()

        # Call main method
        main(self.app)

        # Assert output and calls were made correctly
        expected_output = "\nStarting price parsing for cities: ['Los Angeles', 'New York']\n\n"
        self.assertIn(expected_output, mock_stdout.getvalue())
        self.assertEqual(self.app.generate_report_for_city.call_count, 2)

    def test_main_raise_error(self):
        # Mock return values
        self.mock_configs.get_cities.return_value = ['Boston']
        self.mock_configs.get_cities_mappings.return_value = {'New York': 'reg_0', 'Los Angeles': 'reg_1'}

        # Mock calls to generate_report_for_city
        self.app.generate_report_for_city = MagicMock()

        # Call main method
        with self.assertRaises(ValueError) as context:
            main(self.app)
            self.assertEqual(str(context.exception), "Cities ['Boston'] are not allowed")


if __name__ == '__main__':
    unittest.main()
