class Raypipe():
  def __init__(self, handlers=[]):
    self.handlers = handlers

  def add_to_pipeline(self, handler_type, fn):
    handler = (handler_type, fn)
    return Raypipe(self.handlers + [handler])

  def map(self, fn):
    return self.add_to_pipeline('map', fn)

  def flatten(self):
    return self.add_to_pipeline('flatten', None)

  def flat_map(self, fn):
    return self.map(fn).flatten()

  def filter(self, fn):
    return self.add_to_pipeline('filter', fn)

  def sort(self, fn=None):
    return self.add_to_pipeline('sort', fn)

  def distinct(self):
    return self.add_to_pipeline('distinct', None)

  def sort_distinct(self, fn=None):
    return self.distinct().sort(fn)

  def do(self, fn):
    return self.add_to_pipeline('do', fn)

  def compute(self, values):
    for handler_type, handler_fn in self.handlers:
      if handler_type == 'map':
        values = [handler_fn(val) for val in values]
      if handler_type == 'flatten':
        values = [item for sublist in values for item in sublist]
      if handler_type == 'filter':
        values = [val for val in values if handler_fn(val)]
      if handler_type == 'sort':
        values.sort(key=handler_fn)
      if handler_type == 'distinct':
        values = list(set(values))
      if handler_type == 'do':
        values = handler_fn(values)
    return values

raypipe = Raypipe()
