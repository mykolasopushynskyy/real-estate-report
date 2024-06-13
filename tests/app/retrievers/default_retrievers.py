import unittest
import appconfigs as appconfigs

from app.retrievers.default_retriever import RealEstateRawInfoRetriever


class RealEstateRawInfoRetrieverTest(unittest.TestCase):

    def test_retriever(self):
        config = appconfigs.AppConfigs()
        unit = RealEstateRawInfoRetriever(config)
        unit.retrieve(2003, 1)


if __name__ == '__main__':
    unittest.main()
