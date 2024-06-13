import unittest
from appconfigs import AppConfigs


class ConfigsTestCase(unittest.TestCase):
    def test_configs_read(self):
        configs = AppConfigs()
        self.assertIsNotNone(configs)
        self.assertIsNotNone(configs.get_source_url())


if __name__ == '__main__':
    unittest.main()
