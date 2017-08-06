# s for statistics

from collections import Counter

def get_list_of_dominant_values(items, threshold=0.05):
  num_items = len(items)
  freq_by_value = Counter(items)
  distinct_values = list(freq_by_value.keys())
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
