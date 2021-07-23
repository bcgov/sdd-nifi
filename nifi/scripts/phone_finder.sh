#!/bin/bash

# pattern is 3 digits followed by a "-" followed by 4 digits
grep '[0-9]\{3\}-[0-9]\{4\}' $1
