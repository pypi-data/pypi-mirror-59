# Introduction


Naive aproach of pgfield with an external PG database

## Basic instructions

- Python >= 3.7
- PostgreSQL >= 9.6


```
  load_utilities:
    pgfield:
      factory: guillotina_pgfield.utility.PGFieldUtility
      provides: guillotina_pgfield.interfaces.IPGFieldUtility
      settings:
        dsn: postgres://user:passwd@pg_url:5432/db
        pool_size: 10
```

