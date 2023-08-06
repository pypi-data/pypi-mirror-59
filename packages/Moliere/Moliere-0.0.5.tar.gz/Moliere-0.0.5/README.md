# Moliere
[psycopg2-binary](https://pypi.org/project/psycopg2-binary/) wrapper for easy application integration (e.g. flask web sites).

## Installation
```
$ pip install moliere
```
## Usage
```
import moliere

# Creating instance.
db = moliere.Pgdb()

# Connecting to database.
db.connect(host, db_name, user, pwd)

# Query execution. Return list of dicts (psycopg2 RealDictCursor).
result = db.execute(
  'SELECT * FROM table WHERE id>%(id)s;',
  {
    'id': 7
})

# Closing connection.
db.disconnect()
```

## Automatic connection
While create instance Moliere try to find environment variables with endings `DB_HOST`, `DB_NAME`, `DB_USER` and `DB_PWD`. If it success connection will create automatically.  
Also it have builtin instance of `Pgbd` named `DB_OBJ`, so if you have necessary environment variables you can use package like this:
```
from moliere import DB_OBJ

result = DB_OBJ.execute(
  'SELECT * FROM table WHERE id>%(id)s;',
  {
    'id': 7
})
```