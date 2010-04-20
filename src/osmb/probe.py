import iniparse
import os
import sys
import re
import subprocess
import tempfile
import time

class ProbeError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class Probe:
  def __init__(self):
    self.options = []
    self.allocator = None
    
    self.scenario = None
    self.scenarioTrans = "bin/scen2C.py"
    self.env = os.environ
    self.nmalloc = "malloc"
    self.nfree = "free"
    self.samplesize = None
    self.batchsize = None
    self.privs = "normal"
    self.needed = []
    self.command = "true"
    
    self.validators = {"ssize" : self.validateSampleSize,
                       "scenario": self.validateScenario,
                       "allocator" : self.validateAllocator,
                       "free" : self.validateFree,
                       "malloc" : self.validateMalloc,
                       "bsize" : self.validateBatchSize }
    
    self.req2cli = {"ssize" : '-s',
                    "bsize" : '-b',
                    "allocator" : '-a',
                    "scenario" : '-f',
                    "malloc" : '-m',
                    "free" : '-d'}
  def req2val(self, req):
    if req == "ssize":
      return str(self.samplesize)
    elif req == "bsize":
      return str(self.batchsize)
    elif req == "free":
      return str(self.nfree)
    elif req == "malloc":
      return str(self.nmalloc)
    elif req == "allocator":
      return str(self.allocator)
    elif req == "scenario":
      return str(self.scenarioAsC)
    
    return None

  def setScenTrans(self, path):
    self.scenarioTrans = path
  
  def setPythonPath(self, pp):
    self.env["PYTHONPATH"] = pp

  def setSSize(self, size):
    self.samplesize = size
    
  def setBSize(self, size):
    self.batchsize = size 
  def setScenario(self, scenario):
    self.scenario = scenario
    
  def setMalloc(self, malloc):
    self.nmalloc = malloc
    
  def setFree(self, free):
    self.nfree = free
    
  def setAllocator(self, allocator):
    self.allocator = allocator

  def loadProbe(self, name):
    self.name = name
    path = os.path.join("probes", name, "%s.probe" % name)
    if not os.path.exists(path):
      print >> sys.stderr, "Probe config file not found: %s" % path
      return False
    
    cfg = iniparse.INIConfig(open(path))
    self.privs = cfg.reqs.privs
    self.needed = cfg.reqs.needed
    self.needed = self.needed.split(',')
    self.command = cfg.run.command
    return True
  
  def validateFree(self):
    if re.match(r"[a-zA-Z][a-zA-Z0-9_]*", self.nfree):
      return True
    else:
      print >> sys.stderr, "Free function name has to be valid C identifier" 
      return False
    
  def validateMalloc(self):
    if re.match(r"[a-zA-Z][a-zA-Z0-9_]*", self.nmalloc):
      return True
    else:
      print >> sys.stderr, "Malloc function name has to be valid C identifier" 
      return False
  
  def validateSampleSize(self):
    try:
      int(self.samplesize)
      return True
    except TypeError:
      print >> sys.stderr, "Sample size must be specified and must be an integer" 
      return False
    except ValueError:
      print >> sys.stderr, "Sample size must be specified and must be an integer" 
      return False

  def validateBatchSize(self):
    try:
      int(self.batchsize)
      return True
    except TypeError:
      print >> sys.stderr, "Batch size must be specified and must be an integer" 
      return False
    except ValueError:
      print >> sys.stderr, "Batch size must be specified and must be an integer" 
      return False

  def validateScenario(self):
    if self.scenario is None:
      print >> sys.stderr, "Probe needs scenario specified"
      return False

    if self.scenario and os.path.exists(self.scenario):
      return True
    else:
      print >> sys.stderr, "Scenario file %s does not exist" % self.scenario
      return False
    
  def validateAllocator(self):
    if self.allocator is None:
      print >> sys.stderr, "Probe needs allocator specified"
      return False

    if os.path.exists(self.allocator):
      return True
    else:
      print >> sys.stderr, "Allocator shared library %s does not exist" % self.allocator
      return False
  
  def validate(self):
    if self.privs != "normal":
      if getpass.getuser() != self.privs:
        print >> sys.stderr, "Bad privileges: need %s, run as %s" % (self.privs, getpass.getuser())
        return False

    for req in self.needed:
      if not self.validators[req]():
        return False
    return True
  
  def prepare(self):
    if 'scenario' in self.needed:
      fd, self.scenarioAsC = tempfile.mkstemp(suffix=".c") 
      pd = subprocess.Popen([self.scenarioTrans, self.scenario],
                            stdout=fd, stderr=subprocess.PIPE, env=self.env)
      pd.wait()
      os.close(fd)
      if pd.returncode != 0:
        print >> sys.stderr, "Scenario translation failed:"
        for line in pd.stderr:
          print >> sys.stderr, line.strip()
        return False

    return True

  def launch(self):
    savePath = os.getcwd()
    os.chdir(os.path.join('probes', self.name))
    command = [self.command]
    for req in self.needed:
      command.extend([self.req2cli[req], self.req2val(req)])
    pd = subprocess.Popen(command,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=self.env)
    
    while pd.poll() is None:
      time.sleep(1)

    os.chdir(savePath)  
    if pd.returncode != 0:
      print >> sys.stderr, "Probe running failed:"
      for line in pd.stderr:
        print >> sys.stderr, line.strip()
      return False
    
    else:
      for line in pd.stdout:
        print line,
    return True
