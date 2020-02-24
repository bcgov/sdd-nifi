#!/bin/bash

freqFile=$1
total=0
input="listofnames.txt"
while IFS= read -r line; do
	nameCt=$(grep -i "$line" $freqFile | cut -d" " -f2)
	for found in $nameCt
	do
		if [ $found > 0 ]
		then
			total=$((total+found))
		fi
	done
done < "$input"
echo $total