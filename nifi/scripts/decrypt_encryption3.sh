#!/bin/bash
pword=$(< /dev/stdin)
7z x $1 -p$pword -aoa