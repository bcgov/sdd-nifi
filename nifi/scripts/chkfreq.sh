#!/bin/bash 
# strip non-space and alphabetic characters
# return a sorted list of lowercase word frequencies
if [ $# -ne 1 ]
then
	echo "Usage: $0 file"
	exit -1
fi
sed -e 's/[^[\t a-zA-Z]/ /g'  "$1" | awk '{
x=1
while(x<=NF) {
	freq[tolower($x)]+=1
	x+=1
}
}i
END {
	for (word in freq) {
		print word " " freq[word]
	}
}' | sort
exit 0
