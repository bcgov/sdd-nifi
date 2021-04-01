#!/usr/bin/python3
# checks that a data files adheres to given frictionless table schema
# was used for proof of concept NiFi flow; 
# no longer used; replaced by datatype_consistency_check.py
import sys
import json
import csv
from tableschema import Table
from tableschema import TableSchemaException

err_str = ''
def exc_handler(exc, row_number=None, row_data=None, error_data=None):
    global err_str
    errMessage = ''
    if exc.multiple:
        for error in exc.errors:
            errMessage = errMessage + str(error) + ';'
    else:
        errMessage = str(exc)
    err_str = err_str + 'line:' + str((row_number - 1)*fragmentIndex) + ' , error:' + str(errMessage) + '\n' 

# argv[1] is the resource schema; the replace is a bit of a hack due to limitations of NiFi's handling of parameters 
revised = sys.argv[1].replace('ñÇ','"')
try:
    resourceSchema=json.loads(revised)
except:
    print('Error loading json.  Likely json is invalid.', end = '')
    exit()

# argv[2] is the resource in the data package to validate.  The 'data' elment for the resource should be populated (it's this data that is being validated)
resourceName = sys.argv[2]
fragmentIndex = int(sys.argv[3])
csv_file = csv.reader(sys.stdin, skipinitialspace=True, quotechar='"', delimiter=',')
try:
    results = []
    for row in csv_file: # need to create an array of arrays for creation of Table object
        results.append(row)
    table = Table(results, schema=resourceSchema)
    for t in table.iter(integrity=False, relations=False, cast=True, foreign_keys_values=False, exc_handler=exc_handler):
        continue
    if (err_str == ''):
        print('success', end = '')
    else:
        print(err_str, end = '')
except TableSchemaException as e:
    errMessage = ''
    if e.multiple:
        for error in e.errors:
            errMessage = errMessage + str(error) + ';'
    else:
        errMessage = str(e)
    print(errMessage, end = '')