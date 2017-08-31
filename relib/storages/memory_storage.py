import sys

store = {}

def initialize():
  pass

def get_is_expired(collection_name):
  return collection_name not in store

def store_data(collection_name, data):
  store[sys.intern(collection_name)] = data
  return data

def load_data(collection_name):
  return store[collection_name]
