import os
from .. import imports
import bcolz
import time
from pathlib import Path
import shutil

default_dir = f'{Path.home()}/.relib'
storage_dir = os.environ.get('MEMOIZE_DIR', default_dir) + '/memoize/'

def initialize():
  pass

def get_collection_timestamp(path):
  try:
    full_path = storage_dir + path
    meta_data = bcolz.open(f'{full_path}_meta')[:][0]
    # return meta_data['created']
    return time.time()
  except:
    return 0

def get_is_expired(path):
  now = time.time()
  expiration_time = now - (60 * 60 * 24 * 10)
  collection_time = get_collection_timestamp(path)
  return expiration_time >= collection_time

def insert_data(path, data):
  c = bcolz.carray(data, rootdir=path, mode='w')
  c.flush()

def store_data(path, data, expire_in=None):
  full_path = storage_dir + path
  full_dir = '/'.join(full_path.split('/')[:-1])
  imports.ensure_dir(full_dir)
  created = time.time()
  is_tuple = isinstance(data, tuple)
  length = len(data)
  meta_data = {'created': created, 'is_tuple': is_tuple, 'length': length}
  insert_data(f'{full_path}_meta', meta_data)
  if is_tuple:
    for i in range(length):
      sub_path = f'{path} ({i})'
      store_data(sub_path, data[i])
  else:
    insert_data(full_path, data)
  return data

def load_data(path):
  full_path = storage_dir + path
  meta_data = bcolz.open(f'{full_path}_meta')[:][0]
  if meta_data['is_tuple']:
    partitions = range(meta_data['length'])
    data = [load_data(f'{path} ({i})') for i in partitions]
    return tuple(data)
  else:
    data = bcolz.open(full_path)[:]
    return data

def delete_data(path):
  full_path = storage_dir + path
  try:
    shutil.rmtree(f'{full_path}_meta')
    shutil.rmtree(full_path)
  except FileNotFoundError:
    pass
