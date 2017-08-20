from .. import imports
import bcolz
import numpy as np
import time
from pathlib import Path

storage_dir = str(Path.home()) + '/.relib/memoize/bcolz/'

def initialize():
  imports.ensure_dir(storage_dir)

def get_collection_timestamp(collection_name):
  try:
    meta_data = bcolz.open(storage_dir + collection_name + '_meta')[:][0]
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
  is_list = isinstance(data, list)
  is_np_array = isinstance(data, np.ndarray)
  meta_data = {'created': created, 'is_list': is_list, 'is_np_array': is_np_array}
  c = bcolz.carray(data, rootdir=storage_dir + collection_name, mode='w')
  c.flush()
  c = bcolz.carray(meta_data, rootdir=storage_dir + collection_name + '_meta', mode='w')
  c.flush()

def load_data(collection_name):
  data = bcolz.open(storage_dir + collection_name)[:]
  meta_data = bcolz.open(storage_dir + collection_name + '_meta')[:][0]
  if meta_data['is_list']:
    return data.tolist()
  if not meta_data['is_np_array']:
    return data[0]
  return data
