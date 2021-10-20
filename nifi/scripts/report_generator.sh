#!/bin/bash
# Main validation script that runs on data that newly arrives in the red zone
sep=","
path=$1
report_directory=$2
mkdir -p $report_directory
find $path -type f -name "* *" | while read file; do mv "$file" ${file// /_}; done

find $path -type f \( -name "*.csv" -or -name "*.CSV" \) -print0 | sort |
while IFS= read -r -d '' file; do
	base_file_name=$(basename $file)
	dos2unix -q $file
	#sanitize_csv $file
	size=$(du -h $file | cut  -f1)B
	encoding=$(file -b --mime-encoding $file)
	records=$(wc -l < $file)
	# detect what separator (e.g., comma, pipe) is used to separate the column in the csv 
	hcolumnsbycomma=$(head -1 $file | awk -F"," '{print NF}')
	hcolumnsbypipe=$(head -1 $file | awk -F"|" '{print NF}')
	hcolumnsbyhat=$(head -1 $file | awk -F"^" '{print NF}')
	if [ "$hcolumnsbycomma -gt $hcolumnsbypipe" -a "$hcolumnsbycomma -gt $hcolumnsbyhat" ]
	then
		hcolumns=$hcolumnsbycomma
		sep=","
	else
		if [ "$hcolumnsbypipe -gt $hcolumnsbycomma" -a "$hcolumnsbypipe -gt $hcolumnsbyhat" ]
		then
			hcolumns=$hcolumnsbypipe
			sep="|"
		else
			hcolumns=$hcolumnsbyhat
			sep="^"
		fi
	fi
	# find any numbers that match the pattern for a PHN or phone number
	phnlines=$(./phn_finder.sh $file | wc -l)    
	phonelines=$(./phone_finder.sh $file | wc -l)
	# create a .tab file for each column in the csv.  Tab files have frequency of each value in the column. 
	./chkfreq.sh $file > "${report_directory}${base_file_name}.tab"
	freqnm="${report_directory}${base_file_name}.tab"
	# find any strings that could be common names e.g., Fred
	namecnt=$(./scan_names.sh $freqnm)
	# determine the md5 hash of the file
	md5sum=$(md5sum $file) 
	# print validation report
	echo "X) $file"
	echo "- size: $size"
	echo "- encoding: $encoding"
	echo "- contains $records records (including header)"
	echo "- delimiter: $sep"
	echo "- md5sum: $md5sum"
	echo "******"
	./field_summary_csv.sh $file $sep | ./highlight.sh *remove
	echo "run sanitize_csv on the file if there are linebreaks in quoted fields" | ./highlight.sh *remove
	echo "******"
	echo "- contains $hcolumns columns:"
	./get_column_names.sh $file | ./highlight.sh *remove
	echo "******"
	head -5 $file | ./highlight.sh *remove
	tail -5 $file | ./highlight.sh *remove
	echo "******"
	echo "$phnlines lines have potential PHNs"
	echo "$phonelines lines have potential phone numbers"
	echo "$namecnt potential names flagged"
	echo ""
	echo ""
done
