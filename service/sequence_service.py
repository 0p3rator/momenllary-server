import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
import json
import re
import copy
import transforms3d
import time
from mycolorlog import UseStyle
from sql.postgresql import PostgreSql
from mycolorlog import UseStyle
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
        
        per_query = int(per_page) + 1
        next_key = 0

        sql = ('select id, keyframes_id, ST_ASTEXT(geom) as geom from image_packets ' 
            'where geom && ST_SetSRID(ST_MakeBox2D(ST_Point({point1}), ST_Point({point2})), 4326) '
            'and image_packets.id >= {start_key} and keyframes_id is not null order by image_packets.id limit {per_page}').format(point1=point1, point2=point2, start_key=start_key, per_page=per_query)
        packets_result = self.__psql.execute(sql)
        ## per_query number of records are returned at one time. per_query + 1 and result[:-1] is used to panigation 
        if len(packets_result) == per_query:
            print('111')
            next_key = packets_result[-1]['id']
            packets_result = packets_result[:-1]
        print('NextKey:      ', next_key)
        final_result = self.__generate_features(packets_result)
        final_result['next_start_key'] = next_key        
        # #print features
        return final_result

    def __extract_loc(self, geom):
        indexstart = geom.find('(')
        indexend = geom.find(')')
        loc = geom[indexstart+1:indexend]
        loc = loc.split(',')
        loc = [i.split(' ')[:-1] for i in loc]
        return loc

    def __generate_features(self, packets_result):
        start_time = time.monotonic()
        result_features = copy.deepcopy(sequence_features.features)
        for packet_info in packets_result:
            temp_feature = copy.deepcopy(sequence_features.feature)
            geom_text = packet_info['geom']
            temp_feature['geometry']['coordinates'] = self.__extract_loc(geom_text)
            temp_feature['properties']['coordinateProperties']['image_keys'] = packet_info['keyframes_id']
            temp_feature['properties']['id'] = packet_info['id']
            temp_feature['properties']['key'] = packet_info['id']

            result_features['features'].append(temp_feature)

        print('TotalTime: ', time.monotonic() - start_time)

        return result_features

    def __query_single_packet(self, result, temp_results, packet_id):
        sql = 'select id, image_packet_id, ST_ASTEXT(geom) as geom, qw, qx, qy ,qz from keyframes where image_packet_id = {packet_id} order by filename'.format(packet_id=result['id'])
        keyframes_info = self.__psql.execute(sql)
        temp_results.append(keyframes_info)

if __name__ == '__main__':
    sf = SequenceFeature()
    sf.time = 10
    #print vars(SequenceFeature)
    #print "HELLO"
    #print SequenceFeature.__dict__
    #print SequenceFeature.to_json()