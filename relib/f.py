def map(items, fn):
  return [fn(x) for x in items]

def filter(items, fn):
  return [x for x in items if fn(x)]

def flatten(l):
  return [item for sublist in l for item in sublist]

def group(items, fn):
  data_by_key = {}
  for item in items:
    key = fn(item)
    if key not in data_by_key:
      data_by_key[key] = []
    data_by_key[key].append(item)
  return data_by_key

def compose_dict(items, fn):
  d = {}
  for item in items:
    key, val = fn(item)
    d[key] = val
  return d

def dict_zip(des):
  keys = list(des.keys())
  length = len(des[keys[0]])

  def make_d(index):
    d = {}
    for key in keys:
      d[key] = des[key][index]
    return d

  return map(range(length), make_d)
