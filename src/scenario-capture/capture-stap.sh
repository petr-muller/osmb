#!/bin/bash

COMMAND=$@

. stap-config.sh

FREEARG='$'"$FREEARG"
MALLOCARG='$'"$MALLOCARG"

rm -f memdump.out
stap -v scenario-capture.stp -c "$COMMAND" -o memdump.out $ALLOCATOR $MALLOC $FREE $MALLOCARG $FREEARG
SCENARIO=`./translate.py memdump.out`
rm -f memdump.out

echo "Created scenarios:"
echo $SCENARIO
