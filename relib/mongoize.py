from . import reutils
from . import f
import pymongo
import time
import inspect
from termcolor import colored

mongo = pymongo.MongoClient('mongodb://localhost/').relib

# Helper functions
def get_function_body(func):
  # TODO: Strip comments
  lines = inspect.getsourcelines(func)[0]
  lines = [line.rstrip() for line in lines]
  lines = [line for line in lines if line]
  return '\n'.join(lines)

def get_hash(string):
  return '_' + reutils.sha224(string)

# Core mongoize
def get_collection_timestamp(collection_name):
  try:
    doc = mongo[collection_name].find_one()
    datetime = doc['_id'].generation_time
    return int(datetime.timestamp())
  except:
    return 0

def get_is_expired(collection_name):
  now = time.time()
  expiration_time = now - (60 * 60 * 24 * 5)
  collection_time = get_collection_timestamp(collection_name)
  return expiration_time >= collection_time

def get(collection_name):
  return list(mongo[collection_name].find({}, {'_id': 0}))

def run_memoizer(func, name, force=False):
  if force or get_is_expired(name):
    if force:
      print(colored(' WITH FORCE ', 'grey', 'on_blue'), colored(name, 'blue'))
    else:
      print(colored(' MEMORIZING ', 'grey', 'on_blue'), colored(name, 'blue'))
    data = func()
    mongo[name].drop()
    mongo[name].insert_many(data)
    for row in data:
      del row['_id']
    return data
  else:
    print(colored(' REMEMBERED ', 'grey', 'on_green'), colored(name, 'green'))
    return get(name)

# Memoize decorator
func_by_wrapper = {}
children_by_func = {}

def get_function_from_wrapper(func):
  return func_by_wrapper[func] if func in func_by_wrapper else func

def get_execution_tree(func):
  function_body = get_function_body(func)
  children = children_by_func[func] if func in children_by_func else []
  children_response = f.map(children, get_execution_tree)
  function_bodies = '\n'.join([function_body] + [res['function_bodies'] for res in children_response])
  hash = get_hash(function_bodies)

  def wrapper_func():
    params = [res['run']() for res in children_response]
    return func(*params)

  def run():
    return run_memoizer(wrapper_func, name=hash)

  return {
    'function_bodies': function_bodies,
    'run': run
  }

def memoize(*funcs):
  def _(func):
    unwrapped_funcs = f.map(funcs, get_function_from_wrapper)
    children_by_func[func] = unwrapped_funcs
    run = get_execution_tree(func)['run']
    func_by_wrapper[run] = func
    return run
  return _
