#!/usr/bin/python3

import re
import sys

err_str = ''
lineNum = 1
lineNumOffset = int(sys.argv[1])
dataFileName = sys.argv[2]
#listOfNames = []
#with open("common_names_yob2018.txt") as f:
#    for l in f:
#        listOfNames.append(l.strip('\n'))
for line in sys.stdin:
    if (re.search('(?<!\d)\d{10}(?!\d)',line)):
       err_str = err_str + 'data file:'+ dataFileName +' line:' + str(lineNumOffset + lineNum) + ' , error: Potential PHN found\n' 
#    if any(cname in line for cname in listOfNames):
#       err_str = err_str + 'data file:'+ dataFileName +' line:' + str(lineNumOffset + lineNum) + ' , error: Potential common name found\n' 
    lineNum = lineNum + 1

if (err_str == ''):
    print('', end = '')
else:
    print(err_str, end = '')