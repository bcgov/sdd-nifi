#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Please provide a filename of the datafile to import into the redzone as an argument."
    exit 1
fi
currentdir=`pwd`
reldir=`dirname $0`
node $reldir/approve_import.js $1 $currentdir "$(whoami)" "$(date)"