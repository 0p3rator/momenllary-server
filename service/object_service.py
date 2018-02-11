# -*- coding: UTF-8 -*- 
feature = {
  "type": "Feature",
  "properties": {
    "accuracy": 0.044385486,
    "altitude": 3.2112074,
    "detections": [
      {
        "detection_key": "s6lae5eb1jkq4mijn7mcpof20f",
        "image_key": "NfqrXCDU5LXJkQjbH-NcJw"
      },
      {
        "detection_key": "5ama6jr36p20pkj40b04h163gr",
        "image_key": "9KiEc19-5OhVfUrCU_KfFg"
      },
      {
        "detection_key": "f9v356htr6btqhfqjdji4np3lp",
        "image_key": "Mll86Bsy7fVkoTUzTp34ug"
      }
    ],
    "first_seen_at": "2017-09-28T07:10:01.707Z",
    "key": "mkdoc8tkspvrqvfuv4gl2w9a1y",
    "last_seen_at": "2017-09-28T07:10:09.714Z",
    "package": "trafficsign",
    "updated_at": "2017-11-05T15:20:54.601Z",
    "value": "regulatory--no-u-turn--g1"
  },
  "geometry": {
    "type": "Point",
    "coordinates": [116.37815394327195,39.89526087222983]
  }
}
import json
import sys
sys.path.append("..")
import osmapi.QueryArea as QueryArea
import psycopg2
import time

a = json.dumps(QueryArea.queryArea(116.630, 40.273, 116.635, 40.275))
def get_objects(bbox):
    try:
        #conn = psycopg2.connect(database = 'postgres', user = "postgres", password = "hdmap430", host = "172.16.10.49")
        conn = psycopg2.connect(dbname="map_data_origin", user="postgres", password="zuojingwei", host="mapeditor.momenta.works", port=5432)
        cur = conn.cursor() 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    #objects = QueryArea.queryArea(bbox[0],bbox[1],bbox[2],bbox[3])
    objects = QueryArea.queryArea(116.630, 40.273, 116.635, 40.275)["boards"]
    for obj in objects:
        feature["properties"]["key"] = obj["messageId"]
        for observer in obj["observers"]:
            plateno = observer["basic_info_id"][:2]
            timestamp = observer["basic_info_id"][3:]
            local_str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(timestamp, "%Y-%m-%d-%H-%M-%S"))
            sql = """select id from image_packets where plateno = '{}' and timestamp = '{}' """.format(plateno,local_str_time)
            print sql
            #查询数据库，读取对应image_packet_id
            image_packet_id = 0
            try:
                cur.execute(sql)
                row = cur.fetchone()
                image_packet_id  = row[0]
                print "image_packets_id: " ,image_packet_id
            except(Exception,psycopg2.DatabaseError) as error:
                print(error)
            keyframesStr = ''
            keyframes = []
            for keyframe in observer["observers"]:
                keyframesStr = keyframesStr + '\'' + keyframe[0] + '\'' + ','
                keyframes.append('\'' + keyframe[0] + '\'')
            #keyframesStr = '(' + keyframesStr + ')'
            keyframesStr = ','.join(keyframes)
            keyframesStr = '(' + keyframesStr + ')'


            sql = """select id from keyframes_test where image_packet_id = {} and \
            filename in {} """.format(image_packet_id,keyframesStr)
            print sql
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                print row[0]
        #feature["properties"]["detections"].push

    cur.close()
    conn.close()
    return objects

if __name__=="__main__":
  print json.dumps(QueryArea.queryArea(116.630, 40.273, 116.635, 40.275))