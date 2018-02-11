import json
import copy
import psycopg2
import time
from transforms3d.euler import quat2euler
import numpy as np

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

def extract_loc(position):
    indexstart = position.find('(')
    indexend = position.find(')')
    loc = position[indexstart+1:indexend]
    loc = loc.split(' ')[:2]
    return loc

def jsonify_image(bbox):
    conn = None
    FeatureCollection = {
    'type' : 'FeatureCollection',
    'features' : []
    }
    #print bbox
    point1 = ", ".join(bbox[0:2])
    point2 = ", ".join(bbox[2:4])
    sql = """SELECT keyframes.image_packet_id, keyframes.filename, ST_AsText(keyframes.geom), image_packets.plateno, \
image_packets.timestamp, keyframes.qw, keyframes.qx, keyframes.qy, keyframes.qz, keyframes.id \
from keyframes left join image_packets \
on (keyframes.image_packet_id = image_packets.id) where keyframes.geom && ST_SetSRID(\
ST_MakeBox2D(ST_Point({}),ST_Point({})),4326)\
""".format(point1,point2)
    print sql
    try:
        #conn = psycopg2.connect(database = 'postgres', user = "postgres", password = "hdmap430", host = "172.16.10.49")
        conn = psycopg2.connect(dbname="map_data_origin", user="postgres", password="zuojingwei", host="mapeditor.momenta.works", port=5432)
        cur = conn.cursor()     
        cur.execute(sql)
        rows = cur.fetchall()
        #print("The number of parts: ", cur.rowcount)
        for row in rows:
            loc = extract_loc(row[2])
            filename = row[1]
            timestamp = int(filename)
            local_str_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(row[4]), "%Y-%m-%d %H:%M:%S"))
            imagekey = row[3] + '-' 
            imagekey += local_str_time + '/keyframes/images/' + filename + '.jpg'
            imagekey = row[9]
            print imagekey
            #print imagekey
            #print "loc:" 
            #print loc
            ##calculate euler rotation from quanternion
            quanternion = map(lambda x:float(x),row[5:9])
            ca = quat2euler(quanternion)[2] * 57.3
            feature["properties"]["ca"] = str(ca)
            feature["properties"]["key"] = imagekey
            feature["properties"]["captured_at"] = local_str_time
            feature["properties"]["username"] = row[3]
            feature["geometry"]["coordinates"] = copy.deepcopy(loc)
            FeatureCollection["features"].append(copy.deepcopy(feature))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close() 
    return FeatureCollection

def get_path(imageKey):
    conn = None
    imagePath = ''
    try:
        imagePacketNoReq = """select image_packet_id, filename from keyframes where id = {}""".format(imageKey)
        conn = psycopg2.connect(dbname="map_data_origin", user="postgres", password="zuojingwei", host="mapeditor.momenta.works", port=5432)
        cur = conn.cursor()     
        cur.execute(imagePacketNoReq)
        result = cur.fetchone()
        image_packet_id = result[0]
        filename = result[1]
        imagePacketDateReq = """select plateno, timestamp from image_packets where id = {}""".format(image_packet_id)
        cur.execute(imagePacketDateReq)
        result = cur.fetchone()
        plateno = result[0]
        timestamp = result[1]
        local_str_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S"))
        imagePath = plateno + '-' + local_str_time + '/keyframes/images/' + filename + '.jpg'
    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
    finally:
        if conn is not None:
            conn.close()
    return imagePath

extract_loc("POINT Z (116.373070834778 39.9542073456365 41.0559972521369)")


