import pymongo
from datetime import datetime
import os

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost')
mongo_db = os.environ.get('MONGO_MEMOIZE_DB', 'relib')
mongo = pymongo.MongoClient(mongo_url, connect=False)[mongo_db]
meta_store = mongo.meta_store

def initialize():
  pass

def get_collection_timestamp(path):
  collection_meta = meta_store.find_one({'path': path})
  return collection_meta['created']

def get_is_expired(path):
  try:
    get_collection_timestamp(path)
    return False
  except:
    return True

def should_expire(path, expire_fn):
  return expire_fn(get_collection_timestamp(path))

def store_data(path, data):
  created = datetime.now()
  meta_store.update(
    {'path': path},
    {'path': path, 'created': created},
    upsert=True
  )
  mongo[path].drop()
  mongo[path].insert_many(data)
  return mongo[path]

def load_data(path):
  return mongo[path]
