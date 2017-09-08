from . import storage
from . import hashing
import pymssql
import decimal

def get_query_hash(query):
  trimmed_query = '\n'.join([q.strip() for q in query.strip().split('\n')])
  return '_' + hashing.hash(trimmed_query)

def serialize_rows(rows):
  if len(rows) == 0:
    return rows
  keys = rows[0].keys()
  for row in rows:
    for key in keys:
      val = row[key]
      if isinstance(val, decimal.Decimal):
        row[key] = float(val)
  return rows

def execute_query(conn, query):
  with conn.cursor(as_dict=True) as cursor:
    cursor.execute(query)
    return serialize_rows(list(cursor))

def create_instance(**creds):
  def fetch(query, memoize=False):
    def fn():
      with pymssql.connect(**creds) as conn:
        return execute_query(conn, query)
    if memoize:
      return storage.store_on_demand(fn, name=get_query_hash(query))
    else:
      return fn()

  return fetch
