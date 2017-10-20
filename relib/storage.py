from .storages import memory_storage, pickle_storage, bcolz_storage, mongo_storage
from termcolor import colored

storages = {
  'memory': memory_storage,
  'pickle': pickle_storage,
  'bcolz': bcolz_storage,
  'mongo': mongo_storage
}

initialized_by_storage = {storages[key]: False for key in storages}

def init_storage(storage):
  if not initialized_by_storage[storage]:
    storage.initialize()
    initialized_by_storage[storage] = True

def log(color, title, invoke_level, name, storage_format):
  title_log = colored(title, 'grey', 'on_' + color)
  invoke_level_log = (' ' * min(1, invoke_level)) + ('──' * invoke_level)
  invoke_level_log = colored(invoke_level_log, color)
  storage_log = colored(storage_format, 'white', attrs=['dark'])
  print(title_log, invoke_level_log, colored(name, color), storage_log)

def store_on_demand(func, name, storage_format='pickle', expire_in=None, invoke_level=0):
  storage = storages[storage_format]
  init_storage(storage)
  do_print = storage_format != 'memory'

  if storage.get_is_expired(name):
    if do_print: log('blue', ' MEMORIZING ', invoke_level, name, storage_format)
    data = func()
    return storage.store_data(name, data, expire_in=expire_in)
  else:
    if do_print: log('green', ' REMEMBERED ', invoke_level, name, storage_format)
    return storage.load_data(name)

def read_from_store(name, storage_format='pickle'):
  storage = storages[storage_format]
  init_storage(storage)
  try:
    return storage.load_data(name)
  except:
    return None
