#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
#

__author__ = '@laszlokuehl'

import sys
import json
import sqlite3

from collections import OrderedDict as dict

def toJson(dbName):
    db = sqlite3.connect(dbName)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    data = {}

    tables = [table[0] for table in cursor.execute('SELECT name FROM sqlite_master WHERE type="table";').fetchall()]

    for table in tables:
        tableData = [dict(rec) for rec in cursor.execute('SELECT * FROM ' + str(table))]
        data.update({table: tableData})

    return json.dumps(data, indent=4)

def toDb(jsonFile, out):
    db = sqlite3.connect(out)
    cursor = db.cursor()

    data = json.loads(open(jsonFile, 'r').read(), object_pairs_hook=dict)

    for table in data.keys():
        cursor.execute('CREATE TABLE \'%s\' (%s)' % (table, ', '.join(data[table][0].keys())))

        for colm in data[table]:
            vals = colm.values()
            cursor.execute('INSERT INTO \'%s\' VALUES (%s)' % (table, ', '.join(['?'] * len(vals))), vals)

    db.commit()
    db.close()

if __name__ == '__main__':
    if len(sys.argv[1:]) == 3:
        if sys.argv[1] in ['-j', '--json']:
            with open(sys.argv[3], 'w') as f:
                f.write(toJson(sys.argv[2]))

        elif sys.argv[1] in ['-d', '--database']:
            toDb(sys.argv[2], sys.argv[3])
