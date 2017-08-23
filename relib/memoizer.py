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

wrapper_set = set()
func_by_wrapper = {}
code = type(get_function_body.__code__)

def get_code_children(__code__):
  children = [const for const in __code__.co_consts if isinstance(const, code)]
  children = f.flatten([get_code_children(__code__) for __code__ in children])
  return [__code__] + children

def get_func_children(func):
  code_children = get_code_children(func.__code__)
  co_names = f.flatten([__code__.co_names for __code__ in code_children])

  def filter(co_name):
    try:
      return co_name in func.__globals__ and func.__globals__[co_name] in wrapper_set
    except:
      return False

  def transform(co_name):
    return func_by_wrapper[func.__globals__[co_name]]

  func_children = f.map(f.filter(co_names, filter), transform)
  func_children = [get_func_children(child_func) for child_func in func_children]
  funcs = [func] + f.flatten(func_children)
  funcs = list(set(funcs))
  return sorted(funcs, key=lambda func: func.__name__)

def memoize(in_memory=False, compress=False):
  storage_format = 'memory' if in_memory else 'bcolz' if compress else 'pickle'

  def receive_func(func):
    funcs = get_func_children(func)
    concatenated_function_bodies = '\n'.join(f.map(funcs, get_function_body))

    def wrapper(*args, **kwargs):
      def run():
        return func(*args, **kwargs)

      hash = hashing.hash([concatenated_function_bodies, args, kwargs])
      name = func.__name__ + ' [' + hash + ']'
      return storage.store_on_demand(run, name, storage_format=storage_format)

    wrapper.__name__ = func.__name__ + ' wrapper'
    wrapper_set.add(wrapper)
    func_by_wrapper[wrapper] = func
    return wrapper

  return receive_func
