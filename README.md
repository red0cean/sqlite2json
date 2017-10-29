# sqlite2json
sqlite <=> json

## Usage

```
~ ./sqlite2json.py -j test.db test.json
~ file test.json
test.json: ASCII text
~
~ ./sqlite2json -d test.json test.db
~ file test.db
test.db: SQLite 3.x database, last written using SQLite version 3020001
```