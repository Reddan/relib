import os
import inspect
from types import FunctionType, CodeType
from . import f, imports, hashing

def get_function_dir(func):
  return os.path.dirname(os.path.abspath(func.__code__.co_filename))

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

def get_func_children(func, func_proj_path, func_by_wrapper={}, neighbor_funcs=[]):
  code_children = get_code_children(func.__code__)
  co_names = f.flatten([__code__.co_names for __code__ in code_children])

  def get_candidate_func(co_name):
    try:
      candidate_func = func.__globals__.get(co_name, None)
      return func_by_wrapper.get(candidate_func, candidate_func)
    except TypeError:
      # non hashable datatype
      return None

  def filter(co_name):
    candidate_func = get_candidate_func(co_name)
    if isinstance(candidate_func, FunctionType):
      if candidate_func not in neighbor_funcs:
        func_dir_path = get_function_dir(candidate_func)
        return func_proj_path in func_dir_path
    return False

  func_children = [
    get_candidate_func(co_name)
    for co_name in co_names
    if filter(co_name)
  ]

  func_grand_children = [
    get_func_children(child_func, func_proj_path, func_by_wrapper, func_children)
    for child_func in func_children
  ]

  funcs = [func] + f.flatten(func_grand_children)
  return sorted(set(funcs), key=lambda func: func.__name__)

def get_function_hash(func, func_by_wrapper={}):
  func_dir_path = get_function_dir(func)
  func_proj_path = imports.find_parent_dir_containing(func_dir_path, '.git') or imports.find_parent_dir_containing(func_dir_path, '__init__.py') or os.getcwd()
  funcs = [func] + get_func_children(func, func_proj_path, func_by_wrapper)
  function_bodies = f.map(funcs, get_function_body)
  function_bodies_hash = hashing.hash(function_bodies)
  return function_bodies_hash
