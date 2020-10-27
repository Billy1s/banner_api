errors = {
    "InvalidIdEntered": {
        'status': 400,
        'message': 'campaign_id must be a int',
        'action': 'Please try again with a int'
    },
    "UnknownCampaignId": {
        'status': 400,
        'message': 'campaign_id could not be found',
        'action': 'Please try a different campaign_id'
    },
    "UnknownRoute": {
        'status': 404,
        'message': 'Route not known',
        'action': 'Please try a valid API endpointd'
    },

}
