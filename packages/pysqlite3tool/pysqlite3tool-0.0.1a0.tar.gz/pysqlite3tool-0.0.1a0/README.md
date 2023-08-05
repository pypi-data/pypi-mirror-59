[![PyPI version](https://badge.fury.io/py/SQLiteTool.svg)](https://badge.fury.io/py/SQLiteTool)
[![Build Status](https://travis-ci.org/c-pher/SQLiteTool.svg?branch=master)](https://travis-ci.org/c-pher/SQLiteTool)

# SQLiteTool
The cross-platform sqlite3 based tool to work with SQLite database.

SQLiteTool can:
- Execute custom SQL query
- Select (returns list)
- Delete
- Insert
- Insert many
- Create database (not implemented)
- Update database (not implemented)
- Get cursor to access to low-level original sqlite3 methods.  

## Installation
For most users, the recommended method to install is via pip:
```cmd
pip install psqlite
```
## Import
```python
from pysqlite3tool import SQLiteTool
```

## Helpful predefined methods

* insert
* select
* delete

...
-

## CHANGELOG
- 0.0.1a (8.01.2020) Initial commit. The first alpha
