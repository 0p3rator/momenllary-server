import boto3
session = boto3.session.Session()
s3 = session.client(endpoint_url='http://172.16.10.230:80', aws_access_key_id='2AOP8OZF6542K3ROFD5P',
                    aws_secret_access_key='gR8j2IssVJKm90XWEgz421aispgdQ1Ph8EYIQ59x', service_name='s3')


def get_jpg(m):
    s3.download_file('momenta-hdmap' , m, 'hello.jpg')

#get_jpg('map-data/B9-2017-12-06-15-23-30/keyframes/images/1512545011333.jpg')
def create_presigned_url(bucket, key):
    presigned_url = s3.generate_presigned_url(
        'get_object', Params={'Bucket': bucket, 'Key': key})
    return presigned_url



print create_presigned_url('momenta-hdmap','map-data/B6-2017-12-13-11-59-32/keyframes/json_lane/1513137572365.json')
