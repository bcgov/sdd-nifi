#!/bin/bash
# decripts and unzips AES encrypted datafile with a passphrase from stdin
# no longer used; replaced by "decrypt_and_unzip.sh"
pword=$(< /dev/stdin)
7z x $1 -p$pword -aoa