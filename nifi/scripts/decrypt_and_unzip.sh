#!/bin/bash
fileName=$1
encyptionKey=$2
GPGPassPhraseFile=$3
GPGPrivateKeyLocation=$4
GPG_TTY=$(tty)
export GPG_TTY
case $encyptionKey in
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
		done
		;;
	*)
		7z x $fileName -p$encyptionKey -aoa -odata;;
esac
