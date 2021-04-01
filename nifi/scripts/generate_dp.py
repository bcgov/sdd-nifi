#!/usr/bin/python3
# generates frictionless data package json from all csv files in the current directory
# unzips if the filename has a .zip extension
# designed to be used as part of proof of concept NiFi flow
import sys
import os
from datapackage import Package
from datapackage import exceptions
import zipfile
import shutil

try:
    path = sys.argv[1]
    filename = sys.argv[2]
    outputPath = sys.argv[3]
    filePath = path + os.sep + filename
    if filename.endswith('.zip'):
        with zipfile.ZipFile(filePath,"r") as zip_ref:
            zip_ref.extractall(path)
    filenameNoExt = os.path.splitext(filename)[0]
except:
    shutil.rmtree(path)
    print(sys.exc_info()[0])

try:
    package = Package()
    #package.infer(path + os.sep + '*.csv')
    package.infer('**/*.csv')
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    package.save(outputPath + os.sep + filenameNoExt + '_datapackage.zip')
    print('Success. Data package created.', end = '')
    #shutil.rmtree(path)
except exceptions.DataPackageException as e:
    errMessage = ''
    if e.multiple:
        for error in e.errors:
            errMessage = errMessage + str(error) + ';'
    else:
        errMessage = str(e)
    print(errMessage, end = '')
    shutil.rmtree(path)
except:
    shutil.rmtree(path)
    print(sys.exc_info()[0])