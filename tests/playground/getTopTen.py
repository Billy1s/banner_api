import pymongo
import os
from config import Config
import datetime

print(datetime.datetime.now())

config = Config()

res = config.clicksDB.aggregate([
    {'$match':
         {'campaign_id': 23},
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
    {'$count': 'noOfRecords'},
])

if list(res)[0]['noOfRecords'] > 10:
    res2 = config.clicksDB.aggregate([
        {'$match':
             {'campaign_id': 23},
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
                # 'campaign_id': {'$first': '$campaign_id'},
                'totalRevenue': {'$sum': '$click_conversion.revenue'}
            }
        },
        {'$sort':
            {
                'totalRevenue': -1
            }
        },
        {'$limit': 10}
    ])

    for x in res2:
        print(x)

print(datetime.datetime.now())