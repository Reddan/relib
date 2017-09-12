from . import f
from . import hashing
from . import storage
import inspect
from types import CodeType

func_by_wrapper = {}
invoke_level = -1

def get_function_body(func):
  # TODO: Strip comments
  lines = inspect.getsourcelines(func)[0]
  lines = [line.rstrip() for line in lines]
  lines = [line for line in lines if line]
  return '\n'.join(lines)

def get_code_children(__code__):
  children = [const for const in __code__.co_consts if isinstance(const, CodeType)]
  children = f.flatten([get_code_children(__code__) for __code__ in children])
  return [__code__] + children

def get_func_children(func, neighbor_funcs=[]):
  code_children = get_code_children(func.__code__)
  co_names = f.flatten([__code__.co_names for __code__ in code_children])

  def transform(co_name):
    candidate_func = func.__globals__[co_name]
    return func_by_wrapper.get(candidate_func, candidate_func)

  def filter(co_name):
    candidate_func = func.__globals__.get(co_name, None)
    is_callable = callable(candidate_func) and hasattr(candidate_func, '__code__')
    is_not_neighbor = is_callable and transform(co_name) not in neighbor_funcs
    return is_not_neighbor

  func_children = f.map(f.filter(co_names, filter), transform)
  func_grand_children = [get_func_children(child_func, func_children) for child_func in func_children]
  funcs = [func] + f.flatten(func_grand_children)
  funcs = list(set(funcs))
  return sorted(funcs, key=lambda func: func.__name__)

def get_function_hash(func):
  funcs = get_func_children(func)
  function_bodies = f.map(funcs, get_function_body)
  function_bodies_hash = hashing.hash(function_bodies)
  return function_bodies_hash

def memoize(*args, in_memory=False, compress=False, mongo=False, expire_in=None):
  storage_format = 'memory' if in_memory else 'bcolz' if compress else 'mongo' if mongo else 'pickle'

  def receive_func(func):
    function_hash = get_function_hash(func)

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

  if len(args) == 1 and callable(args[0]):
    return receive_func(args[0])

  return receive_func
