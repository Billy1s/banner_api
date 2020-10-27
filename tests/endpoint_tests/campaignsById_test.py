import unittest
from resources.config import Config
from resources.errors import errors
import requests


class TestSuiteCampaignById(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSuiteCampaignById, self).__init__(*args, **kwargs)
        self.config = Config(env='test')

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

    # test for x >= 10
    def test_x_10(self):
        ''' test to check if more then 10 results it returns banners with the highest revenue '''
        self.config.db.drop_collection('clicks')
        self.config.db.drop_collection('conversions')

        dummyDataClicksToReturn = [{'_id': 101, 'banner_id': 201, 'campaign_id': 503},
                                   {'_id': 102, 'banner_id': 202, 'campaign_id': 503},
                                   {'_id': 103, 'banner_id': 203, 'campaign_id': 503},
                                   {'_id': 104, 'banner_id': 204, 'campaign_id': 503},
                                   {'_id': 105, 'banner_id': 205, 'campaign_id': 503},
                                   {'_id': 106, 'banner_id': 206, 'campaign_id': 503},
                                   {'_id': 107, 'banner_id': 207, 'campaign_id': 503},
                                   {'_id': 108, 'banner_id': 208, 'campaign_id': 503},
                                   {'_id': 109, 'banner_id': 209, 'campaign_id': 503},
                                   {'_id': 110, 'banner_id': 210, 'campaign_id': 503},
                                   ]
        dummyDataClicksFalse = [{'_id': 201, 'banner_id': 301, 'campaign_id': 503},
                                {'_id': 202, 'banner_id': 302, 'campaign_id': 503},
                                {'_id': 203, 'banner_id': 303, 'campaign_id': 503},
                                {'_id': 204, 'banner_id': 304, 'campaign_id': 503},
                                {'_id': 205, 'banner_id': 305, 'campaign_id': 503},
                                {'_id': 206, 'banner_id': 306, 'campaign_id': 503},
                                {'_id': 207, 'banner_id': 307, 'campaign_id': 503},
                                {'_id': 208, 'banner_id': 308, 'campaign_id': 503},
                                {'_id': 209, 'banner_id': 309, 'campaign_id': 503},
                                {'_id': 210, 'banner_id': 310, 'campaign_id': 503},
                                ]

        dummyDataconversionsToReturn = [{'_id': 101, 'click_id': 101, 'revenue': 5},
                                        {'_id': 102, 'click_id': 102, 'revenue': 5},
                                        {'_id': 103, 'click_id': 103, 'revenue': 5},
                                        {'_id': 104, 'click_id': 104, 'revenue': 5},
                                        {'_id': 105, 'click_id': 105, 'revenue': 5},
                                        {'_id': 106, 'click_id': 106, 'revenue': 5},
                                        {'_id': 107, 'click_id': 107, 'revenue': 5},
                                        {'_id': 108, 'click_id': 108, 'revenue': 5},
                                        {'_id': 109, 'click_id': 109, 'revenue': 5},
                                        {'_id': 110, 'click_id': 110, 'revenue': 5},
                                        ]
        dummyDataconversionsFalse = [{'_id': 201, 'click_id': 201, 'revenue': 1},
                                     {'_id': 202, 'click_id': 202, 'revenue': 1},
                                     {'_id': 203, 'click_id': 203, 'revenue': 1},
                                     {'_id': 204, 'click_id': 204, 'revenue': 1},
                                     {'_id': 205, 'click_id': 205, 'revenue': 1},
                                     {'_id': 206, 'click_id': 206, 'revenue': 1},
                                     {'_id': 207, 'click_id': 207, 'revenue': 1},
                                     {'_id': 208, 'click_id': 208, 'revenue': 1},
                                     {'_id': 209, 'click_id': 209, 'revenue': 1},
                                     {'_id': 210, 'click_id': 210, 'revenue': 1},
                                     ]

        self.config.clicksDB.insert_many(dummyDataClicksToReturn + dummyDataClicksFalse)
        self.config.conversionsDB.insert_many(dummyDataconversionsToReturn + dummyDataconversionsFalse)

        response = requests.get('http://localhost:5000/campaigns/503')
        data = response.json()

        for dummyData in dummyDataClicksToReturn:
            self.assertIn(dummyData['banner_id'], [x['_id'] for x in data])


    # test for x in range(5,10
    def test_x_5_10(self):
        ''' test to check if more then 10 results it returns banners with the highest revenue '''
        self.config.db.drop_collection('clicks')
        self.config.db.drop_collection('conversions')

        dummyDataClicksToReturn = [{'_id': 101, 'banner_id': 201, 'campaign_id': 503},
                                   {'_id': 102, 'banner_id': 202, 'campaign_id': 503},
                                   {'_id': 103, 'banner_id': 203, 'campaign_id': 503},
                                   {'_id': 104, 'banner_id': 204, 'campaign_id': 503},
                                   {'_id': 105, 'banner_id': 205, 'campaign_id': 503},
                                   {'_id': 106, 'banner_id': 206, 'campaign_id': 503},
                                   {'_id': 107, 'banner_id': 207, 'campaign_id': 503},
                                   ]

        dummyDataconversionsToReturn = [{'_id': 101, 'click_id': 101, 'revenue': 5},
                                        {'_id': 102, 'click_id': 102, 'revenue': 5},
                                        {'_id': 103, 'click_id': 103, 'revenue': 5},
                                        {'_id': 104, 'click_id': 104, 'revenue': 5},
                                        {'_id': 105, 'click_id': 105, 'revenue': 5},
                                        {'_id': 106, 'click_id': 106, 'revenue': 5},
                                        {'_id': 107, 'click_id': 107, 'revenue': 5},
                                        ]

        self.config.clicksDB.insert_many(dummyDataClicksToReturn)
        self.config.conversionsDB.insert_many(dummyDataconversionsToReturn)

        response = requests.get('http://localhost:5000/campaigns/503')
        data = response.json()

        for dummyData in dummyDataClicksToReturn:
            self.assertIn(dummyData['banner_id'], [x['_id'] for x in data])
        self.assertEqual(7, len(data))


    # test for x in range(1,5)
    def test_x_1_5(self):
        ''' Test to check if not enough data with revenue endpoint will get most clicks to make result up to 5 '''
        self.config.db.drop_collection('clicks')
        self.config.db.drop_collection('conversions')

        dummyDataClicks = [{'_id': 101, 'banner_id': 201, 'campaign_id': 503},
                           {'_id': 102, 'banner_id': 202, 'campaign_id': 503},
                           {'_id': 103, 'banner_id': 203, 'campaign_id': 503},
                           {'_id': 104, 'banner_id': 204, 'campaign_id': 503},
                           {'_id': 105, 'banner_id': 205, 'campaign_id': 503},
                           ]

        dummyDataconversions = [{'_id': 101, 'click_id': 101, 'revenue': 5},
                                {'_id': 102, 'click_id': 102, 'revenue': 2},
                                {'_id': 103, 'click_id': 103, 'revenue': 3},
                                ]
        self.config.clicksDB.insert_many(dummyDataClicks)
        self.config.conversionsDB.insert_many(dummyDataconversions)

        response = requests.get('http://localhost:5000/campaigns/503')
        data = response.json()

        for dummyData in dummyDataClicks:
            self.assertIn(dummyData['banner_id'], [x['_id'] for x in data])

    # test for x == 0
    def test_x_0(self):
        ''' Test to check if no revenue found return banners by clicks '''
        self.config.db.drop_collection('clicks')
        self.config.db.drop_collection('conversions')

        dummyDataClicks = [{'_id': 101, 'banner_id': 201, 'campaign_id': 503},
                           {'_id': 102, 'banner_id': 202, 'campaign_id': 503},
                           {'_id': 103, 'banner_id': 203, 'campaign_id': 503},
                           {'_id': 104, 'banner_id': 204, 'campaign_id': 503},
                           {'_id': 105, 'banner_id': 205, 'campaign_id': 503},
                           ]

        # dummyDataconversions = [{'_id': 101, 'click_id': 101, 'revenue': 5},
        #                         {'_id': 102, 'click_id': 102, 'revenue': 2},
        #                         {'_id': 103, 'click_id': 103, 'revenue': 3},
        #                         ]

        self.config.clicksDB.insert_many(dummyDataClicks)
        # self.config.conversionsDB.insert_many(dummyDataconversions)

        response = requests.get('http://localhost:5000/campaigns/503')
        data = response.json()

        for dummyData in dummyDataClicks:
            self.assertIn(dummyData['banner_id'], [x['_id'] for x in data])

    # test for x == 0
    def test_x_0(self):
        ''' Test to check if not enough banners by clicks it will add random to make collection up to 5 '''
        self.config.db.drop_collection('clicks')
        self.config.db.drop_collection('conversions')

        dummyDataClicks = [{'_id': 101, 'banner_id': 201, 'campaign_id': 503},
                           {'_id': 102, 'banner_id': 202, 'campaign_id': 503},
                           {'_id': 103, 'banner_id': 203, 'campaign_id': 503},
                           ]

        self.config.clicksDB.insert_many(dummyDataClicks)

        response = requests.get('http://localhost:5000/campaigns/503')
        data = response.json()

        self.assertEqual(5, len(data))





if __name__ == '__main__':
    unittest.main()
