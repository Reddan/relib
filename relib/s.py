# s for statistics

from . import f
from collections import Counter

def get_list_of_dominant_values(items, threshold=0.05):
  num_items = len(items)
  freq_by_value = Counter(items)
  distinct_values = sorted(freq_by_value.keys())
  dominant_values = [val for val in distinct_values if freq_by_value[val] / num_items >= threshold]
  return dominant_values, distinct_values

def get_one_hotter_categories(items, by_key, threshold=0):
  values = [item[by_key] for item in items]
  dominant_values, distinct_values = get_list_of_dominant_values(values, threshold)
  exclude_other = len(dominant_values) == len(distinct_values)
  categories = dominant_values if exclude_other else dominant_values + ['_OTHER_']
  return categories

def list_dict_distinct_values(items, threshold=0):
  fields = items[0].keys()
  return {field: get_one_hotter_categories(items, field, threshold) for field in fields}

def create_plain_one_hotter(values):
  normal_map = {}

  def create_normal(value, multiplier):
    if value not in normal_map:
      normal_map[value] = {}
    normal = [multiplier if value == value2 else 0 for value2 in values]
    normal_map[value][multiplier] = normal
    return normal

  def one_hot(_value, multiplier=1):
    value = _value if _value in values else '_OTHER_'
    if value in normal_map and multiplier in normal_map[value]:
      return normal_map[value][multiplier]
    if value not in values:
      raise ValueError('Value <' + str(_value) + '> does not exist')
    else:
      return create_normal(value, multiplier)

  return one_hot

def create_one_hotter(values_by_field):
  fields = sorted(values_by_field.keys())
  one_hot_by_field = {field: create_plain_one_hotter(values_by_field[field]) for field in fields}

  def one_hot(item, multiplier=1):
    x = [one_hot_by_field[field](item[field], multiplier) for field in fields]
    return f.flatten(x)

  return one_hot

def iterate_grids(make_params, fn):
  initial_params_set = [f.make_combinations_by_dict(param_set) for param_set in make_params]

  initial_params = {}
  for params_set in initial_params_set:
    initial_params = {**initial_params, **params_set[0]}

  def next_iteration(default_params, params_sets, scores_params_list=[]):
    if len(params_sets) == 0:
      return scores_params_list

    uncleared_set = params_sets[0]
    params_list = [{**default_params, **additional_params} for additional_params in uncleared_set]
    scores = [fn(params) for params in params_list]
    new_scores_params_list = f.dict_zip({'score': scores, 'params': params_list})
    scores_params_list = sorted(new_scores_params_list + scores_params_list, key=lambda x: x['score'])
    min_score_index = scores.index(min(scores))
    additional_params = uncleared_set[min_score_index]
    new_default_params = {**default_params, **additional_params}
    return next_iteration(new_default_params, params_sets[1:], scores_params_list)

  return next_iteration(initial_params, initial_params_set)

def get_model(on_params, grid_data, current_data, grids):
  scores_params_list = iterate_grids(
    grids,
    lambda params: on_params(params, grid_data[0], grid_data[1], grid_data[2], grid_data[3])[1]
  )

  best_params = scores_params_list[0]['params']
  model = on_params(best_params, current_data[0], current_data[1], current_data[2], current_data[3])[0]
  return model
