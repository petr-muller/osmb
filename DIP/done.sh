#!/bin/bash

pdftotext projekt.pdf raw.txt
tail -n +90 raw.txt > stripped.txt
CHARS=`wc -c stripped.txt | cut -d ' ' -f 1 `
NPAGES=$(($CHARS/1800))
echo "Znaku:      $CHARS"
echo "Normostran: $NPAGES"
echo "Goal:       100"
