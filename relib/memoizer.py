from . import hashing
from . import storage
from .function_body import get_function_hash

func_by_wrapper = {}
invoke_level = -1

def get_invoke_path(func, function_hash, args, kwargs):
  hash = hashing.hash([function_hash, args, kwargs or 0])
  file_name = func.__code__.co_filename.split('/')[-1]
  name = func.__name__
  return file_name + '/' + name + '/' + hash

def memoize(opt_func=None, in_memory=False, compress=False, mongo=False, expire_in=None):
  storage_format = 'memory' if in_memory else 'bcolz' if compress else 'mongo' if mongo else 'pickle'

  def receive_func(func):
    function_hash = get_function_hash(func, func_by_wrapper)

    def wrapper(*args, **kwargs):
      def run():
        return func(*args, **kwargs)

      global invoke_level
      invoke_level += 1
      invoke_path = get_invoke_path(func, function_hash, args, kwargs)
      out = storage.store_on_demand(run, invoke_path, storage_format=storage_format, expire_in=expire_in, invoke_level=invoke_level)
      invoke_level -= 1
      return out

    wrapper.__name__ = func.__name__ + ' wrapper'
    func_by_wrapper[wrapper] = func
    return wrapper

  return receive_func(opt_func) if callable(opt_func) else receive_func

def read_only(wrapper_func, args=(), kwargs={}, in_memory=False, compress=False, mongo=False):
  func = func_by_wrapper[wrapper_func]
  storage_format = 'memory' if in_memory else 'bcolz' if compress else 'mongo' if mongo else 'pickle'
  invoke_path = get_invoke_path(func, get_function_hash(func), args, kwargs)
  return storage.read_from_store(invoke_path, storage_format=storage_format)
