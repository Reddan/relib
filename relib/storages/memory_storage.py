store = {}

def initialize():
  pass

def get_is_expired(collection_name):
  return collection_name not in store

def store_data(collection_name, data):
  store[collection_name] = data

def load_data(collection_name):
  return store[collection_name]
