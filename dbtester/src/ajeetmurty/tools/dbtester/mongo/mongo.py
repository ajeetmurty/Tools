import os
import platform
import logging.config
import configparser
from pymongo import MongoClient
from datetime import datetime
import time
import random

logging.config.fileConfig('logging.conf')
logr = logging.getLogger('pylog')
config = configparser.ConfigParser()
config.read('config/mongodb_mongolab-test.ini')
MONGODB_URI = config.get('connection_params', 'uri')
MONGODB_HOST = config.get('connection_params', 'host')
MONGODB_PORT = config.get('connection_params', 'port')
MONGODB_DATABASE = config.get('connection_params', 'database')
MONGODB_COLLECTION = config.get('connection_params', 'collection')
MONGODB_TOKEN01 = config.get('connection_params', 'token01')
MONGODB_TOKEN02 = config.get('connection_params', 'token02')

def main():
    logr.info('start')
    try:
        print_sys_info()
        test_mongodb_conn()
        test_mongodb_insert()
    except Exception: 
        logr.exception('Exception')
    logr.info('stop')

def print_sys_info():
    logr.info('login|hostname|os|python : {0}|{1}|{2}|{3}.'.format(os.getlogin(), platform.node() , platform.system() + '-' + platform.release() , platform.python_version()))

def test_mongodb_conn():
    conn_string = MONGODB_URI.format(MONGODB_TOKEN01, MONGODB_TOKEN02, MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE)
    logr.info('connecting uri : ' + conn_string)
    client = MongoClient(conn_string)
    logr.info('mongodb server info: ' + str(client.server_info()))
    db = client[MONGODB_DATABASE]
    coll = db[MONGODB_COLLECTION]
    logr.info('document count: ' + str(coll.count()))
    logr.info('document dump: ' + str(list(coll.find())))
    client.close()

def test_mongodb_insert():
    conn_string = MONGODB_URI.format(MONGODB_TOKEN01, MONGODB_TOKEN02, MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE)
    logr.info('connecting uri : ' + conn_string)
    client = MongoClient(conn_string)
    db = client[MONGODB_DATABASE]
    coll = db[MONGODB_COLLECTION]
    dict_insert = {}
    dict_insert['name'] = 'temp_record'
    dict_insert['creation_timestamp'] = datetime.utcnow()
    dict_insert['creation_epochtime'] = int(time.time())
    dict_insert['random_float'] = random.random()
    logr.info('dict to commit : ' + str(dict_insert))
    obj_id = coll.insert(dict_insert)
    logr.info('insertion successful : ' + str(obj_id))
    some = coll.remove({"_id" : obj_id})
    logr.info('removal successful : ' + str(some))
    client.close()
    

if __name__ == '__main__':
    main()
