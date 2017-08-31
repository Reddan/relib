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

def insert_data(path, data):
  c = bcolz.carray(data, rootdir=path, mode='w')
  c.flush()

def store_data(collection_name, data):
  path = storage_dir + collection_name
  created = time.time()
  is_tuple = isinstance(data, tuple)
  length = len(data)
  meta_data = {'created': created, 'is_tuple': is_tuple, 'length': length}
  insert_data(path + '_meta', meta_data)
  if is_tuple:
    for i in range(length):
      sub_collection_name = collection_name + ' (' + str(i) + ')'
      store_data(sub_collection_name, data[i])
  else:
    insert_data(path, data)
  return data

def load_data(collection_name):
  path = storage_dir + collection_name
  meta_data = bcolz.open(path + '_meta')[:][0]
  if meta_data['is_tuple']:
    partitions = range(meta_data['length'])
    data = [load_data(collection_name + ' (' + str(i) + ')') for i in partitions]
    return tuple(data)
  else:
    data = bcolz.open(path)[:]
    return data
