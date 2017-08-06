# s for statistics

from collections import Counter

def get_list_of_dominant_values(items, threshold=0.05):
  num_items = len(items)
  freq_by_value = Counter(items)
  distinct_values = list(freq_by_value.keys())
  dominant_values = [val for val in distinct_values if freq_by_value[val] / num_items >= threshold]
  return dominant_values, distinct_values

