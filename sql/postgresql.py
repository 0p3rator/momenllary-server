import psycopg2
import conf.conf as conf
class PostgreSql:
    __conn = None
    __cur = None
    def __init__(self,dbname):
        self.__conn = psycopg2.connect(dbname="map_data_origin", user="postgres", password="zuojingwei", host="mapeditor.momenta.works", port=5432)
        self.__cur = conn.cursor()     
        
        self.__conn = psycopg2.connect(dbname=conf.db_databaseName, user=conf.db_username, password=conf.db_password, host=conf.db_host, port=conf.db_port)
    def Query(self,sqlstr):
        return __cur.execute(sqlstr)
    def __del__(self):
        self.__conn.close()