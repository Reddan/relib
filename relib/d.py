# d for debugging

import sys
import os
import time
from inspect import getargspec

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print('Ran {.__name__} in {} seconds'.format(func, end - start))
    return result
  return wrapper

def silence_stdout():
  sys.stdout = open(os.devnull, 'w')

def restore_stdout():
  sys.stdout = sys.__stdout__

def get_func_arg_list(func):
  return getargspec(func).args

def silenced(func):
  def wrapper(*args, **kwargs):
    silence_stdout()
    result = func(*args, **kwargs)
    restore_stdout()
    return result
  return wrapper
