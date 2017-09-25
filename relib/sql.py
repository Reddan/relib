from . import storage
from . import hashing
import pyodbc
import decimal

def get_query_hash(query):
  trimmed_query = '\n'.join([q.strip() for q in query.strip().split('\n')])
  return '_' + hashing.hash(trimmed_query)

def serialize_row(row):
  for i in range(len(row)):
    if isinstance(row[i], decimal.Decimal):
      row[i] = float(row[i])
  return row

def execute_query(conn, query):
  with conn.cursor() as cursor:
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]

    def dictify(row):
      serialize_row(row)
      return dict(zip(columns, row))

    rows = [dictify(row) for row in cursor.fetchall()]
    return rows

def create_instance(**creds):
  connection_string = 'DRIVER={0};PORT={1};SERVER={2};PORT={1};DATABASE={3};UID={4};PWD={5}'.format(
    '{ODBC Driver 13 for SQL Server}',
    creds['port'] if 'port' in creds else 1433,
    creds['server'],
    creds['database'],
    creds['user'],
    creds['password']
  )

  def fetch(query, memoize=False):
    def fn():
      with pyodbc.connect(connection_string) as conn:
        return execute_query(conn, query)
    if memoize:
      return storage.store_on_demand(fn, name=get_query_hash(query))
    else:
      return fn()

  return fetch
