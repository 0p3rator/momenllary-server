# -*- coding: UTF-8 -*- 
import psycopg2
import time                    

# sql = """select plateno, timestamp from image_packets where timestamp \
# < '2018-02-05' and timestamp > '2017-11-30' order by timestamp"""
sql = """SELECT distinct (image_packets.plateno, image_packets.timestamp), image_packets.plateno, image_packets.timestamp from
image_packets left join keyframes on (keyframes.image_packet_id = image_packets.id) where
keyframes.geom && ST_SetSRID(ST_MakeBox2D(
    ST_Point(116.2597274780, 39.9905362994),
    ST_Point(116.5007400513, 39.8277861079)),4326) and timestamp > '2017-11-30' order by image_packets.timestamp"""

basedir = "/Users/wangchangyu/s3imagepacket-list/fourth-ring/"
try:
    conn = psycopg2.connect(dbname="map_data_origin", user="postgres", password="zuojingwei", host="mapeditor.momenta.works", port=5432)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    print "Connect Success"
    fo = open(basedir + "000.txt", "wb")
    i = 0
    j = 0
    for row in rows:
        print i
        if (i >= 100):
            if fo:
                fo.close()
                i = 0
                j = j+1
                filename = basedir + "%03d"%j + ".txt"
                print filename
                fo = open(filename, "wb")

        plateno = row[1]
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(row[2]), "%Y-%m-%d %H:%M:%S"))
        packetname = plateno + '-' + timestamp
        print packetname
        fo.write(packetname + '\n')

        i = i+1
    if fo:
        fo.close()
  # 
  
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close() 