import psycopg2
from shapely.geometry import Point
from shapely.wkb import loads

point = Point(116,50,10)
print point
print(point.wkt)


sql1 = """insert into keyframes (filename, image_packet_id, qw, qx, qy, qz, geom) "
                    "VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))"""
                    

#try:
#   conn = psycopg2.connect(database = 'postgres', user = "postgres", password = "hdmap430", host = "10.2.129.4")
#except:
#    print("Connect to the database fail")

print("Connect Success!")


https = "https://a.mapillary.com/v3/sequences?bbox=116.3671875%2C39.8928799002948%2C116.38916015624999%2C39.90973623453719&client_id=NzNRM2otQkR2SHJzaXJmNmdQWVQ0dzo1ZWYyMmYwNjdmNDdlNmVi&page=0&per_page=1000"
indexStart = https.find('=')
indexEnd = https.find('&')
bbox = https[indexStart+1:indexEnd]
point1 = ", ".join(bbox.split('%2C')[0:2])
point2 = ", ".join(bbox.split('%2C')[2:4])

sql = """SELECT * from keyframes where geom && ST_SetSRID(\
ST_MakeBox2D(ST_Point({}),ST_Point({})),4326)""".format(point1,point2)


s1 = "SELECT * FROM {table_name} WHERE the_geom && ST_SetSRID(ST_MakeBox2D(ST_Point(-73.9980, 40.726), ST_Point(-73.995, 40.723)), 4326)"

print(bbox)
print(point1)
print(point2)
print sql