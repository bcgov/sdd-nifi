#!/usr/bin/python3
import sys
import json
from datapackage import Package
from datapackage import exceptions

dataFolder = sys.argv[1]

try:
    package = Package()
    print(json.dumps(package.infer('**/*.csv')))
except exceptions.DataPackageException as e:
    errMessage = ''
    if e.multiple:
        for error in e.errors:
            errMessage = errMessage + str(error) + ';'
    else:
        errMessage = str(e)
    print(errMessage, end = '')
except:
    print(sys.exc_info()[0])