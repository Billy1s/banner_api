import pymongo
import os
from datetime import datetime

class Config:

    def __init__(self, env='dev'):
        self.db = self._createDBConnection(env)
        self.clicksDB = self.db['clicks']
        self.impressionsDB = self.db['impressions']
        self.conversionsDB = self.db['conversions']

    def _createDBConnection(self, env):
        mongoUser = os.environ['mongoUser']
        mongoPassword = os.environ['mongoPassword']
        client = pymongo.MongoClient(
            f"mongodb+srv://{mongoUser}:{mongoPassword}@cluster0.bbz2d.mongodb.net/db1?retryWrites=true&w=majority")
        db = client[env + '-' + 'db' + self.checkTimeQuarter()]
        return db

    def checkTimeQuarter(self):
        now = datetime.now()
        current_time = int(now.strftime("%M"))
        if current_time in range(0, 16):
            return '1'
        elif current_time in range(16, 31):
            return '2'
        elif current_time in range(31, 46):
            return '3'
        elif current_time in range(46, 61):
            return '4'
        else:
            return '1'


    def checkCampaignId(self, campaign_id, collection='impressions'):
        if collection == 'impressions':
            return self.impressionsDB.find({'campaign_id': campaign_id}).limit(1)
        elif collection == 'clicks':
            return self.clicksDB.find({'campaign_id': campaign_id}).limit(1)
        else:
            raise ValueError("Collection not recognised")


    def getCampaignBannerTopRevenue(self, campaign_id, limit=10):
        return self.clicksDB.aggregate([
            {'$match':
                 {'campaign_id': campaign_id},
             },
            {'$lookup':
                {
                    'from': 'conversions',
                    'localField': '_id',
                    'foreignField': 'click_id',
                    'as': 'click_conversion'
                }
            },
            {'$unwind': '$click_conversion'},
            {'$group':
                {
                    '_id': '$banner_id',
                    'totalRevenue': {'$sum': '$click_conversion.revenue'}
                }
            },
            {'$sort':
                {
                    'totalRevenue': -1
                }
            },
            {'$limit': limit}
        ])

    def getCampaignBannerTopClicks(self, campaign_id, limit=5):
        return self.clicksDB.aggregate([
            {'$match':
                 {'campaign_id': campaign_id},
             },
            {'$group':
                {
                    '_id': '$banner_id',
                    'totalClicks': {'$sum': 1}
                }
            },
            {'$sort':
                {
                    'totalClicks': -1
                }
            },
            {'$limit': limit}
        ])
