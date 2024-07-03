import unittest
from unittest.mock import MagicMock, Mock

import responses

from retriever.default_retriever import RealEstateRawInfoRetriever

TEST_DATA = "<html></html>"
TEST_URL = "http://www.svdevelopment.com/ua/web/flat_costs/"
CITIES_MAPPINGS = dict(
    київ="regs_2",
    дніпропетровськ="regs_719",
    донецьк="regs_459",
    львів="regs_248",
    одеса="regs_225",
    харків="regs_714"
)


class RealEstateRawInfoRetrieverTest(unittest.TestCase):
    @responses.activate
    def test_retriever(self):
        responses.add(responses.POST, TEST_URL, TEST_DATA, status=200)
        config = Mock()
        config.get_source_url = MagicMock(return_value=TEST_URL)
        config.get_cities_mappings = MagicMock(return_value=CITIES_MAPPINGS)

        unit = RealEstateRawInfoRetriever(config)
        text = unit.retrieve("львів", 2003)

        self.assertIsNotNone(text)
        self.assertEqual(text, TEST_DATA)


if __name__ == '__main__':
    unittest.main()
