from functools import wraps
import psycopg2.pool
import psycopg2.extras
import time as time
import sys
sys.path.append("..")
from mycolorlog import UseStyle
from conf.conf import postgresql as pgcfg
import asyncio
import asyncpg
import threading

def log_query(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start_time = time.time()
        print("The querystring is:", args[1])
        run = func(*args,**kwargs)
        end_time = time.time()
        print(UseStyle(('Query time cost is: ', end_time - start_time), fore='yellow'))
        return run
    return wrap

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
    __pool = None
    __cur = None
    def __init__(self):      
        self.__loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__loop)
        self.__pool = self.__loop.run_until_complete(asyncpg.create_pool(
            min_size=1,
            max_size=100,
            database=pgcfg['dbname'],
            user=pgcfg['user'],
            password=pgcfg['password'], 
            host=pgcfg['host'], 
            port=pgcfg['port']
            ))
        if self.__pool is None:
            print("error")
   
    async def __execute(self, sql):
        con = await self.__pool.acquire()
        result = await con.fetch(sql)
        return result

    @log_query
    def execute(self, queryString):
        print('Thread Name', threading.currentThread().getName())
        try:
            asyncio.get_event_loop()
        except RuntimeError:    
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
        #    result = new_loop.run_until_complete(self.__execute(queryString))
        result = self.__loop.run_until_complete(self.__execute(queryString))
        #result = asyncio.get_event_loop().run_until_complete(self.__execute(queryString))
        return result

    @property
    def loop(self):
        return self.__loop

    @property
    def pool(self):
        return self.__pool

    def __del__(self):
        self.__pool.terminate()

if __name__ == '__main__':
    pg = PostgreSql()
    result = pg.execute('select * from keyframes limit 2')
    print("hello")
    print(result)