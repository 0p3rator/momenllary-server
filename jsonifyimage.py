import json
import copy
import psycopg2
import time
from transforms3d.euler import quat2euler
from transforms3d.quaternions import quat2mat
from transforms3d.euler import mat2euler
import numpy as np

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



