from time import time
from termcolor import colored

active_mds = []

class measure_duration:
  def __init__(self, name):
    self.name = name
    active_mds.append(self)

  def __enter__(self):
    self.start = time()

  def __exit__(self, *_):
    duration = round(time() - self.start, 4)
    depth = len(active_mds) - 1
    indent = ('──' * depth) + (' ' * (depth > 0))
    text = '{}: {} seconds'.format(self.name, duration)
    print(colored(indent + text, attrs=['dark']))
    active_mds.remove(self)
