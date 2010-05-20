#!/bin/bash

cleanup(){
  rm -rf $LPATH $MS $GSN $EXECUTABLE $OUTPUTFILE $GREPPEDOUT $LOCREPORT
}

. ../commonlib.sh

parse_options $@

check_option "$ALLOCATOR" "allocator"
check_option "$SCENARIO" "scenario"
check_option "$MALLOC" "malloc function name"
check_option "$FREE" "free function name"
check_option "$MARG" "malloc argument"
check_option "$FARG" "free argument"

OUTPUTFILE=`mktemp`
EXECUTABLE=`mktemp`
GSN=`mktemp`
MS=`mktemp`

uniquize_allocator $ALLOCATOR

checked_command "gcc -o $EXECUTABLE $SCENARIO -std=c99 $APATH -lpthread -DALLOCATE=$MALLOC -DFREE=$FREE" "Scenario compilation"
checked_command "gcc -o $GSN get_syscall_numbers.c -std=c99" "Helper compilation"

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

LOCREPORT=`mktemp`
checked_command "./parse.py $GREPPEDOUT $LOCREPORT" "Computing locality"

PLOT_LOCABS=`mktemp`
PLOT_LOCREL=`mktemp`
checked_command "./analysis.py $LOCREPORT $PLOT_LOCABS $PLOT_LOCREL" "Data analysis"

mv $PLOT_LOCABS $PLOT_LOCABS.ps
mv $PLOT_LOCREL $PLOT_LOCREL.ps

echo "Absolute locality plot:      $PLOT_LOCABS.ps"
echo "Relative locality plot:      $PLOT_LOCREL.ps"

cleanup

echo "==============================================================================="
exit 0
