#!/usr/bin/python3

import argparse
import os
import json
import sys
from tableschema import Table
from DIPSeparator import *

datapackageJson = json.load(sys.stdin)
parser = argparse.ArgumentParser()
parser.add_argument("uploadDir", help="The file upload directory which the metadata file is about")
parser.add_argument("uploadsDir", help="The top level file upload directory")

args = parser.parse_args()
uploadDir = args.uploadDir
uploadsDir = args.uploadsDir

resourcesJson = datapackageJson["resources"]
for resourceJson in resourcesJson:
    
    tblSchema = resourceJson.get("schema")
    srcFile = uploadsDir + uploadDir + resourceJson.get('path')
    print(srcFile)
    table = Table(srcFile, schema=tblSchema)

    seperator = DIPSeparator()
    startIndex = srcFile.rfind(os.sep)
    endIndex = srcFile.rfind(".")

    if ( startIndex == -1 ):
        startIndex = 0
    else:
        startIndex += 1

    if ( endIndex == -1 ):
        endIndex = len(srcFile)

    fileNameNoExt = srcFile[startIndex:endIndex]
    outputFiles = seperator.separate(table, fileNameNoExt, uploadDir)
    print(outputFiles, end='')