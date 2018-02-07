from io import BytesIO
from random import random

def get_tmp_path():
  file_name = str(random())[2:]
  return '/tmp/' + file_name

def pickle_keras_model(model):
  tmp_path = get_tmp_path()
  model.save(tmp_path)
  with open(tmp_path, 'rb') as file:
    return BytesIO(file.read())

def keras_pickle_to_model(model_bytes):
  from keras.models import load_model
  tmp_path = get_tmp_path()
  with open(tmp_path, 'wb') as file:
    file.write(model_bytes.read())
    return load_model(tmp_path)
