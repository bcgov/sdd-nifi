#!/usr/bin/python3
"""
Proof of concept script for checking if a research project's datafiles match
the metadata for the project's data. Basically we want to make sure our metadata for
a project's data is in fact what data we're giving them.   
"""
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
#loop all the files (called resources in frictionless) in the metadata
for resourceJson in resourcesJson:
    srcFile = projectsDir + projectDir + resourceJson.get('path')
    filesInMetadata.append(srcFile)
    print(srcFile)
    
    #if the metadata has a schema use it to validate the data
    #we want to make sure the data adheres to the metadata
    if ("schema" in resourceJson):
        tblSchema = resourceJson.get("schema")
        table = Table(srcFile, schema=tblSchema)
        for t in table.iter(integrity=False, relations=False, cast=True, foreign_keys_values=False, exc_handler=exc_handler):
            continue
# find any files in the project folder that are not in the metadata 
# i.e., did the project receive a file(s) they should've have?
for dir, subdir, files in os.walk(projectsDir + projectDir):
    for file in files:
        f = os.path.join(dir, file)
        if (f not in filesInMetadata):
            err_str = err_str + 'unexpected file:' + f + '\n'
if (err_str == ''):
    print('success', end = '')
else:
    print(err_str, end = '')