import inspect
from types import CodeType
from . import f
from . import hashing

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

def get_func_children(func, func_by_wrapper={}, neighbor_funcs=[]):
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
  func_grand_children = [get_func_children(child_func, func_by_wrapper, func_children) for child_func in func_children]
  funcs = [func] + f.flatten(func_grand_children)
  funcs = list(set(funcs))
  return sorted(funcs, key=lambda func: func.__name__)

def get_function_hash(func, func_by_wrapper={}):
  funcs = get_func_children(func, func_by_wrapper)
  function_bodies = f.map(funcs, get_function_body)
  function_bodies_hash = hashing.hash(function_bodies)
  return function_bodies_hash
