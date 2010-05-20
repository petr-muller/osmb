#!/bin/bash

COMMAND=$@

rm -f memdump.out
LD_PRELOAD=./libfakemalloc.so $@
SCENARIO=`./translate.py memdump.out`
rm -f memdump.out

echo "Created scenarios:"
echo $SCENARIO
