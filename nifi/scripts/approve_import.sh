#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Please provide a filename of the datafile to import into the redzone as an argument."
    exit 1
fi
node approve_import.js $1 "$(whoami)" "$(date)"
#approvalinfo=",\"approver\":\"${USER}\",\"approval_time\":\"${date}\"}"
#echo $approvalinfo
#echo $approvalinfo >> $1 || { echo 'Error appending approval info to file. Exiting.' ; exit 1; }
#data_to_release=cat $1
#echo $data_to_release
#curl -v http://localhost:8881/contentListener -H 'Content-Type: application/json' -d $data_to_release
#mv $1 approved/$1