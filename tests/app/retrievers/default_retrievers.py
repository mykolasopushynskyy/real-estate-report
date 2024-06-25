import argparse
import unittest
import configs

from app.retrievers.default_retriever import RealEstateRawInfoRetriever


class RealEstateRawInfoRetrieverTest(unittest.TestCase):
    def test_retriever(self):
        cl_args = argparse.Namespace()
        config = configs.AppConfigs(cl_args)
        unit = RealEstateRawInfoRetriever(config)
        text = unit.retrieve("львів", 2003)
        self.assertIsNotNone(text)


if __name__ == '__main__':
    unittest.main()
