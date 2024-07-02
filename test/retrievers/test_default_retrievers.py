import unittest
from unittest.mock import MagicMock, Mock

import responses

from retrievers.default_retriever import RealEstateRawInfoRetriever

TEST_DATA = "<html></html>"
TEST_URL = "http://www.svdevelopment.com/ua/web/flat_costs/"


class RealEstateRawInfoRetrieverTest(unittest.TestCase):
    @responses.activate
    def test_retriever(self):
        responses.add(responses.POST, TEST_URL, TEST_DATA, status=200)
        config = Mock()
        config.get_source_url = MagicMock(return_value=TEST_URL)

        unit = RealEstateRawInfoRetriever(config)
        text = unit.retrieve("львів", 2003)

        self.assertIsNotNone(text)
        self.assertEqual(text, TEST_DATA)


if __name__ == '__main__':
    unittest.main()
