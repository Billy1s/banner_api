from flask import Flask, jsonify
from resources.config import Config
from resources.utils import Utils
from flask_cors import CORS, cross_origin
from resources.errors import errors
import random

config = Config()
utils = Utils()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.errorhandler(404)
def not_found(e):
    return jsonify(errors['UnknownRoute']), 404

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({'hello': 'world'})


@app.route("/campaigns/<campaign_id>", methods=["GET"])
@cross_origin()
def campaignsById(campaign_id):
    try:
        id = int(campaign_id)
    except ValueError:
        return jsonify(errors['InvalidIdEntered']), 400

    # check campaign_id valid
    res = config.checkCampaignId(id, 'clicks')

    oneRecord = [x for x in res]

    if len(oneRecord) < 1:
        return jsonify(errors['UnknownCampaignId']), 400

    results = config.getCampaignBannerTopRevenue(id)

    # Unpack results and load path to s3 image
    unPackedResults = [utils.create_presigned_url(x) for x in results]

    random.shuffle(unPackedResults)

    unPackedResultsCount = len(unPackedResults)

    # X > 10 & X in range(5,10)
    if unPackedResultsCount >= 5:
        return jsonify(unPackedResults)
    # X in range(1,5)
    elif unPackedResultsCount in range(1, 5):
        topClickBannersToGet = 5 - unPackedResultsCount
        topClicksResults = config.getCampaignBannerTopClicks(id)
        topClicksUnPackedResults = [utils.create_presigned_url(x) for x in topClicksResults
                                    if x['_id'] not in [x['_id'] for x in unPackedResults]]
        bannersToReturn = unPackedResults + topClicksUnPackedResults[0:topClickBannersToGet]
        return jsonify(bannersToReturn)
    # X == 0
    elif unPackedResultsCount == 0:
        return campaignsByIdTopClicks(id)



@app.route("/campaigns/topclicks/<campaign_id>", methods=["GET"])
@cross_origin()
def campaignsByIdTopClicks(campaign_id):
    try:
        id = int(campaign_id)
    except ValueError:
        return jsonify(errors['InvalidIdEntered']), 400

    # check campaign_id valid
    res = config.checkCampaignId(id, 'clicks')
    oneRecord = [x for x in res]
    if len(oneRecord) < 1:
        return jsonify(errors['UnknownCampaignId']), 400

    results = config.getCampaignBannerTopClicks(id)

    unPackedResults = [utils.create_presigned_url(x) for x in results]

    random.shuffle(unPackedResults)

    # If less then 5 add random unique banners to make up to 5
    if len(unPackedResults) < 5:
        bannersToGet = 5 - len(unPackedResults)
        currentBanners = [x['_id'] for x in unPackedResults]
        newBannerIds = utils.generateUniqueBannerIds(currentBanners, bannersToGet)
        newBannersUnpacked = [utils.create_presigned_url(x) for x in newBannerIds]
        bannersToReturn = newBannersUnpacked + unPackedResults
        return jsonify(bannersToReturn)

    return jsonify(unPackedResults)
