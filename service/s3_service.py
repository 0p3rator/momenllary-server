import boto3
import sys
sys.path.append('..')
from conf.conf import s3 as s3cfg


session = boto3.session.Session()
s3 = session.client('s3','cn-north-1', endpoint_url=s3cfg['host'], aws_access_key_id=s3cfg['key'],
                    aws_secret_access_key=s3cfg['secret'])

class S3Service(object):
    def __init__(self):
        self.__name = ''

    def create_presigned_url(self,bucket, key):
        presigned_url = s3.generate_presigned_url(
            'get_object', Params={'Bucket': bucket, 'Key': key})
        return presigned_url

    def download(self, bucket, key, localpath):
        s3.download_file(bucket, key, localpath)

if __name__ == '__main__':
    s3client = S3Service()
    s3client.download('momenta-hdmap', 'map-data/B5-2018-03-03-16-26-49/keyframes/images/1520066509889.jpg', '/data/project/momenllary-server/test.jpg')
    print s3client.create_presigned_url('momenta-hdmap', 'map-data/B5-2018-03-03-16-26-49/keyframes/images/1520066509889.jpg')