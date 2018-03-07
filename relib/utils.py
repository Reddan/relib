import tempfile
from io import BytesIO
from copy import copy

def get_tmp_path():
  return tempfile.mkstemp()[1]

class PickleableKerasModel():
  def __init__(self, model):
    tmp_path = get_tmp_path() + '.h5'
    model.save(tmp_path)
    with open(tmp_path, 'rb') as file:
      self.wrapped_model = BytesIO(file.read())

  def unwrap(self):
    from keras.models import load_model
    tmp_path = get_tmp_path() + '.h5'
    with open(tmp_path, 'wb') as file:
      data = copy(self.wrapped_model).read()
      file.write(data)
      return load_model(tmp_path)
