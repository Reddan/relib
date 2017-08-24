from . import f
from . import hashing
from . import storage
import inspect

def get_function_body(func):
  # TODO: Strip comments
  lines = inspect.getsourcelines(func)[0]
  lines = [line.rstrip() for line in lines]
  lines = [line for line in lines if line]
  return '\n'.join(lines)

func_by_wrapper = {}
code = type(get_function_body.__code__)

def get_code_children(__code__):
  children = [const for const in __code__.co_consts if isinstance(const, code)]
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
    is_callable = callable(candidate_func)
    is_not_neighbor = is_callable and transform(co_name) not in neighbor_funcs
    return is_not_neighbor

  func_children = f.map(f.filter(co_names, filter), transform)
  func_grand_children = [get_func_children(child_func, func_children) for child_func in func_children]
  funcs = [func] + f.flatten(func_grand_children)
  funcs = list(set(funcs))
  return sorted(funcs, key=lambda func: func.__name__)

def memoize(in_memory=False, compress=False):
  storage_format = 'memory' if in_memory else 'bcolz' if compress else 'pickle'

  def receive_func(func):
    funcs = get_func_children(func)
    function_bodies = f.map(funcs, get_function_body)
    function_bodies_hash = hashing.hash(function_bodies)

    def wrapper(*args, **kwargs):
      def run():
        return func(*args, **kwargs)

      hash = hashing.hash([function_bodies_hash, args, kwargs or 0])
      name = func.__name__ + ' [' + hash + ']'
      return storage.store_on_demand(run, name, storage_format=storage_format)

    wrapper.__name__ = func.__name__ + ' wrapper'
    func_by_wrapper[wrapper] = func
    return wrapper

  return receive_func
