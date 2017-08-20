from . import reutils
from . import f
from .storages import pickle_storage
from .storages import bcolz_storage
from .storages import mongo_storage
import inspect
from termcolor import colored

storages = {'pickle': pickle_storage, 'bcolz': bcolz_storage, 'mongo': mongo_storage}

storages['pickle'].initialize()
storages['bcolz'].initialize()

# Helper functions
def get_function_body(func):
  # TODO: Strip comments
  lines = inspect.getsourcelines(func)[0]
  lines = [line.rstrip() for line in lines]
  lines = [line for line in lines if line]
  return '\n'.join(lines)

def get_hash(string):
  return ' [' + reutils.sha224(string) + ']'

# Core mongoize
def run_memoizer(func, name, force=False, storage_format='pickle'):
  storage = storages[storage_format]
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

# Memoize decorator
func_by_wrapper = {}
children_by_func = {}
storage_format_by_func = {}

def get_execution_tree(func):
  function_body = get_function_body(func)
  children = children_by_func[func]
  storage_format = storage_format_by_func[func]
  children_response = f.map(children, get_execution_tree)
  function_bodies = '\n'.join([function_body] + [res['function_bodies'] for res in children_response])
  hash = func.__name__ + get_hash(function_bodies)

  def wrapper_func():
    params = [res['run']() for res in children_response]
    return func(*params)

  def run():
    return run_memoizer(wrapper_func, name=hash, storage_format=storage_format)

  return {
    'function_bodies': function_bodies,
    'run': run
  }

def memoize(*funcs, storage_format='pickle'):
  def _(func):
    unwrapped_funcs = [func_by_wrapper[func] if func in func_by_wrapper else func for func in funcs]
    children_by_func[func] = unwrapped_funcs
    storage_format_by_func[func] = storage_format
    run = get_execution_tree(func)['run']
    func_by_wrapper[run] = func
    return run
  return _
