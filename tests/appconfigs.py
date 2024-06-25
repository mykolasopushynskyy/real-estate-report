import argparse
import unittest
from configs import AppConfigs


class ConfigsTestCase(unittest.TestCase):
    def test_configs_read(self):
        cl_args = argparse.Namespace()
        unit = AppConfigs(cl_args)
        self.assertIsNotNone(unit)
        self.assertIsNotNone(unit.get_source_url())


if __name__ == '__main__':
    unittest.main()
