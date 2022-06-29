#!/bin/bash

# Pattern is 9 followed by 9 digits which may be preceded or followed by non-digits 
grep '\(^9[0-9]\{9\}$\|[^0-9]9[0-9]\{9\}$\|^9[0-9]\{9\}[^0-9]\|[^0-9]9[0-9]\{9\}[^0-9]\)' "$1"
