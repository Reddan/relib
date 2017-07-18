from . import mongoize
from . import reutils
import pymssql
import decimal

def get_query_hash(query):
  trimmed_query = '\n'.join([q.strip() for q in query.strip().split('\n')])
  return '_' + reutils.sha224(trimmed_query)

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
    return serialize_rows([x for x in cursor])

def create_instance(server, user, password, database):
  def fetch(query, memoize=False):
    def fn():
      with pymssql.connect(server, user, password, database) as conn:
        return execute_query(conn, query)
    if memoize:
      return mongoize.run_memoizer(fn, name=get_query_hash(query))
    else:
      return fn()

  return fetch
