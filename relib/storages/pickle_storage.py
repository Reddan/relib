from .. import imports
import pickle
import time
from pathlib import Path

storage_dir = str(Path.home()) + '/.relib/memoize/pickle/'

def initialize():
  imports.ensure_dir(storage_dir)

def get_collection_timestamp(collection_name):
  try:
    with open(storage_dir + collection_name + '_meta.pkl', 'rb') as file:
      meta_data = pickle.load(file)
    return meta_data['created']
  except:
    return 0

def get_is_expired(collection_name):
  now = time.time()
  expiration_time = now - (60 * 60 * 24 * 10)
  collection_time = get_collection_timestamp(collection_name)
  return expiration_time >= collection_time

def store_data(collection_name, data):
  created = time.time()
  meta_data = {'created': created}
  with open(storage_dir + collection_name + '.pkl', 'wb') as file:
    pickle.dump(data, file, -1)
  with open(storage_dir + collection_name + '_meta.pkl', 'wb') as file:
    pickle.dump(meta_data, file, -1)
  return data

def load_data(collection_name):
  with open(storage_dir + collection_name + '.pkl', 'rb') as file:
    return pickle.load(file)
