# s for statistics

from . import f
from collections import Counter

def get_list_of_dominant_values(items, threshold=0.05):
  num_items = len(items)
  freq_by_value = Counter(items)
  distinct_values = sorted(freq_by_value.keys())
  dominant_values = [val for val in distinct_values if freq_by_value[val] / num_items >= threshold]
  return dominant_values, distinct_values

def create_one_hotter(items, by_key, threshold=0.05):
  values = [item[by_key] for item in items]
  dominant_values, distinct_values = get_list_of_dominant_values(values, threshold)
  exclude_other = len(dominant_values) == len(distinct_values)
  categories = dominant_values if exclude_other else dominant_values + ['_OTHER_']
  normal_by_cat = {}

  def create_normal(cat, multiplier):
    if cat not in normal_by_cat:
      normal_by_cat[cat] = {}
    normal = [multiplier if cat == cat2 else 0 for cat2 in categories]
    normal_by_cat[cat][multiplier] = normal
    return normal

  def one_hot(item, multiplier=1):
    cat = item[by_key]
    cat = cat if cat in dominant_values else '_OTHER_'
    if cat == '_OTHER_' and exclude_other:
      raise ValueError('Item contains a non existent category')
    if cat in normal_by_cat and multiplier in normal_by_cat[cat]:
      return normal_by_cat[cat][multiplier]
    else:
      return create_normal(cat, multiplier)

  return one_hot, categories

def get_one_hotter_categories(items, by_key, threshold=0):
  values = [item[by_key] for item in items]
  dominant_values, distinct_values = get_list_of_dominant_values(values, threshold)
  exclude_other = len(dominant_values) == len(distinct_values)
  categories = dominant_values if exclude_other else dominant_values + ['_OTHER_']
  return categories

def create_one_hotter2(categories, by_key):
  normal_by_cat = {}

  def create_normal(cat, multiplier):
    if cat not in normal_by_cat:
      normal_by_cat[cat] = {}
    normal = [multiplier if cat == cat2 else 0 for cat2 in categories]
    normal_by_cat[cat][multiplier] = normal
    return normal

  def one_hot(item, multiplier=1):
    cat = item[by_key]
    cat = cat if cat in categories else '_OTHER_'
    if cat not in categories:
      raise ValueError('Item contains a non existent category')
    if cat in normal_by_cat and multiplier in normal_by_cat[cat]:
      return normal_by_cat[cat][multiplier]
    else:
      return create_normal(cat, multiplier)

  return one_hot

def grid_search(make_params, fn):
  initial_params_set = [f.make_combinations_by_dict(param_set) for param_set in make_params]

  initial_params = {}
  for params_set in initial_params_set:
    initial_params = {**initial_params, **params_set[0]}

  def grid_search(default_params, params_sets, scores_params_list=[]):
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
    return grid_search(new_default_params, params_sets[1:], scores_params_list)

  return grid_search(initial_params, initial_params_set)

