#!/bin/bash
# Proof of concept script for indicating which files to release into the red zone.
if [ $# -eq 0 ]; then
    echo "Please provide the uuid of the datafile to release as an argument."
    exit 1
fi
data_to_release="{\"data_to_release_uuid\":\"${1}\"}"
echo $data_to_release
curl -v http://localhost:8881/contentListener -H 'Content-Type: application/json' -d $data_to_release