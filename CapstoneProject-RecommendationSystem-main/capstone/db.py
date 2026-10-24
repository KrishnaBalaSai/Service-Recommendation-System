# db.py
import pymongo
import certifi
from config import MONGO_URI, DB_NAME

client = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]
