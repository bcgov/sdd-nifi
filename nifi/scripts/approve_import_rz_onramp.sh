#!/bin/bash
# Used as part of NiFi flow to handle requests coming from inside the secure zone being processed
# Options include whether the file specified is GPG encrypted and whether a virus scan of it is needed
# Records who and when approvals are made and saves to an approval json file
if [ $# -eq 0 ]; then
    echo "Please provide a filename of the existing datafile in the redzone as an argument.  You can optionally GPG decrypt by using the -d option.  You can enable virus scanning via the -v option."
    exit 1
fi
encryption_type='None'
run_virus_scan='false'
OPTIND=1
while getopts ":dvf:" opt; do
  case $opt in
    d)
      encryption_type='GPG'
      echo "GPG decryption enabled" >&2
      ;;
    v)
      run_virus_scan='true'
      echo "virus scan enabled" >&2
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2; return 1
      ;;
  esac
done
shift $((OPTIND-1))
if [ -z "$1" ]; then echo "missing filename"; exit 1; else filename="$1"; fi
approver=`whoami`
approval_time=`date`
current_dir=`pwd`
mkdir -p $current_dir/approved/approval_info
json_format='{"data_file_name":"%s","approver":"%s","approval_time":"%s","encryption_type":"%s","run_virus_scan":"%s"}'
json_string=$(printf "$json_format" "$filename" "$approver" "$approval_time" "$encryption_type" "$run_virus_scan")
echo "$json_string" > $current_dir/approved/approval_info/approve_$filename.json
mv $current_dir/$filename $current_dir/approved/$filename
echo "$1 has successfully been approved."