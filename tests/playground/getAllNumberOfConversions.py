import pymongo
import os
from config import Config

config = Config()


res = config.clicksDB.aggregate([
    {'$lookup':
        {
            'from': 'conversions',
            'localField': '_id',
            'foreignField': 'click_id',
            'as': 'click_conversion'
        }
    },
    {'$unwind': '$click_conversion'},
    {'$group': {
        '_id': '$campaign_id', 'banners': {'$push': '$banner_id'}
    }
    }
    # {'$count': 'noOfRecords'},
])
# print(res)
# print(list(res)[0]['noOfRecords'])

for x in res:
    print(x)