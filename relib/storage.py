from .storages import memory_storage, pickle_storage, bcolz_storage, mongo_storage
from termcolor import colored

storages = {
  'memory': memory_storage,
  'pickle': pickle_storage,
  'bcolz': bcolz_storage,
  'mongo': mongo_storage
}

def log(color, title, invoke_level, name, storage_format):
  title_log = colored(title, 'grey', 'on_' + color)
  invoke_level_log = (' ' * min(1, invoke_level)) + ('──' * invoke_level)
  invoke_level_log = colored(invoke_level_log, color)
  storage_log = colored(storage_format, 'white', attrs=['dark'])
  print(title_log, invoke_level_log, colored(name, color), storage_log)

def store_on_demand(func, name, storage_format='pickle', invoke_level=0):
  storage = storages[storage_format]
  storage.initialize()
  do_print = storage_format != 'memory'

  if storage.get_is_expired(name):
    if do_print: log('blue', ' MEMORIZING ', invoke_level, name, storage_format)
    data = func()
    storage.store_data(name, data)
    return data
  else:
    if do_print: log('green', ' REMEMBERED ', invoke_level, name, storage_format)
    return storage.load_data(name)
