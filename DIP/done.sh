#!/bin/bash

pdftotext projekt.pdf raw.txt
tail -n +90 raw.txt > stripped.txt
CHARS=`wc -c stripped.txt | cut -d ' ' -f 1 `
NPAGES=$(($CHARS/1800))
echo "Znaku:      $CHARS"
echo "Normostran: $NPAGES"
echo "2nd normo:  $((`wc -c obsah.tex | cut -f 1 -d ' '` / 2000 ))"
echo "Goal:       100"
