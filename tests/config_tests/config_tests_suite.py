import unittest
from resources.config import Config
from app import app



class TestSuiteConfig(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSuiteConfig, self).__init__(*args, **kwargs)
        self.app = app.test_client()
        self.config = Config(env='test')

    def test_checkCampaignIdClicks(self):
        dummyData = {'_id': 100, 'banner_id': 100, 'campaign_id': 200}
        self.config.db.drop_collection('clicks')
        self.config.clicksDB.insert_one(dummyData)
        result = self.config.checkCampaignId(200, 'clicks')
        x = [x for x in result][0]
        print(x)
        self.assertEqual(dummyData, x)

    def test_checkCampaignIdImpressions(self):
        dummyData = {'_id': 100, 'banner_id': 100, 'campaign_id': 200}
        self.config.db.drop_collection('impressions')
        self.config.impressionsDB.insert_one(dummyData)
        result = self.config.checkCampaignId(200, 'impressions')
        x = [x for x in result][0]
        self.assertEqual(dummyData, x)






if __name__ == '__main__':
    unittest.main()
