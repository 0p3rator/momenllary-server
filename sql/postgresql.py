from functools import wraps
import psycopg2.pool
import psycopg2.extras
from time import time
from time import sleep
import sys
sys.path.append("..")
from mycolorlog import UseStyle
from conf.conf import postgresql as pgcfg

def Singleton(cls):
    _instance = {}
    @wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _singleton

@Singleton
class PostgreSql(object):
    __conn = None
    __cur = None
    def __init__(self):      
        self.__conn = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=20,
            dbname=pgcfg['dbname'],
            user=pgcfg['user'],
            password=pgcfg['password'], 
            host=pgcfg['host'], 
            port=pgcfg['port']
            )
        if self.__conn is None:
            print "error"

    def execute(self, queryString):
        #print queryString
        result_set = None
        conn = None
        try:
            conn = self.__conn.getconn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(queryString)
            result_set = cur.fetchall()
            cur.close()
            conn.commit()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print UseStyle(error, fore = 'red')
            raise Exception
        finally:
            if conn is not None:
                self.__conn.putconn(conn)
        return result_set

    def get_conn(self):
        con = self.__conn.getconn()
        return con

    def put_conn(self, connection):
        self.__conn.putconn(conn)

    def __del__(self):
        self.__conn.closeall()
    
    

if __name__ == '__main__':
    pg = PostgreSql()
    pg1 = PostgreSql()
    for i in range(1,5):
        try:        
            conn =  pg.get_conn()
            print conn
            cur = conn.cursor()
            cur.execute("select * from keyframes limit 2")
            result_set = cur.fetchall()
            #print result_set
            cur.close()
            #conn.commit()
            #pg.put_conn(conn)
        except (Exception, psycopg2.DatabaseError) as error:
            print "error in executing with exception: ",error