#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Please provide a filename of the existing datafile in the redzone as an argument.  You can optionally GPG decrypt by adding a 2nd argument of 'GPG'."
    exit 1
fi
if [[ $2 == 'GPG' ]]; then
   encryption_type='GPG'
   echo "GPG decryption option selected."
else
   encryption_type='None'
fi
approver=`whoami`
approval_time=`date`
current_dir=`pwd`
mkdir -p $current_dir/approved/approval_info
json_format='{"data_file_name":"%s","approver":"%s","approval_time":"%s","encryption_type":"%s"}'
json_string=$(printf "$json_format" "$1" "$approver" "$approval_time" "$encryption_type")
echo "$json_string" > $current_dir/approved/approval_info/approve_$1.json
mv $current_dir/$1 $current_dir/approved/$1
echo "$1 has successfully been approved."