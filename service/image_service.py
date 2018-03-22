
import json
import copy
import psycopg2
import time
from transforms3d.euler import quat2euler
from transforms3d.quaternions import quat2mat
from transforms3d.euler import mat2euler
import numpy as np
import sys
import re
sys.path.append("..")
from mycolorlog import UseStyle

feature = {
'type' : 'Feature',
'properties' : {
    'ca' : '180',
    'camera_make': 'momenta_car_cam',
    'camera_model' : 'GreyPoint',
    'captured_at' :'',
    'key' : 'EXQOjnY4yqX7JsnXcgl0iw', 
    'pano' : False,
    'user_key' : 'Momenta666',
    'username' : 'changyu'  
    },
'geometry' : {
    'type' : 'Point',
    'coordinates' : []
    }
}

class ImageService(object):
    def __init__(self):
        self.__matConvert = np.array([1, 0, 0, 0, 0, 1, 0, -1, 0]).reshape(3,3)

    def get_images(self, params, bbox):
        conn = None

        
        perPage = params.get('per_page')
        startKey = params.get('start_key')
        image_packet = params.get('image_packet')
        print image_packet
        image_packet_filter = ""
        if (image_packet is None):
            image_packet_filter = ""
        else:
            image_packet_filter = self.__extract_image_packet(image_packet)
        if not startKey:
            startKey = 0

        perQuery = long(perPage) + 1

        FeatureCollection = {
        'type' : 'FeatureCollection',
        'features' : []
        }
        point1 = ", ".join(bbox[0:2])
        point2 = ", ".join(bbox[2:4])
        sql = """SELECT keyframes.image_packet_id, keyframes.filename, ST_AsText(keyframes.geom), image_packets.plateno, \
    image_packets.timestamp, keyframes.qw, keyframes.qx, keyframes.qy, keyframes.qz, keyframes.id \
    from keyframes left join image_packets \
    on (keyframes.image_packet_id = image_packets.id) where keyframes.geom && ST_SetSRID(\
    ST_MakeBox2D(ST_Point({}),ST_Point({})),4326) {} and keyframes.id >= {} order by keyframes.id limit {}\
    """.format(point1, point2, image_packet_filter, startKey, perQuery)
        print sql
        try:
            #conn = psycopg2.connect(database = 'postgres', user = "postgres", password = "hdmap430", host = "172.16.10.49")
            starttime = time.clock()
            conn = psycopg2.connect(dbname="map_data_origin", user="postgres", password="zuojingwei", host="mapeditor.momenta.works", port=5432)
            connecttime = time.clock()
            cur = conn.cursor()     
            cur.execute(sql)
            rows = cur.fetchall()
            querytime = time.clock()

            print UseStyle(("Connect time = " ,connecttime - starttime), fore = 'yellow')
            print UseStyle(("Querytime = ", querytime - connecttime), fore = 'yellow')

            nextStartKey = 0
            #print("The number of parts: ", cur.rowcount)
            if len(rows) == perQuery:
                nextStartKey = rows[-1][9]
                rows = rows[:-1]
            FeatureCollection['next_start_key'] = nextStartKey

            for row in rows:
                FeatureCollection["features"].append(copy.deepcopy(self.__extract_feature(row)))

        except (Exception, psycopg2.DatabaseError) as error:
            print UseStyle(error, fore = 'red')
        finally:
            if conn is not None:
                conn.close() 
        return FeatureCollection

    
    def __extract_loc(self, position):
        indexstart = position.find('(')
        indexend = position.find(')')
        loc = position[indexstart+1:indexend]
        loc = loc.split(' ')[:2]
        return loc

    def __extract_image_packet(self, image_packets):
        reResult = re.search('^B[0-9]-20[0-9]{2}-', image_packets, re.M|re.I)
        if(not reResult):
            return ""
        else:            
            image_packets_arr = image_packets.split(' ')
            print image_packets_arr
            plateno = reduce(self.__remove_repeat, map(lambda x: x[0:2],image_packets_arr))
            print plateno
            timestamp_arr = map(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(x[3:], "%Y-%m-%d-%H-%M-%S")), image_packets_arr)
            timestamp = reduce(lambda x, y: x + "', '" + y  , timestamp_arr)
            print """and plateno in ('{}') and timestamp in ('{}')""".format(plateno, timestamp)
            return """and plateno in ('{}') and timestamp in ('{}')""".format(plateno, timestamp)

    def __remove_repeat(self,x,y):
        if y not in x:
            return x + "', '" + y
        else:
            return x


    #generate feature according to the sql record
    def __extract_feature(self, row):
        loc = self.__extract_loc(row[2])
        filename = row[1]
        timestamp = int(filename)
        local_str_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(row[4]), "%Y-%m-%d %H:%M:%S"))
        imagekey = row[3] + '-' 
        imagekey += local_str_time + '/keyframes/images/' + filename + '.jpg'
        imagekey = row[9]
        ##calculate euler rotation from quanternion
        quanternion = map(lambda x:float(x),row[5:9])
        matTemp = quat2mat(quanternion)
        matTemp = self.__matConvert.dot(matTemp)
        eulerTemp = mat2euler(matTemp,"sxyz")
        ca = eulerTemp[2] * 57.3

        #ca = quat2euler(quanternion,"szyx")[2] * 57.3 * -1
        feature["properties"]["ca"] = str(ca)
        feature["properties"]["key"] = imagekey 
        feature["properties"]["captured_at"] = local_str_time
        feature["properties"]["username"] = row[3]
        feature["geometry"]["coordinates"] = copy.deepcopy(loc)
        return feature

    

class Kls(object):
    def __init__(self, data):
        self.data = data

    def printd(self):
        print(self.data)

if __name__ == '__main__':
    iss = ImageService()
    #iss.remove_repeat('B5', 'B6')
    #iss.extract_image_packet("B5-2017-12-01-15-30-10")
    #iss.get_images([u'116.47705078125003', u'39.92658842190944', u'116.49902343750003', u'39.9434364619742'])
