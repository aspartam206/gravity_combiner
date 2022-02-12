#!/bin/sh
cd blocklist
for file in ./*.txt
do
    zip -9 $(basename -s .txt $file) $file
done