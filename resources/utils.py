from flask import jsonify
import boto3
import random
from botocore.exceptions import ClientError

class Utils:
    def make_error(self, status_code, message, action):
        response = jsonify({
            'status': status_code,
            'message': message,
            'action': action
        })
        return response

    def generateUniqueBannerIds(self, currentIds, numbersToAdd):
        outputIds = []
        for x in range(0, numbersToAdd):
            while True:
                randomNo = random.randint(100, 500)
                if randomNo in currentIds:
                    pass
                else:
                    outputIds.append(randomNo)
                    break
        return [{'_id': id} for id in outputIds]

    def create_presigned_url(self, data):
        bucket_name = 'ba-banners'
        object_name = f'images/image_{data["_id"]}.png'
        expiration = 4000

        s3_client = boto3.client('s3')
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': bucket_name,
                                                                'Key': object_name},
                                                        ExpiresIn=expiration)
            data["url"] = response
            return data

        except ClientError as e:
            logging.error(e)
            return None





