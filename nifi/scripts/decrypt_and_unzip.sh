#!/bin/bash
fileName=$1
encryptionType=$2
encryptionKey=$3
GPG_TTY=$(tty)
export GPG_TTY
case $encryptionType in
	"None")
		7z x $fileName -odata
		#unzip $fileName -d data
	;;
	"GPG")
		decryptedFileName="${fileName}_de.zip"
		[ -z "$GPG_PASS_PHRASE" ] && echo "GPG passphrase environment variable not set." && exit 1
		gpg --decrypt --pinentry-mode loopback --passphrase $GPG_PASS_PHRASE -o $decryptedFileName $fileName || { echo 'error occurred during GPG decryption attempt' ; exit 1; }
		7z x $decryptedFileName -odata
	;;
	"GPG-MC")
		7z x $fileName -odata || { echo 'error occurred during unzipping attempt' ; exit 1; }
		FILES=./data/*
		[ -z "$GPG_PASS_PHRASE" ] && echo "GPG passphrase environment variable not set." && exit 1
		for f in $FILES
		do
			decryptedFileName="${f}_de" 
			# loop through files and decrypt
			gpg --decrypt --pinentry-mode loopback --passphrase $GPG_PASS_PHRASE -o $decryptedFileName $f  || { echo 'error occurred during GPG decryption attempt' ; exit 1; }
			mv $decryptedFileName $f
			if [ $encryptionKey != 'None' ]
			then
				7z x $f -p$encryptionKey -aoa -odata || { echo 'error occurred during AES decryption attempt' ; exit 1; }
				mv $f $(basename $f) 
			fi
		done
		;;
	"AES")
		7z x $fileName -p$encryptionKey -aoa -odata || { echo 'error occurred during AES decryption attempt' ; exit 1; }
		;;
	*)
		echo 'no valid encryption type specified.  Expecting EncryptionType is one of: None, GPG, GPG-MC, AES' 
		exit 1
		;;
esac
