"""Configure app to connect with database mongo."""
import os
from pymongo import MongoClient

DATABASE = MongoClient()['restapi'] # DB_NAME
client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
DEBUG = True
#client = MongoClient('localhost', 27017)