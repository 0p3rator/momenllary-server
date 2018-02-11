# -*- coding: UTF-8 -*- 
import psycopg2
import time                    

sql = """select plateno, timestamp from image_packets where timestamp \
< '2018-02-05' and timestamp > '2017-11-30' order by timestamp"""
try:
    conn = psycopg2.connect(dbname="map_data_origin", user="postgres", password="zuojingwei", host="mapeditor.momenta.works", port=5432)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    print "Connect Success"
    fo = open("/Users/wangchangyu/s3imagepacket-list/000.txt", "wb")
    i = 0
    j = 0
    for row in rows:
        print i
        if (i >= 40):
            if fo:
                fo.close()
                i = 0
                j = j+1
                filename = "/Users/wangchangyu/s3imagepacket-list/" + "%03d"%j + ".txt"
                print filename
                fo = open(filename, "wb")

        plateno = row[0]
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(row[1]), "%Y-%m-%d %H:%M:%S"))
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