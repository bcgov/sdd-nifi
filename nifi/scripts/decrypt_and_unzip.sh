#!/bin/bash
fileName=$1
encryptionType=$2
GPGPassPhraseFile=$3
GPGPrivateKeyLocation=$4
encryptionKey=$5
GPG_TTY=$(tty)
export GPG_TTY
case $encryptionType in
	"None")
		7z x $fileName -odata
		#unzip $fileName -d data
	;;
	"GPG")
		#gpg --import < $GPGPrivateKeyLocation
		decryptedFileName="${fileName}_de.zip" 
		gpg --decrypt --pinentry-mode loopback  --passphrase-file $GPGPassPhraseFile -o $decryptedFileName --secret-keyring $GPGPrivateKeyLocation $fileName
		7z x $decryptedFileName -odata
	;;
	"GPG-MC")
		7z x $fileName -odata
		FILES=./data/*
		for f in $FILES
		do
			decryptedFileName="${f}_de" 
			# loop through files and decrypt
			gpg --decrypt --pinentry-mode loopback  --passphrase-file $GPGPassPhraseFile -o $decryptedFileName --secret-keyring $GPGPrivateKeyLocation $f
			mv $decryptedFileName $f
			if [ $encryptionKey != 'None' ]
			then
				7z x $f -p$encryptionKey -aoa -odata || { echo 'error occurred during AES decryption attempt' ; exit 1; }
				mv $f $(basename $f) 
			fi
		done
		;;
	*)
		7z x $fileName -p$encyptionKey -aoa -odata;;
esac
