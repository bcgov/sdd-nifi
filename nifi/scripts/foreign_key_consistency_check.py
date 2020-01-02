#!/usr/bin/python3

import sys
import json
import os
from datapackage import Package
from datapackage import exceptions
import zipfile
import shutil

err_str = ''
def exc_handler(exc, row_number=None, row_data=None, error_data=None):
    global err_str
    if (type(exc).__name__ == 'UnresolvedFKError'):
        errMessage = ''
        if exc.multiple:
            for error in exc.errors:
                errMessage = errMessage + str(error) + ';'
        else:
            errMessage = str(exc)
        err_str = err_str + 'Error:' + str(errMessage) + '\n' 

try:
    path = sys.argv[2]
    # assumes that the datapackage 'resource' array has been added as flowfile attribute; assumes json has quotes replaced with ñÇ (to avoid nifi stripping quotes)
    revised = sys.argv[1].replace('ñÇ','"')
    dataPackageSchema=json.loads(revised)
    filename = sys.argv[3]
    zippath = path + os.sep + filename
    with zipfile.ZipFile(zippath,"r") as zip_ref:
        zip_ref.extractall(path)
except:
    shutil.rmtree(path)
    print(sys.exc_info()[0])

try:
    package = Package(dataPackageSchema, base_path=path)
    for resource in package.resources:
        for r in resource.iter(integrity=False, relations=True, cast=True, foreign_keys_values=False, exc_handler=exc_handler):
            continue
    if (err_str == ''):
        print('Success. Foreign key integrity check passed.', end = '')
    else:
        print(err_str, end = '')
    shutil.rmtree(path)
except exceptions.RelationError as e:
    errMessage = ''
    if e.multiple:
        for error in e.errors:
            errMessage = errMessage + str(error) + ';'
    else:
        errMessage = str(e)
    print(errMessage, end = '')
    shutil.rmtree(path)
except exceptions.DataPackageException: 
    print('Foreign key integrity check passed but other errors present.', end = '')
    shutil.rmtree(path)
