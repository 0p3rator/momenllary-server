import psycopg2
import conf.conf as config


def createConnection(database=config.db_databaseName,user=config.db_username,password=config.db_password,host=config.db_host):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host)
    return conn;

def closeConnection(connection):
    connection.close()

def closeCur(cur):
    cur.close()