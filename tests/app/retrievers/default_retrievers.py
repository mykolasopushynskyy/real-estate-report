import unittest
import configs

from app.retrievers.default_retriever import RealEstateRawInfoRetriever


class RealEstateRawInfoRetrieverTest(unittest.TestCase):

    def test_retriever(self):
        config = configs.AppConfigs()
        unit = RealEstateRawInfoRetriever(config)
        unit.retrieve("львів", 2003)


if __name__ == '__main__':
    unittest.main()
