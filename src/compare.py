#!/usr/bin/python

from optparse import OptionParser
import sys
import tempfile
import subprocess
import os
import osmb

VERBOSE=False
HELPER_PATH='helpers'

def verbose(message):
  global VERBOSE
  if VERBOSE:
    print message

def abort(message):
  print >> sys.stderr, "ERROR: %s" % message
  sys.exit(1)

def simple_checked_command(message, command):
  print message.ljust(50),
  comp_result = subprocess.call(command)

  if comp_result == 0:
    print "[ PASS ]"
  else:
    print "[ FAIL ]"
    abort(message)

def simple_checked_result(message, result):
  print message.ljust(50),

  if result:
    print "[ PASS ]"
  else:
    print "[ FAIL ]"
    abort(message)

def probe_compare(name, args):
  probe = osmb.probe.Probe()
  probe.setPythonPath(os.path.join(os.getcwd()))
  simple_checked_result("Loading the probe", probe.loadProbe(name))
  simple_checked_result("Probe comparation", probe.compare(args))

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-v', '--verbose', dest='verbose', default=False,
                    action="store_true", help="More verbose output")
  parser.add_option("-p", "--probe", dest="probe", default=None,
                    help="Probe name", metavar="PROBE")

  (options, args) = parser.parse_args()

  VERBOSE = options.verbose

  if not options.probe:
    print >> sys.stderr, "Probe argument needed"
    sys.exit(1)

  if len(args) < 2:
    print >> sys.stderr, "Need at least two data files to compare"
    sys.exit(1)

  probe_compare(options.probe, args)

