#!/bin/bash
# helper script for highlighting lines in validation report 
if [ ! $1 ] 
then
    echo "Usage: highlight [string]"
    echo "returns stdin with [string] prepended"
    exit 1
fi

while read line
do
    echo "$1 $line"
done  < /dev/stdin
