import sys
import os
import hashlib

def sha224(string):
  return hashlib.sha224(string.encode('utf-8')).hexdigest()

def silence_stdout():
  sys.stdout = open(os.devnull, 'w')

def restore_stdout():
  sys.stdout = sys.__stdout__
