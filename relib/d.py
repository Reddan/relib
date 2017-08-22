# d for debugging

import sys
import os
import time

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
