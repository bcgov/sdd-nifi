#!/bin/bash
# Main NiFi flow script for decrypting and unzipping data files
fileName=$1
encryptionType=$2
encryptionKey=$3
runVirusScan=$4
gpgPassPhrase=$(<$5)
case $encryptionType in
	"None")
		if [[ $runVirusScan != 'false' ]] 
		then
			echo 'Starting anti-virus scan...'
			clamscan $fileName || { echo 'File is infected. Exiting.' ; exit 1; }
			echo 'Virus scan complete.'
		fi
		echo 'Unzipping file...'
		7z x $fileName -odata
		#unzip $fileName -d data
	;;
	"GPG")
		decryptedFileName="${fileName}_de.zip"
		[ -z "$gpgPassPhrase" ] && echo "GPG passphrase variable not set." && exit 1
		gpg --decrypt --pinentry-mode loopback --passphrase $gpgPassPhrase -o $decryptedFileName $fileName || { echo 'error occurred during GPG decryption attempt' ; exit 1; }
		echo "Successfully decrypted GPG encrypted file"
		if [[ $runVirusScan != 'false' ]] 
		then
			echo 'Starting anti-virus scan...'
			clamscan $decryptedFileName || { echo 'File is infected. Exiting.' ; exit 1; }
			echo 'Virus scan complete.'
		fi
		echo 'Unzipping file...'
		7z x $decryptedFileName -odata
	;;
	"GPG-MC")
		7z x $fileName -odata || { echo 'error occurred during unzipping attempt' ; exit 1; }
		FILES=./data/*
		[ -z "$gpgPassPhrase" ] && echo "GPG passphrase variable not set." && exit 1
		for f in $FILES
		do
			decryptedFileName="${f}_de" 
			# loop through files and decrypt
			gpg --decrypt --pinentry-mode loopback --passphrase $gpgPassPhrase -o $decryptedFileName $f  || { echo 'error occurred during GPG decryption attempt' ; exit 1; }
			echo "Successfully decrypted GPG encrypted file $f"
			mv $decryptedFileName $f
			if [[ $encryptionKey != 'None' ]]
			then
				7z x $f -p$encryptionKey -aoa -odata || { echo 'error occurred during AES decryption attempt' ; exit 1; }
				mv $f $(basename $f) 
				echo "Successfully decrypted and unzipped AES encrypted file"
			fi
			echo 'Starting anti-virus scan on data folder...'
			clamscan -r data || { echo 'Data folder file(s) is infected. Exiting.' ; exit 1; }
			echo 'Virus scan complete.'
		done
		;;
	"AES")
		7z x $fileName -p$encryptionKey -aoa -odata || { echo 'error occurred during AES decryption attempt' ; exit 1; }
		echo "Successfully decrypted and unzipped AES encrypted file"
		echo 'Starting anti-virus scan on data folder...'
		clamscan -r data || { echo 'Data folder file(s) is infected. Exiting.' ; exit 1; }
		echo 'Virus scan complete.'
		;;
	*)
		echo 'No valid encryption type specified.  Expecting EncryptionType is one of: None, GPG, GPG-MC, AES' 
		exit 1
		;;
esac
