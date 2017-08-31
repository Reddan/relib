import pymongo
import time

mongo = None

def initialize():
  global mongo
  if mongo == None:
    mongo = pymongo.MongoClient('mongodb://localhost/').relib

def get_collection_timestamp(collection_name):
  try:
    doc = mongo[collection_name].find_one()
    datetime = doc['_id'].generation_time
    return int(datetime.timestamp())
  except:
    return 0

def get_is_expired(collection_name):
  now = time.time()
  expiration_time = now - (60 * 60 * 24 * 10)
  collection_time = get_collection_timestamp(collection_name)
  return expiration_time >= collection_time

def store_data(collection_name, data):
  mongo[collection_name].drop()
  mongo[collection_name].insert_many(data)
  for row in data:
    del row['_id']
  return mongo[collection_name]

def load_data(collection_name):
  data = mongo[collection_name].find({}, {'_id': 0})
  return list(data)
