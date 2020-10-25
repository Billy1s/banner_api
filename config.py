import pymongo
import os


class Config:

    def __init__(self):
        self.db = self._createDBConnection()
        self.clicksDB = self.db['clicks']
        self.impressionsDB = self.db['impressions']
        self.conversionsDB = self.db['conversions']

    def _createDBConnection(self):
        mongoUser = os.environ['mongoUser']
        mongoPassword = os.environ['mongoPassword']
        client = pymongo.MongoClient(
            f"mongodb+srv://{mongoUser}:{mongoPassword}@cluster0.bbz2d.mongodb.net/db1?retryWrites=true&w=majority")
        return client['db1']
