import json
import csv

def import_json(filename):
  with open(filename) as file:
    return json.load(file)

def export_json(filename, data):
  with open(filename, 'w') as file:
    json.dump(data, file)

def import_csv_as_dict_array(filename, delimiter=','):
  with open(filename) as file:
    reader = csv.DictReader(file, delimiter=delimiter, skipinitialspace=True)
    return [{k: v for k, v in row.items()} for row in reader]

def export_csv_from_dict_array(filename, data):
  keys = data[0].keys()
  with open(filename, 'w') as file:
    dict_writer = csv.DictWriter(file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
