import pymongo
import os
from config import Config

config = Config()

res = config.clicksDB.aggregate([
    {'$match':
         {'campaign_id': 5},
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
            'countOfBanners': {'$sum': 1},
            'sumOfRevenue': {'$sum': '$click_conversion.revenue'}
        }
    },
    # {'$count': 'noOfRecords'},
])
# print(res)
# print(list(res)[0]['noOfRecords'])

# for x in res:
#     print(x)
#
l = [x for x in res]

for x in l:
    print(x)

print(len(l))
