def distinct(items):
  return list(set(items))

def find(iterable):
  return next(iterable, None)

def transpose_dict(des):
  keys = list(des.keys())
  length = len(des[keys[0]])

  return [
    {
      key: des[key][i]
      for key in keys
    }
    for i in range(length)
  ]

def make_combinations_by_dict(des, keys=None, pairs=[]):
  keys = sorted(des.keys()) if keys == None else keys
  if len(keys) == 0:
    return [dict(pairs)]
  key = keys[0]
  remaining_keys = keys[1:]
  new_pairs = [(key, val) for val in des[key]]
  return flatten(
    [make_combinations_by_dict(des, remaining_keys, [pair] + pairs) for pair in new_pairs]
  )

def merge_dicts(*dicts):
  result = {}
  for dictionary in dicts:
    result.update(dictionary)
  return result

def intersect(*lists):
  return set.intersection(*map(set, lists))

def ensure_tuple(value):
  if isinstance(value, tuple):
    return value
  return (value,)

def omit(d, keys):
  if keys:
    d = dict(d)
    for key in keys:
      del d[key]
  return d

def pick(d, keys):
  return tuple(d[key] for key in keys)

def flatten(l, iterations=1):
  if iterations == 0:
    return l
  return flatten([value for inner_list in l for value in inner_list], iterations - 1)

def transpose(tuples, default_num_returns=0):
  result = tuple(zip(*tuples))
  if not result:
    return ([],) * default_num_returns
  return tuple(map(list, result))

def deepen_dict(d):
  result = {}
  for (*tail, head), value in d.items():
    curr = result
    for key in tail:
      if key not in curr:
        curr[key] = {}
      curr = curr[key]
    curr[head] = value
  return result

def group(pairs):
  values_by_key = {}
  for key, value in pairs:
    if key not in values_by_key:
      values_by_key[key] = []
    values_by_key[key].append(value)
  return values_by_key

def get_at(d, keys, default):
  try:
    for key in keys:
      d = d[key]
  except KeyError:
    return default
  return d
