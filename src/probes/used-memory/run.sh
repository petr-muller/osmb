#!/bin/bash

cleanup(){
  rm -rf $LPATH $OUTPUTFILE $EXECUTABLE $GSN $MS $GREPPEDOUT $MEMMODEL
}

. ../commonlib.sh
parse_options $@

check_option "$ALLOCATOR" "allocator"
check_option "$SCENARIO" "scenario"
check_option "$MALLOC" "malloc function name"
check_option "$FREE" "free function name"
check_option "$MARG" "malloc argument"
check_option "$FARG" "free argument"

uniquize_allocator $ALLOCATOR

OUTPUTFILE=`mktemp`
EXECUTABLE=`mktemp`
touch /tmp/been
checked_command "gcc -o $EXECUTABLE $SCENARIO -std=c99 $APATH -lpthread -DALLOCATE=$MALLOC -DFREE=$FREE" "Scenario compilation"
touch /tmp/here

GSN=`mktemp`
checked_command "gcc -o $GSN get_syscall_numbers.c -std=c99" "Helper compilation"

MS=`mktemp`
checked_command "cp malloc-syscall.stp $MS"   "Modifying the stap script"
checked_command "sed -i 's|MARG|$MARG|g' $MS" "Modifying the stap script"
checked_command "sed -i 's|FARG|$FARG|g' $MS" "Modifying the stap script"

PID=$(stap $MS $APATH $EXECUTABLE `$GSN` $MALLOC $FREE -o $OUTPUTFILE -F)

if [ -z "$PID" ]
then
  abort "Stap command was not successful"
fi

checked_command "LD_PRELOAD=$APATH $EXECUTABLE" "Running the testcase"
checked_command "kill -INT $PID" "Stopping systemtap daemon"

while [ "`ps -o comm= -p $PID`" == "stap" ]
do
  sleep 1
done
sleep 1

GREPPEDOUT=`mktemp`
grep TYPE $OUTPUTFILE > $GREPPEDOUT
rm -f $OUTPUTFILE

echo "==============================================================================="

MEMMODEL=`mktemp`
checked_command "./parse.py $GREPPEDOUT $MEMMODEL" "Memory image construction"
rm -f $GREPPEDOUT

PLOT_TIME=`mktemp`
TEXT_RATIOS=`mktemp`
checked_command "./analysis.py $MEMMODEL $PLOT_TIME $TEXT_RATIOS" "Data analysis"
rm -rf $MEMMODEL

mv $PLOT_TIME $PLOT_TIME.ps
mv $TEXT_RATIOS $TEXT_RATIOS.txt

echo "Used memory ratio in time plot:      $PLOT_TIME.ps"
echo "Used memory ratio in time raw data:  $TEXT_RATIOS.txt"

cleanup

echo "==============================================================================="
exit 0
