import boto3
import sys
sys.path.append('..')
from conf.conf import s3 as s3cfg


session = boto3.session.Session()
s3 = session.client(endpoint_url=s3cfg['host'], aws_access_key_id=s3cfg['key'],
                    aws_secret_access_key=s3cfg['secret'], service_name='s3')

class S3Service(object):
    def __init__(self):
        self.__name = ''

    def create_presigned_url(self,bucket, key):
        presigned_url = s3.generate_presigned_url(
            'get_object', Params={'Bucket': bucket, 'Key': key})
        return presigned_url

