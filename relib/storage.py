from .storages import pickle_storage, bcolz_storage, mongo_storage
from termcolor import colored

storages = {'pickle': pickle_storage, 'bcolz': bcolz_storage, 'mongo': mongo_storage}

def store_on_demand(func, name, force=False, storage_format='pickle'):
  storage = storages[storage_format]
  storage.initialize()
  storage_log = colored(storage_format, 'white', attrs=['dark'])
  if force or storage.get_is_expired(name):
    if force:
      print(colored(' WITH FORCE ', 'grey', 'on_blue'), colored(name, 'blue'), storage_log)
    else:
      print(colored(' MEMORIZING ', 'grey', 'on_blue'), colored(name, 'blue'), storage_log)
    data = func()
    storage.store_data(name, data)
    return data
  else:
    print(colored(' REMEMBERED ', 'grey', 'on_green'), colored(name, 'green'), storage_log)
    return storage.load_data(name)
