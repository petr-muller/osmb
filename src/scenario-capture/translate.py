#!/usr/bin/python

import tempfile
import os
import sys

class Alloc:
  def __init__(self, ident, size, address):
    self.ident = ident
    self.size = size
    self.address = address

  def asScenCommand(self):
    return "alloc %s %s" % (self.ident, self.size)

class Free:
  def __init__(self, ident):
    self.ident = ident

  def asScenCommand(self):
    return "dealloc %s" % (self.ident)

class Thread:
  def __init__(self, tid):
    self.allocations = {}
    self.actions = []
    self.counter = 0
    self.base ="IDENT"
    self.tid = tid

  def addMalloc(self, command):
    size = command["SIZE"]
    address = command["RETURN"]
    ident = self.base + str(self.counter)

    self.counter += 1

    self.actions.append(Alloc(ident, size, address))
    self.allocations[address] = ident

  def addFree(self, command):
    address = command["POINTER"]
    if address in self.allocations:
      self.actions.append(Free(self.allocations[address]))
      del self.allocations[address]

  def asWorkjob(self):
    retval = "workjob wj%s = {\n" % self.tid
    retval += "\n".join([x.asScenCommand() for x in self.actions])
    retval += "\n}\n"
    retval += "thread %s does workjob wj%s times 1\n" % (self.tid, self.tid)
    return retval

class Scenario:
  def __init__(self):
    self.threads = {}

  def addMalloc(self, command):
    tid = command["TID"]

    if tid not in self.threads:
      self.threads[tid] = Thread(tid)

    self.threads[tid].addMalloc(command)

  def addFree(self, command):
    tid = command["TID"]
    if tid not in self.threads:
      self.threads[tid] = Thread(tid)
    self.threads[tid].addFree(command)

  def asScenario(self):
    return "\n".join([self.threads[x].asWorkjob() for x in self.threads ])

class Memory:
  def __init__(self):
    self.pids = {}

  def createScenarios(self):
    counter = 0
    handle, filename = tempfile.mkstemp()
    os.close(handle)
    retval = []
    for pid in self.pids:
      pidfile = filename + str(pid)
      fp = open(pidfile, 'w')
      fp.write(self.pids[pid].asScenario())
      fp.close
      retval.append(pidfile)
    return retval

  def parseLine(self,line):
    line = line.split()

    if len(line) not in (4,5) or line[0] not in ("MALLOC", "FREE"):
      return

    type = line[0]
    command = {}
    for item in line[1:]:
      key,value = item.split('=')
      value = value
      command[key] = value

    pid = command["PID"]
    if pid not in self.pids:
      self.pids[pid] = Scenario()

    if type == "MALLOC":
      self.pids[pid].addMalloc(command)
    else:
      self.pids[pid].addFree(command)

fp = open(sys.argv[1], 'r')

memory = Memory()
line = fp.readline()
while line:
  memory.parseLine(line)
  line = fp.readline()
fp.close()
files = memory.createScenarios()
print "\n".join(files)
