from .. import imports
import pickle
import time
from pathlib import Path

storage_dir = str(Path.home()) + '/.relib/memoize/'

def initialize():
  pass

def get_collection_timestamp(path):
  try:
    full_path = storage_dir + path
    with open(full_path + '_meta.pkl', 'rb') as file:
      meta_data = pickle.load(file)
    return meta_data['created']
  except:
    return 0

def get_is_expired(path):
  now = time.time()
  expiration_time = now - (60 * 60 * 24 * 10)
  collection_time = get_collection_timestamp(path)
  return expiration_time >= collection_time

def store_data(path, data, expire_in=None):
  created = time.time()
  meta_data = {'created': created}
  full_path = storage_dir + path
  full_dir = '/'.join(full_path.split('/')[:-1])
  imports.ensure_dir(full_dir)
  with open(full_path + '.pkl', 'wb') as file:
    pickle.dump(data, file, -1)
  with open(full_path + '_meta.pkl', 'wb') as file:
    pickle.dump(meta_data, file, -1)
  return data

def load_data(path):
  full_path = storage_dir + path
  with open(full_path + '.pkl', 'rb') as file:
    return pickle.load(file)
