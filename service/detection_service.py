import json
import re
import time
from s3_service import S3Service

import sys
sys.path.append('..')
from sql.postgresql import PostgreSql

class DetectionService(object):
    def __init__(self):
        self.__psql = PostgreSql()
        self.__s3Service = S3Service()

    def get_s3url(self, params):
        imageKey = params.get('imagekey')
        tagType = params.get('tag')
        
        #Get detection path
        path = self.__get_path(imageKey)
        
        #For IntrinsicMatrix
        if tagType is not None:

            if (tagType == 'IntrinsicMatrix'):
                path = re.sub('/images.*','/IntrinsicMatrix.json',path)
            #For json_lane, json_line, json_trafficsign, json_project(spSlam result)
            else:        
                path = path.replace('/images','/' + tagType)
                path = path.replace('.jpg','.json')
            
        path = 'map-data/' + path
        url = self.__s3Service.create_presigned_url('momenta-hdmap',path)
        return url

    def get_frame_location(self, imageKey):
        sqlString = """select ST_AsText(keyframes.geom) as point, image_packets.plateno, image_packets.timestamp \
         from keyframes left join image_packets on (keyframes.image_packet_id = image_packets.id) \
          where keyframes.id = {}""".format(imageKey)
        print sqlString
        result = self.__psql.execute(sqlString)[0]
        resultJson = {}
        plateno = result['plateno']
        timestamp = result['timestamp']
        resultJson['packet_name'] = plateno + '-' + 'local_str_time'

        patt = re.compile(r'[0-9][0-9\.\s]+')
        loc = patt.search(result['point']).group()
        resultJson['loc'] = loc
        return resultJson

    def get_packet_location(self, packetName):
        plateno = packetName[:2]
        timestamp = packetName[3:]
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(timestamp, "%Y-%m-%d-%H-%M-%S"))
        print timestamp
        sqlString = "select ST_AsText(keyframes.geom) \
        as point from keyframes where image_packet_id = (select id from image_packets where plateno = '{}' and timestamp = '{}')  \
        order by id".format(plateno, timestamp)
        print sqlString
        result = self.__psql.execute(sqlString)[0]
        resultJson = {}
        patt = re.compile(r'[0-9][0-9\.\s]+')
        loc = patt.search(result['point']).group()
        resultJson['loc'] = loc
        return resultJson


    def __get_path(self, imageKey):
        conn = None
        imagePath = ''
        sqlString = """select keyframes.filename, image_packets.plateno, image_packets.timestamp from keyframes \
             left join image_packets on (keyframes.image_packet_id = image_packets.id) where keyframes.id = {}""".format(imageKey)
            
        result = self.__psql.execute(sqlString)[0]
        plateno = result['plateno']
        timestamp = result['timestamp']
        filename = result['filename']
        local_str_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S"))
        imagePath = plateno + '-' + local_str_time + '/keyframes/images/' + filename + '.jpg'
        return imagePath

if __name__=='__main__':
    serDetection = DetectionService()
    serDetection.get_path(406675)