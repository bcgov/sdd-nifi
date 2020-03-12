#!/usr/bin/python3

import argparse
import os
import json
from tableschema import Table
from DIPSeparator import *

parser = argparse.ArgumentParser()
parser.add_argument("src", help="The source file which the metadata file is about")
parser.add_argument("ts", help="The table schema of the file", nargs='?', default='')

args = parser.parse_args()

srcFile = args.src
if args.ts == "":
    jsonFile = args.src.replace('.csv', '.json')#args.json
    table = Table(srcFile, jsonFile)
else:
    jsonLoaded=json.loads(args.ts)
    table = Table(srcFile, schema=jsonLoaded)

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
outputFiles = seperator.separate(table, fileNameNoExt)
print(outputFiles, end='')