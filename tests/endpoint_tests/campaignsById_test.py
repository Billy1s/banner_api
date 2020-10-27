import unittest
import json
from config import Config
from app import app
from resources.errors import errors
import requests


class TestSuiteCampaignById(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSuiteCampaignById, self).__init__(*args, **kwargs)
        self.app = app.test_client()
        self.config = Config()

    def test_searchCampaignByID(self):
        response = requests.get('http://localhost:5000/campaigns/1')
        data = response.json()

        for obj in data:
            keys = obj.keys()
            self.assertIn('_id', keys)
            self.assertIn('url', keys)

        self.assertEqual(200, response.status_code)

    def test_invalidInput(self):
        response = requests.get('http://localhost:5000/campaigns/y')
        data = response.json()

        self.assertEqual(errors['InvalidIdEntered'], data)
        self.assertEqual(400, response.status_code)

    def test_unknownCampaignId(self):
        response = requests.get('http://localhost:5000/campaigns/00000000')
        data = response.json()

        self.assertEqual(errors['UnknownCampaignId'], data)
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
