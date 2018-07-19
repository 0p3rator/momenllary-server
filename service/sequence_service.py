import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
import json
import re
import copy
import transforms3d
from mycolorlog import UseStyle
from sql.postgresql import PostgreSql
from mycolorlog import UseStyle
import threading
import conf.sequence_features as sequence_features

class SequenceService(object):
    def __init__(self):
        self.__psql = PostgreSql()
        pass

    def get_sequences(self, params):
        per_page = params.get('per_page')
        start_key = params.get('start_key')
        bbox = params.get('bbox')
        if not bbox:
            raise Exception('No bbox in params')
        
        bbox = bbox.split(',')
        point1 = ','.join(bbox[0:2])
        point2 = ','.join(bbox[2:4])
        if not start_key:
            start_key = 0
        
        per_query = long(per_page) + 1
        next_key = 0

        sql = ('select id from image_packets '
            'where geom && ST_SetSRID(ST_MakeBox2D(ST_Point({point1}), ST_Point({point2})), 4326) '
            'and id >= {start_key} order by id limit {per_page}').format(point1=point1, point2=point2, start_key=start_key, per_page=per_query)
        # sql = ('select keyframes.id as keyframe_id, ST_ASTEXT(keyframes.geom) as keyframe_geom, '
        #  'keyframes.qw, keyframes.qx, keyframes.qy, keyframes.qz, '
        #  'image_packets.id as packet_id, image_packets.timestamp, '
        #  'ST_ASTEXT(image_packets.geom) as packet_geom from '
        #  'image_packets left join keyframes on (image_packets.id = keyframes.image_packet_id) '
        #  'where keyframes.geom && ST_SetSRID(ST_MakeBox2D(ST_Point({point1}), ST_Point({point2})), 4326) ' 
        #  'and image_packets.id >= {start_key} order by keyframes.filename limit {per_page}').format(point1=point1, point2=point2, start_key=start_key, per_page=1000000000)
        result = self.__psql.execute(sql)
        ## per_query number of records are returned at one time. per_query + 1 and result[:-1] is used to panigation 
        if len(result) == per_query + 1:
            next_key = result[-1]['id']
            result = result[:-1]
        final_result = self.__generate_features(result)
        final_result['next_start_key'] = next_key        
        # print features
        return final_result

    def __extract_loc(self, position):
        indexstart = position.find('(')
        indexend = position.find(')')
        loc = position[indexstart+1:indexend]
        loc = loc.split(' ')[:2]
        return loc

    # def __generate_features(self, query_result):
    #     temp_features = {}
    #     result_features = copy.deepcopy(sequence_features.features)
    #     for result in query_result:
    #         temp_features[result['id']] = copy.deepcopy(sequence_features.feature)
    #         sql = 'select id, ST_ASTEXT(geom) as geom, qw, qx, qy ,qz from keyframes where image_packet_id = {packet_id}'.format(packet_id=result['id'])
    #         keyframes_info = self.__psql.execute(sql)
    #         for keyframe in keyframes_info:
    #             loc = self.__extract_loc(keyframe['geom'])
    #             # heading angle
    #             quanterion = [keyframe['qw'], keyframe['qx'], keyframe['qy'], keyframe['qz']]
    #             euler = transforms3d.euler.quat2euler(quanterion, 'sxyz')
    #             ca = euler[2] * 57.3
    #             temp_features[result['id']]['geometry']['coordinates'].append(loc)
    #             temp_features[result['id']]['properties']['coordinateProperties']['cas'].append(ca)
    #             temp_features[result['id']]['properties']['coordinateProperties']['image_keys'].append(keyframe['id'])
    #     for (key, value) in temp_features.items():
    #         result_features['features'].append(value)
    #     # print result_features
    #     return result_features

    def __generate_features(self, query_result):
        temp_features = {}
        result_features = copy.deepcopy(sequence_features.features)
        threads = []
        for result in query_result:
            thread = threading.Thread(target=self.__query_single_packet, args=(result, temp_features, result['id']))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        
        for (key, value) in temp_features.items():
            result_features['features'].append(value)
        # print result_features
        return result_features

    def __query_single_packet(self, result, temp_features, packet_id):
        temp_features[result['id']] = copy.deepcopy(sequence_features.feature)
        sql = 'select id, ST_ASTEXT(geom) as geom, qw, qx, qy ,qz from keyframes where image_packet_id = {packet_id} order by filename'.format(packet_id=result['id'])
        keyframes_info = self.__psql.execute(sql)
        for keyframe in keyframes_info:
            loc = self.__extract_loc(keyframe['geom'])
            # heading angle
            quanterion = [keyframe['qw'], keyframe['qx'], keyframe['qy'], keyframe['qz']]
            euler = transforms3d.euler.quat2euler(quanterion, 'sxyz')
            ca = euler[2] * 57.3
            temp_features[result['id']]['geometry']['coordinates'].append(loc)
            temp_features[result['id']]['properties']['coordinateProperties']['cas'].append(ca)
            temp_features[result['id']]['properties']['coordinateProperties']['image_keys'].append(keyframe['id'])
            temp_features[result['id']]['properties']['id'] = result['id']
            temp_features[result['id']]['properties']['key'] = result['id']


 
    # def __genreate_features(self, query_result):
    #     temp_features = {}
    #     result_features = copy.deepcopy(sequence_features.features)
    #     for result in query_result:
    #         if result['packet_id'] not in temp_features:
    #             temp_features[result['packet_id']] = copy.deepcopy(sequence_features.feature)
    #         print UseStyle((result['keyframe_geom']), fore='yellow')
    #         loc = self.__extract_loc(result['keyframe_geom'])
    #         # heading angle
    #         quanterion = [result['qw'], result['qx'], result['qy'], result['qz']]
    #         euler = transforms3d.euler.quat2euler(quanterion, 'sxyz')
    #         ca = euler[2] * 57.3
    #         temp_features[result['packet_id']]['geometry']['coordinates'].append(loc)
    #         temp_features[result['packet_id']]['properties']['coordinateProperties']['cas'].append(ca)
    #         temp_features[result['packet_id']]['properties']['coordinateProperties']['image_keys'].append(result['keyframe_id'])
    #     for (key, value) in temp_features.items():
    #         result_features['features'].append(value)
    #     # print result_features
    #     return result_features

            


if __name__ == '__main__':
    sf = SequenceFeature()
    sf.time = 10
    print vars(SequenceFeature)
    print "HELLO"
    print SequenceFeature.__dict__
    print SequenceFeature.to_json()