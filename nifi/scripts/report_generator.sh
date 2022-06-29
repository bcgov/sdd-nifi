#!/bin/bash
# Main validation script that runs on data that newly arrives in the red zone
sep=","
path=$1
report_directory=$2
mkdir -p $report_directory
# find $path -type f -name "* *" | while read file; do mv "$file" ${file// /_}; done

find $path -type f \( -name "*.csv" -or -name "*.CSV" \) -print0 | sort |
while IFS= read -r -d '' file; do
	# determine the md5 hash of the file
	md5sum=$(md5sum "$file")
	base_file_name=$(basename "$file")
	size=$(du -h "$file" | cut  -f1)B
	encoding=$(file -b --mime-encoding "$file")
	num_lines=$(wc -l < "$file")
	# detect what separator (e.g., comma, pipe) is used to separate the column in the csv 
	declare -A delimiter
	delimiter[","]=$(head -1 "$file" | awk -F"," '{print NF}')
	delimiter["|"]=$(head -1 "$file" | awk -F"|" '{print NF}')
	delimiter["\t"]=$(head -1 "$file" | awk -F"\t" '{print NF}')
	delimiter[";"]=$(head -1 "$file" | awk -F";" '{print NF}')
	delimiter[":"]=$(head -1 "$file" | awk -F":" '{print NF}')
	delimiter["^"]=$(head -1 "$file" | awk -F"^" '{print NF}')
	max=0
	for k in "${!delimiter[@]}";do
		if (( ${delimiter["$k"]} > max));then
				max="${delimiter["$k"]}"
				sep="$k"
		fi
	done

	
	# find any numbers that match the pattern for a PHN or phone number
	phnlines=$(./phn_finder.sh "$file" | wc -l)    
	phonelines=$(./phone_finder.sh "$file" | wc -l)
	# create a .tab file for each column in the csv.  Tab files have frequency of each value in the column. 
	./chkfreq.sh "$file" > "${report_directory}${base_file_name}.tab"
	freqnm="${report_directory}${base_file_name}.tab"
	# find any strings that could be common names e.g., Fred
	./scan_names.sh "$freqnm" > "$freqnm.names"
	 
	# print validation report
	echo "Preliminary auto-generated validation report"
	echo "X) $file"
	echo "- size: $size"
	echo "- encoding: $encoding"
	echo "- contains $num_lines lines (including header)"
	echo "- delimiter: $sep"
	echo "- md5sum: $md5sum"
	echo "******"
	./field_summary_csv.sh "$file" $sep | ./highlight.sh *remove
	echo "******"
	echo "- contains $hcolumns columns:"
	./get_column_names.sh "$file"
	echo "******"
	head -5 "$file" | ./highlight.sh *remove
	tail -5 "$file" | ./highlight.sh *remove
	echo "******"
	echo "$phnlines lines have potential PHNs"
	echo "$phonelines lines have potential phone numbers"
	echo ""
	echo ""
done
