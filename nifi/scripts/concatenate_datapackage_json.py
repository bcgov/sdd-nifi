#!/usr/bin/python3
# create a frictionless data package by combining n data packages together
# given a dataset's data may come from multiple uploads from a data provider there would then be
# a need to be able to combine the upload data package jsons together to have one that represented
# the dataset in its entirety.
# proof of concept; not used;
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
    #To do - need to test that resource names are unique 
try:
    #is valid datapackage json?
    combinedDataPackageJson = Package(concatDpkJson)
except:
    print("invalid combined data package")
print(json.dumps(concatDpkJson))