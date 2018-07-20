import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
import json
import re
import copy
import transforms3d
from mycolorlog import UseStyle
from sql.postgresql11 import PostgreSql
from mycolorlog import UseStyle
import threading
import conf.sequence_features as sequence_features
import asyncpg
import asyncio
import time

class SequenceService(object):
    def __init__(self):
        self.__psql = PostgreSql()
        pass

    async def async_query(self):
       #pool = await asyncpg.create_pool(user='postgres', host='127.0.0.1', port=5433, password='zuojingwei', database='map_data_origin')
       con = await self.pool.acquire()
       try:
           result = await con.fetch('select * from keyframes limit 10')
           print(result)
       finally:
           await self.pool.release(con)
    
   # def execute(self):
   #     asyncio.get_event_loop().run_until_complete(self.async_query())
   
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

        sql = ('select id from image_packets '
            'where geom && ST_SetSRID(ST_MakeBox2D(ST_Point({point1}), ST_Point({point2})), 4326) '
            'and id >= {start_key} order by id limit {per_page}').format(point1=point1, point2=point2, start_key=start_key, per_page=per_query)
        result = self.__psql.execute(sql)

        ## per_query number of records are returned at one time. per_query + 1 and result[:-1] is used to panigation 
        if len(result) == per_query + 1:
            next_key = result[-1]['id']
            result = result[:-1]
        
        start_time = time.monotonic()
       # final_result = self.__psql.loop.run_until_complete(self.async_query(result))
        final_result = self.__generate_features(result)
        timecost = time.monotonic() - start_time
        print('timecost:', timecost)
        final_result['next_start_key'] = next_key        
        # #print features
        return final_result

    def __extract_loc(self, position):
        indexstart = position.find('(')
        indexend = position.find(')')
        loc = position[indexstart+1:indexend]
        loc = loc.split(' ')[:2]
        return loc

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
        # #print result_features
        return result_features

    async def async_query(self, query_result):
        temp_features = {}
        for result in query_result:
            temp_features[result['id']] = copy.deepcopy(sequence_features.feature)
            async with self.__psql.pool.acquire() as con:
                sql = 'select id, ST_ASTEXT(geom) as geom, qw, qx, qy ,qz from keyframes where image_packet_id = {packet_id} order by filename'.format(packet_id=result['id'])
                keyframes_info = await con.fetch(sql)
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
        return temp_features


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
    
async def async_query():
    pool = await asyncpg.create_pool(user='postgres', host='127.0.0.1', port=5433, password='zuojingwei', database='map_data_origin')
    con = await pool.acquire()
    try:
        result = await con.fetch('select * from keyframes limit 10')
        print(result)
    finally:
        await pool.release(con)
    #return result

if __name__ == '__main__':
    sf = SequenceService()
    #sf.execute()
  #  newloop = asyncio.new_event_loop()
  #  asyncio.set_event_loop(newloop)
  #  newloop.run_until_complete(sf.async_query())
    print("hello")
    result = asyncio.get_event_loop().run_until_complete(async_query())
    print(result)