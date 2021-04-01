#!/bin/bash
# Captures the name and time of an approval request and feeds that to approve_import.js as part of the NiFi flow
if [ $# -eq 0 ]; then
    echo "Please provide a filename of the datafile to import into the redzone as an argument."
    exit 1
fi
currentdir=`pwd`
reldir=`dirname $0`
node $reldir/approve_import.js $1 $currentdir "$(whoami)" "$(date)"