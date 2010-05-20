ALLOCATOR=""
SCENARIO=""
SSIZE=""
BSIZE=""
MALLOC=""
FREE=""
MARG=""
FARG=""
APATH=""
LPATH=""

abort(){
  echo "$1" >&2
  cleanup
  exit 1
}

parse_options(){
  while getopts a:f:s:b:m:d:l:e: o
  do
    case "$o" in
      a) ALLOCATOR="$OPTARG";;
      f) SCENARIO="$OPTARG";;
      s) SSIZE="$OPTARG";;
      b) BSIZE="$OPTARG";;
      m) MALLOC="$OPTARG";;
      d) FREE="$OPTARG";;
      l) MARG="$OPTARG";;
      e) FARG="$OPTARG";;
      [?]) abort "Invalid option: $o";;
    esac
  done
}

check_option(){
  if [ -z $1 ]
  then
    abort "Mandatory argument not supplied: $2"
  fi
}

checked_command(){
  eval "$1"

  if [ "$?" != "0" ]
  then
    echo "$2 failed. Command:" >&2
    echo "$1" >&2
    cleanup
    exit 1
  fi
}

uniquize_allocator(){
  local ALL=$1
  LPATH=`mktemp -d`
  cp "$1" "$LPATH"
  APATH="$LPATH/`basename $1`"
}
