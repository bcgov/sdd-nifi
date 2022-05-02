#!/bin/bash
# looks for common names; called by report generator script as part of validation
freqFile=$1
total=0
input="listofnames.txt"
echo "Common names in $freqFile:"
while IFS= read -r line; do
	nameCt=$(grep -i "^$line " $freqFile | cut -d" " -f2)
	if [ $nameCt > 0 ]
	then
		echo "$line $nameCt"
	fi
done < "$input"