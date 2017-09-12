import pymongo
import datetime

mongo = pymongo.MongoClient('mongodb://localhost/', connect=False).relib
meta_store = mongo.meta_store

def initialize():
  meta = list(meta_store.find())
  meta = [m for m in meta if get_is_expired(m['collection_name'])]
  for m in meta:
    mongo[m['collection_name']].drop()

def get_is_expired(collection_name):
  collection_meta = meta_store.find_one({'collection_name': collection_name})
  now = datetime.datetime.now()
  if collection_meta and collection_meta['expire_at']:
    return now >= collection_meta['expire_at']
  return False

def store_data(collection_name, data, expire_in=None):
  expire_at = expire_in and datetime.datetime.now() + datetime.timedelta(seconds=expire_in)
  meta_store.update(
    {'collection_name': collection_name},
    {'collection_name': collection_name, 'expire_at': expire_at},
    upsert=True
  )
  collection.drop()
  collection.insert_many(data)
  return collection

def load_data(collection_name):
  return mongo[collection_name]
