import tempfile
import os
from io import BytesIO
from copy import copy
from subprocess import call
from pathlib import Path

def get_tmp_path():
  return tempfile.mkstemp()[1]

def get_tmp_directory():
  dir_path = get_tmp_path()
  os.remove(dir_path)
  os.makedirs(dir_path)
  return dir_path + '/'

class DirectoryBytesIO:
  def __init__(self, directory):
    p = Path(directory)
    file_names = [x.name for x in p.iterdir()]

    def to_bytes(path):
      with open(path, 'rb') as file:
        return BytesIO(file.read())

    self.byte_map = {
      file_name: to_bytes(directory + '/' + file_name)
      for file_name in file_names
    }

  def unpack(self, directory):
    for file_name in self.byte_map:
      path = directory + '/' + file_name
      with open(path, 'wb') as file:
        data = copy(self.byte_map[file_name]).read()
        file.write(data)

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

class TerminalPlot():
  def __init__(self, plt):
    tmp_path = get_tmp_path() + '.png'
    plt.savefig(tmp_path)
    with open(tmp_path, 'rb') as file:
      self.wrapped_plot = BytesIO(file.read())
    os.remove(tmp_path)
    plt.close()

  def show(self):
    tmp_path = get_tmp_path() + '.png'
    self.savefig(tmp_path)
    call(['imgcat', tmp_path])
    os.remove(tmp_path)

  def savefig(self, path):
    with open(path, 'wb') as file:
      data = copy(self.wrapped_plot).read()
      file.write(data)
