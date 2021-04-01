#!/usr/bin/python3
# checks that a data files adheres to given frictionless table schema
# was used for proof of concept NiFi flow
import sys
import argparse
import json
import csv
from tableschema import Table

err_str = ''
def exc_handler(exc, row_number=None, row_data=None, error_data=None):
    global err_str
    errMessage = ''
    if exc.multiple:
        for error in exc.errors:
            errMessage = errMessage + str(error) + ';'
    else:
        errMessage = str(exc)
    err_str = err_str + 'line:' + str(row_number - 1) + ' , error:' + str(errMessage) + '\n' 

parser = argparse.ArgumentParser()
parser.add_argument("src", help="The source file which the metadata file is about")
parser.add_argument("ts", help="The table schema of the file", nargs='?', default='')

args = parser.parse_args()

srcFile = args.src
results = []

if args.ts == "":
    jsonFile = args.src.replace('.csv', '.json')#args.json
    table = Table(srcFile, jsonFile)
else:
    jsonLoaded=json.loads(args.ts)
    table = Table(srcFile, schema=jsonLoaded)
   
for t in table.iter(integrity=False, relations=False, cast=True, foreign_keys_values=False, exc_handler=exc_handler):
    continue
if (err_str == ''):
    print('success', end = '')
else:
    print(err_str, end = '')