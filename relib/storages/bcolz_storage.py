import os
from .. import imports
import bcolz
from datetime import datetime
from pathlib import Path
import shutil

default_dir = str(Path.home()) + '/.relib'
storage_dir = os.environ.get('MEMOIZE_DIR', default_dir) + '/memoize/'

def initialize():
  pass

def get_collection_timestamp(path):
  full_path = storage_dir + path
  meta_data = bcolz.open(full_path + '_meta')[:][0]
  return meta_data['created']

def get_is_expired(path):
  try:
    get_collection_timestamp(path)
    return False
  except:
    return True

def should_expire(path, expire_fn):
  return expire_fn(get_collection_timestamp(path))

def insert_data(path, data):
  c = bcolz.carray(data, rootdir=path, mode='w')
  c.flush()

def store_data(path, data, expire_in=None):
  full_path = storage_dir + path
  full_dir = '/'.join(full_path.split('/')[:-1])
  imports.ensure_dir(full_dir)
  created = datetime.now()
  is_tuple = isinstance(data, tuple)
  length = len(data)
  meta_data = {'created': created, 'is_tuple': is_tuple, 'length': length}
  insert_data(full_path + '_meta', meta_data)
  if is_tuple:
    for i in range(length):
      sub_path = path + ' (' + str(i) + ')'
      store_data(sub_path, data[i])
  else:
    insert_data(full_path, data)
  return data

def load_data(path):
  full_path = storage_dir + path
  meta_data = bcolz.open(full_path + '_meta')[:][0]
  if meta_data['is_tuple']:
    partitions = range(meta_data['length'])
    data = [load_data(path + ' (' + str(i) + ')') for i in partitions]
    return tuple(data)
  else:
    data = bcolz.open(full_path)[:]
    return data

def delete_data(path):
  full_path = storage_dir + path
  try:
    shutil.rmtree(full_path + '_meta')
    shutil.rmtree(full_path)
  except FileNotFoundError:
    pass
