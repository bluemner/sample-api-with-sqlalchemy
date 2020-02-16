""" Test Status Endpoint
"""
import unittest
from sample import settings
from sample.app import main


class TestStatusCollection(unittest.TestCase):
    """ Collection Class Test
    """

    @classmethod
    def setUpClass(cls):
        cls.api = main(UNIT_TEST =True).test_client()
        cls.url_prefix = settings.FLASK_URL_PREFIX
        return super().setUpClass()

    def test_get(self):
        """ Test Get method on Status
        """
        response = self.api.get(f'{self.url_prefix}/status')
        self.assertIsNotNone(response)
        self.assertAlmostEqual(response.status_code, 200)
