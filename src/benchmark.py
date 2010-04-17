#!/usr/bin/python

from optparse import OptionParser
import sys
import tempfile
import subprocess
import os
import osmb

VERBOSE=False
HELPER_PATH='helpers'
TEST_FILE='test.c'
FAKE_LIB='libfakemalloc.c'

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

def probe(name, options):
  probe = osmb.probe.Probe()
  simple_checked_result("Loading the probe", probe.loadProbe(name))

  probe.setScenario(options.scenario)
  probe.setBSize(options.bsize)
  probe.setSSize(options.ssize)
  probe.setMalloc(options.malloc)
  probe.setFree(options.free)
  probe.setAllocator(options.allocator)
  probe.setPythonPath(os.path.join(os.getcwd()))
  
  simple_checked_result("Probe validation", probe.validate())
  simple_checked_result("Probe preparation", probe.prepare())
  simple_checked_result("Probe run", probe.launch())

def command_test(allocator, malloc, free):
  verbose("Testing allocator: %s" % allocator)

  libpath   = tempfile.mkdtemp()
  verbose("Library path: %s" % libpath)
  command = ['gcc', '-shared', '-fPIC', '-std=c99',
             os.path.join(HELPER_PATH,FAKE_LIB),
             '-o', os.path.join(libpath, 'libfakemalloc.so'),
             "-DALLOCATE=%s" % malloc, "-DFREE=%s" % free ]
  simple_checked_command("Compiling fake malloc library", command)
  
  fp, fpath = tempfile.mkstemp()
  os.close(fp)
  verbose("Executable path: %s" % fpath)
  command = ['gcc', os.path.join(HELPER_PATH,TEST_FILE),
             '-o', fpath, '-std=c99',
             "-DALLOCATE=%s" % malloc, "-DFREE=%s" % free,
             '-L%s' % libpath, '-lfakemalloc' ]

  simple_checked_command("Compiling the testcase", command)
  
  testpath = os.path.dirname(allocator)
  verbose("Tested library path: %s" % testpath)
  environment = {'LD_LIBRARY_PATH' : "%s:%s" % (libpath, testpath)}
  verbose("LD_LIBRARY_PATH: %s" % environment["LD_LIBRARY_PATH"])
  
  process = subprocess.Popen(fpath, env=environment, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  process.wait()
  retcode = process.returncode
  stdout,stderr  = process.communicate()
  stdout = stdout.strip()
  stdout = stdout.split('\n')
  print "Running the testcase without the custom allocator".ljust(50),
  if retcode == 0 \
     and stdout.count("Fake malloc") == 1 \
     and stdout.count("Fake free") == 1:
    print "[ PASS ]"
  else:
    print "[ FAIL ]"
    print "stdout:"
    print "\n".join(stdout)
    print "stderr:"
    print stderr
    abort("Running the testcase failed")
  
  environment["LD_PRELOAD"] = allocator
  process = subprocess.Popen(fpath, env=environment,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  process.wait()
  retcode=process.returncode
  stdout,stderr = process.communicate()
  stdout = stdout.strip()
  stdout = stdout.split('\n')
  print "Running the testcase with the custom allocator".ljust(50),
  if retcode == 0 \
      and stdout.count("Fake malloc") == 0\
      and stdout.count("Fake free") == 0:
    print "[ PASS ]"
  else:
    print "[ FAIL ]"
    print "=== stdout ==="
    print "\n".join(stdout)
    print "=== stderr ==="
    print stderr
    abort("Malloc from custom library was not called")

  print "Provided allocator library test passed"

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-a', '--allocator', dest='allocator',
                    help='Path to allocator to test. If not specified, '\
                         ' system library will be used',
                    default=None, metavar='FILE')
  parser.add_option('-v', '--verbose', dest='verbose', default=False,
                    action="store_true", help="More verbose output")
  parser.add_option('-s', '--scenario', dest='scenario', metavar='FILE',
                    help='Scenario file to use', default=None)
  parser.add_option('-m', '--malloc', dest='malloc', default='malloc',
                    help="Name of malloc function in a library",
                    metavar='MALLOC_FUNCTION')
  parser.add_option('-f', '--free', dest='free', default='free',
                    help="Name of free function in a library",
                    metavar='FREE_FUNCTION')
  parser.add_option("-p", "--probe", dest="probe", default=None,
                    help="Probe name", metavar="PROBE")
  parser.add_option("-c", "--count", dest="ssize", default=1,
                    help="Sample size (number of measurements)",
                    metavar="NUMBER")
  parser.add_option("-b", "--bsize", dest="bsize", default=1,
                    help="Batch size (number of executions per measurements)",
                    metavar="NUMBER")
  
  (options, args) = parser.parse_args()
  
  VERBOSE = options.verbose
  
  if len(args) != 1:
    abort("Incorrect number of arguments. Needs exactly one command")

  verbose("Command: %s" % args[0])
  
  command = args[0]
  if command == "test":
    if not options.allocator:
      abort("Test command needs an allocator (-a option)")
    command_test(options.allocator, options.malloc, options.free)

  elif command == "probe":
    if not options.probe:
      abort("Probe command needs a probe (-p option)")
    probe(options.probe, options)