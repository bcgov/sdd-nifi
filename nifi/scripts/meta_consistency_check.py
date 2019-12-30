#!/usr/bin/python3

import sys
import json
from datapackage import Package
from datapackage import exceptions

# argv[1] is the data package schema
revised = sys.argv[1].replace('ñÇ','"')
try:
    dataPackageSchema=json.loads(revised)
except:
    print('Error loading json.  Likely json is invalid.', end = '')
    exit()

# argv[2] is the resource in the data package to validate.  The 'data' elment for the resource should be populated (it's this data that is being validated)
resourceName = sys.argv[2]
try:
    package = Package(dataPackageSchema)
    resource = package.get_resource(resourceName)
    resource.read(keyed=False, extended=False, cast=True, integrity=False, relations=False)
    print('success', end = '')
except exceptions.DataPackageException as e:
    errMessage = ''
    if e.multiple:
        for error in e.errors:
            errMessage = errMessage + str(error) + ';'
    else:
        errMessage = str(e)
    print(errMessage, end = '')