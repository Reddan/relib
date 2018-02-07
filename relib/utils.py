from io import BytesIO
from random import random

def get_tmp_path():
  file_name = str(random())[2:]
  return '/tmp/' + file_name

class PickleableKerasModel():
  def __init__(self, model):
    tmp_path = get_tmp_path()
    model.save(tmp_path)
    with open(tmp_path, 'rb') as file:
      self.wrapped_model = BytesIO(file.read())

  def unwrap(self):
    from keras.models import load_model
    tmp_path = get_tmp_path()
    with open(tmp_path, 'wb') as file:
      file.write(self.wrapped_model.read())
      return load_model(tmp_path)
