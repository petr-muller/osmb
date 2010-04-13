#!/bin/bash

ALLOCATOR=""
SCENARIO=""
SSIZE=""
BSIZE=""
MALLOC=""
FREE=""

while getopts a:f:s:b:m:d: o
do
	case "$o" in
		a) ALLOCATOR="$OPTARG";;
		f) SCENARIO="$OPTARG";;
		s) SSIZE="$OPTARG";;
		b) BSIZE="$OPTARG";;
		m) MALLOC="$OPTARG";;
		d) FREE="$OPTARG";;
		[?]) echo "Invalid option: $o" >&2; exit 1;;
	esac
done

if 	[ -z "$ALLOCATOR" ] || [ -z "$SSIZE" ] || [ -z "$BSIZE" ] ||\
	[ -z "$SCENARIO" ] || [ -z "$MALLOC" ] || [ -z "$FREE" ]
then
	echo "Not all of mandatory options were supplied" >&2
	exit 1
fi

EXECUTABLE=`mktemp`
BATCHFILE=`mktemp`
OUTPUTFILE=`mktemp`

gcc -o $EXECUTABLE $SCENARIO -g -std=c99 -lpthread -DALLOCATE=$MALLOC -DFREE=$FREE

if [ "$?" != "0" ]
then
	echo "Scenario compilation failed. Command:" >&2
	echo "gcc -o $EXECUTABLE $SCENARIO -g -std=c99 -lpthread -DALLOCATE=$MALLOC -DFREE=$FREE" >&2
	exit 1
fi

LD_PRELOAD=$ALLOCATOR $EXECUTABLE >&2
if [ "$?" != "0" ]
then
	echo "Test testcase run failed" >&2
	exit 1
fi

cat > $BATCHFILE << EOF
#!/bin/bash

for batch in \`seq $BSIZE\`
do
	LD_PRELOAD=$ALLOCATOR $EXECUTABLE
done
EOF

chmod a+x $BATCHFILE

echo "REAL SYSTEM USER" > $OUTPUTFILE
for sample in `seq $SSIZE`
do
	/usr/bin/time --output $OUTPUTFILE\
				  --format "%e %S %U"\
				  --append\
				  $BATCHFILE
done
python evaluate.py $OUTPUTFILE

rm $EXECUTABLE $BATCHFILE