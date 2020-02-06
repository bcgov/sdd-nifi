#!/bin/bash

# awk expression ignores commas in double-quoted fields
# see: https://www.gnu.org/software/gawk/manual/html_node/Splitting-By-Content.html 

file=$1

if [[ $2 ]]
then
    sep=$2
else
    sep=,
fi




hfields=$(head -1 $file | awk -F$sep '{print NF}')
echo "Header has $hfields fields"




tail -n +2 $file | awk -F$sep -vFPAT="([^$sep]*)|(\"[^\"]+\")" -vOFS=$sep '{addup[NF]+=1}                                                                            
END {                                                                                                                                    
for (i in addup) {                                                                                                                       
print addup[i] " rows with " i " fields"                                                                         

}}' 

echo "total $(cat $file | wc -l) rows in file"
