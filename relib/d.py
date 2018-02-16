# d for debugging

import sys
import os
from time import time as timestamp
from inspect import getargspec
from termcolor import colored

id = 0

class measure_duration:
  def __init__(self, name):
    self.name = name
    self.start = timestamp()

  def __enter__(self):
    pass

  def __exit__(self, *_):
    duration = round(timestamp() - self.start, 4)
    text = '{}: {} seconds'.format(self.name, duration)
    print(colored(text, attrs=['dark']))

def timer(func):
  def wrapper(*args, **kwargs):
    global id
    name = func.__name__ + '[' + str(id) + ']'
    id += 1
    with measure_duration(name):
      return func(*args, **kwargs)
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
