import unittest
import os
import argparse
from datetime import datetime
from unittest.mock import patch
from configs import AppConfigs, obfuscate_path, is_true_config, empty_or_else, PROJECT_DIR


class TestAppConfigs(unittest.TestCase):

    def setUp(self):
        self.cl_args = argparse.Namespace(
            cities=[],
            hide_districts=None
        )
        self.configs = AppConfigs(self.cl_args)

    def test_get_source_url(self):
        self.assertEqual(self.configs.get_source_url(), "http://www.svdevelopment.com/ua/web/flat_costs/")

    def test_get_cities_mappings(self):
        expected_cities_mappings = {"дніпропетровськ": "regs_719",
                                    "донецьк": "regs_459",
                                    "київ": "regs_2",
                                    "львів": "regs_248",
                                    "одеса": "regs_225",
                                    "харків": "regs_714"}
        self.assertEqual(self.configs.get_cities_mappings(), expected_cities_mappings)

    def test_get_cities(self):
        self.cl_args.cities = []
        self.assertEqual(self.configs.get_cities(),
                         ["київ", "дніпропетровськ", "донецьк", "львів", "одеса", "харків"])
        self.cl_args.cities = ["city1"]
        self.assertEqual(self.configs.get_cities(), ["city1"])

    def test_get_start_year(self):
        self.assertEqual(self.configs.get_start_year(), 2003)

    def test_get_inflation_adjustment_year(self):
        self.assertEqual(self.configs.get_inflation_adjustment_year(), 2003)

    def test_hide_districts(self):
        self.assertFalse(self.configs.hide_districts())

    def test_get_report_destination_folder(self):
        self.assertEqual(obfuscate_path(self.configs.get_report_destination_folder()), '<project_path>/reports')

    @patch('configs.datetime')
    def test_get_current_year(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2020, 1, 1)
        self.assertEqual(self.configs.get_current_year(), 2020)

    @patch('configs.datetime')
    def test_get_current_month(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2020, 2, 1)
        self.assertEqual(self.configs.get_current_month(), 2)


class TestUtilityFunctions(unittest.TestCase):
    def test_obfuscate_path(self):
        test_path = os.path.join(PROJECT_DIR, "some_folder")
        self.assertEqual(obfuscate_path(test_path), "<project_path>/some_folder")

    def test_is_true_config(self):
        self.assertTrue(is_true_config("true"))
        self.assertTrue(is_true_config("True"))
        self.assertTrue(is_true_config("yes"))
        self.assertTrue(is_true_config("Yes"))
        self.assertTrue(is_true_config("y"))
        self.assertTrue(is_true_config("Y"))
        self.assertFalse(is_true_config("false"))
        self.assertFalse(is_true_config("False"))

    def test_empty_or_else(self):
        self.assertEqual(empty_or_else(None, 'default'), 'default')
        self.assertEqual(empty_or_else('value', 'default'), 'value')


if __name__ == '__main__':
    unittest.main()
