#!/bin/bash

ALLOCATOR=""
SCENARIO=""
MALLOC=""
FREE=""

abort(){
	echo "$1" >&2
	exit 1
}

cleanup(){
  rm -f $EXECUTABLE $GSN $OUTPUTFILE $MEMMODEL $PLOT
}

checked_command(){
  $1

  if [ "$?" != "0" ]
  then
    echo "$2 failed. Command:" >&2
    echo "$1" >&2
    cleanup
    exit 1
  fi
}

while getopts a:f:s:b:m:d: o
do
	case "$o" in
		a) ALLOCATOR="$OPTARG";;
		f) SCENARIO="$OPTARG";;
		m) MALLOC="$OPTARG";;
		d) FREE="$OPTARG";;
		[?]) echo "Invalid option: $o" >&2; exit 1;;
	esac
done

if  [ -z "$ALLOCATOR" ] || [ -z "$SCENARIO" ] || [ -z "$MALLOC" ] || [ -z "$FREE" ]
then
	abort "Not all of mandatory options were supplied"
fi


OUTPUTFILE=`mktemp`
EXECUTABLE=`mktemp`
checked_command "gcc -o $EXECUTABLE $SCENARIO -std=c99 -lpthread -DALLOCATE=$MALLOC -DFREE=$FREE" "Scenario compilation"

GSN=`mktemp`
checked_command "gcc -o $GSN get_syscall_numbers.c -std=c99" "Helper compilation"


checked_command "stap malloc-syscall.stp -c $EXECUTABLE $ALLOCATOR $EXECUTABLE `$GSN` -o $OUTPUTFILE" "Trace collection"

MEMMODEL=`mktemp`
checked_command "./parse.py $OUTPUTFILE > $MEMMODEL" "Memory image construction"

PLOT=`mktemp`
checked_command "./plotta.py $MEMMODEL $PLOT" "Plot generation"

cleanup

exit 0
