from . import hashing
from . import storage
from .function_body import get_function_hash

func_by_wrapper = {}
invoke_level = -1

def memoize(opt_func=None, in_memory=False, compress=False, mongo=False, expire_in=None):
  storage_format = 'memory' if in_memory else 'bcolz' if compress else 'mongo' if mongo else 'pickle'

  def receive_func(func):
    function_hash = get_function_hash(func, func_by_wrapper)

    def wrapper(*args, **kwargs):
      def run():
        return func(*args, **kwargs)

      global invoke_level
      invoke_level += 1
      hash = hashing.hash([function_hash, args, kwargs or 0])
      name = func.__name__ + ' [' + hash + ']'
      out = storage.store_on_demand(run, name, storage_format=storage_format, expire_in=expire_in, invoke_level=invoke_level)
      invoke_level -= 1
      return out

    wrapper.__name__ = func.__name__ + ' wrapper'
    func_by_wrapper[wrapper] = func
    return wrapper

  return receive_func(opt_func) if callable(opt_func) else receive_func

def read_only(func, args=[], kwargs={}, in_memory=False, compress=False, mongo=False):
  storage_format = 'memory' if in_memory else 'bcolz' if compress else 'mongo' if mongo else 'pickle'
  function_hash = get_function_hash(func)
  hash = hashing.hash([function_hash, args, kwargs or 0])
  name = func.__name__ + ' [' + hash + ']'
  return storage.read_from_store(name, storage_format=storage_format)
