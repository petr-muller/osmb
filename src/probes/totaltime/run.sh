#!/bin/bash

cleanup(){
  rm -rf $EXECUTABLE $BATCHFILE $OUTPUTFILE $LPATH
}

. ../commonlib.sh

parse_options $@

check_option "$ALLOCATOR" "allocator"
check_option "$SSIZE" "sample size"
check_option "$BSIZE" "batch size"
check_option "$SCENARIO" "scenario"
check_option "$MALLOC" "malloc function name"
check_option "$FREE" "free function name"

EXECUTABLE=`mktemp`
BATCHFILE=`mktemp`
OUTPUTFILE=`mktemp`

uniquize_allocator $ALLOCATOR

checked_command "gcc -o $EXECUTABLE $SCENARIO -g -std=c99 $APATH -lpthread -DALLOCATE=$MALLOC -DFREE=$FREE" "Testcase compilation"

checked_command "LD_LIBRARY_PATH=$LPATH $EXECUTABLE" "Test dry run"

cat > $BATCHFILE << EOF
#!/bin/bash

set -e
for batch in \`seq $BSIZE\`
do
	LD_LIBRARY_PATH=$LPATH $EXECUTABLE
done
EOF

chmod a+x $BATCHFILE

echo "REAL SYSTEM USER" > $OUTPUTFILE
for sample in `seq $SSIZE`
do
	checked_command '/usr/bin/time --output $OUTPUTFILE --format "%e %S %U" --append $BATCHFILE'
done

checked_command "python evaluate.py $OUTPUTFILE" "Parsing the output"
cleanup
