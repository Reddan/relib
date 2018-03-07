import tempfile
from io import BytesIO
from copy import copy
from subprocess import call

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

class TerminalPlot():
  def __init__(self, plt):
    tmp_path = get_tmp_path() + '.png'
    plt.savefig(tmp_path)
    with open(tmp_path, 'rb') as file:
      self.wrapped_plot = BytesIO(file.read())

  def show(self):
    tmp_path = get_tmp_path() + '.png'
    with open(tmp_path, 'wb') as file:
      data = copy(self.wrapped_plot).read()
      file.write(data)
    call(['imgcat', tmp_path])
