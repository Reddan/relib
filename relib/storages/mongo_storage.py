import pymongo
import datetime
import os

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost')
mongo_db = os.environ.get('MONGO_MEMOIZE_DB', 'relib')
mongo = pymongo.MongoClient(mongo_url, connect=False)[mongo_db]
meta_store = mongo.meta_store

def initialize():
  meta = meta_store.find()
  meta = [m for m in meta if get_is_expired(m['collection_name'])]
  for m in meta:
    mongo[m['collection_name']].drop()

def _get_is_expired(collection_name):
  collection_meta = meta_store.find_one({'collection_name': collection_name})
  now = datetime.datetime.now()
  if collection_meta:
    if collection_meta['expire_at']:
      return now >= collection_meta['expire_at']
    return False
  return True

def get_is_expired(collection_name):
  is_expired = _get_is_expired(collection_name)
  return is_expired

def store_data(collection_name, data, expire_in=None):
  expire_at = expire_in and datetime.datetime.now() + datetime.timedelta(seconds=expire_in)
  meta_store.update(
    {'collection_name': collection_name},
    {'collection_name': collection_name, 'expire_at': expire_at},
    upsert=True
  )
  mongo[collection_name].drop()
  mongo[collection_name].insert_many(data)
  return mongo[collection_name]

def load_data(collection_name):
  return mongo[collection_name]
