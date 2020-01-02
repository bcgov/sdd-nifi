#!/usr/bin/python3

import sys
import json
from datapackage import Package
from datapackage import exceptions

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

# argv[1] is the data package schema 
revised = sys.argv[1].replace('ñÇ','"')
try:
    dataPackageSchema=json.loads(revised)
except:
    print('Error loading json.  Likely json is invalid.', end = '')
    exit()

# argv[2] is the resource in the data package to validate.  The 'data' elment for the resource should be populated (it's this data that is being validated)
resourceName = sys.argv[2]
fragmentIndex = int(sys.argv[3])
try:
    package = Package(dataPackageSchema)
    resource = package.get_resource(resourceName)
    for r in resource.iter(integrity=False, relations=False, cast=True, foreign_keys_values=False, exc_handler=exc_handler):
        continue
    if (err_str == ''):
        print('success', end = '')
    else:
        print(err_str, end = '')
except exceptions.DataPackageException as e:
    errMessage = ''
    if e.multiple:
        for error in e.errors:
            errMessage = errMessage + str(error) + ';'
    else:
        errMessage = str(e)
    print(errMessage, end = '')