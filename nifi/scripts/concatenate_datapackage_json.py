#!/usr/bin/python3

import json
import sys
from datapackage import Package

concatPackageName = sys.argv[1]
concatDpkJson = {}
try:
    concatDpkJson = json.loads(sys.argv[2])
except:
    print("invalid json - 1st datapackage")
try:
    datapackageJson = Package(concatDpkJson)
except:
    print("invalid data package - 1st datapackage")
concatDpkJson['name'] = concatPackageName
i = 2
for arg in sys.argv[2:]:
    try:
        dpkgJson = json.loads(arg)
    except:
        print("invalid json - datapackage " + str(i))
    try:
        #is valid datapackage json?
        datapackageJson = Package(dpkgJson)
    except:
        print("invalid data package - datapackage " + str(i))
    concatDpkJson["resources"].extend(dpkgJson["resources"])
    i = i + 1
print(json.dumps(concatDpkJson))