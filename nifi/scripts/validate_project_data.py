#!/usr/bin/python3

import argparse
import os
import json
import sys
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

datapackageJson = json.load(sys.stdin)
parser = argparse.ArgumentParser()
parser.add_argument("projectDir", help="The project directory which the metadata file is about")
parser.add_argument("projectsDir", help="The top level projects directory")

args = parser.parse_args()
projectDir = args.projectDir
projectsDir = args.projectsDir

resourcesJson = datapackageJson["resources"]
filesInMetadata = []
for resourceJson in resourcesJson:
    srcFile = projectsDir + projectDir + resourceJson.get('path')
    filesInMetadata.append(srcFile)
    print(srcFile)

    if ("schema" in resourceJson):
        tblSchema = resourceJson.get("schema")
        table = Table(srcFile, schema=tblSchema)
        for t in table.iter(integrity=False, relations=False, cast=True, foreign_keys_values=False, exc_handler=exc_handler):
            continue

for dir, subdir, files in os.walk(projectsDir + projectDir):
    for file in files:
        f = os.path.join(dir, file)
        if (f not in filesInMetadata):
            err_str = err_str + 'unexpected file:' + f + '\n'
if (err_str == ''):
    print('success', end = '')
else:
    print(err_str, end = '')