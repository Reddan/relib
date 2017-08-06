# d for debugging

import time

def timer(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print('Ran {.__name__} in {} seconds'.format(func, end - start))
    return result
  return wrapper
