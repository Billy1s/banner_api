from flask import Flask, jsonify
from config import Config
from utils import Utils
from flask_cors import CORS, cross_origin
import random

config = Config()
utils = Utils()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({'hello': 'world'})


@app.route("/campaigns/<campaign_id>", methods=["GET"])
@cross_origin()
def campaignsById(campaign_id):
    try:
        id = int(campaign_id)
    except ValueError:
        return utils.make_error(500,
                                'campaign_id must be a int',
                                "Please try again with a int")

    results = config.clicksDB.aggregate([
        {'$match':
             {'campaign_id': id},
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
    unPackedResults = [utils.create_presigned_url(x) for x in results]

    random.shuffle(unPackedResults)

    if len(unPackedResults) < 1:
        return utils.make_error(400,
                                f'No results found for campaign_id: {id}',
                                'Please try another campaign_id'), 400

    return jsonify(unPackedResults)
