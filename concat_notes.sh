#!/bin/bash

for d in $*
do
    cd $d
    (for i in *.txt; do echo "";cat -s $i; done) >> all.txt.tmp
    mv all.txt.tmp all.txt
    cp all.txt all.txt.orig
    cd ..
done
