#!/usr/bin/python

import osmb
import sys

class SummaryMemory(osmb.memmodel.Memory):
  def __init__(self):
    self.counts = {}
    self.counts["alloc"] = 0
    self.counts["dealloc"] = 0
    self.counts["mmap"] = 0
    self.counts["munmap"] = 0
    self.counts["brk"] = 0

    osmb.memmodel.Memory.__init__(self)

    self.commands = { 'malloc' : self.newallocate,
                      'free' : self.deallocate,
                      'mmap' : self.mmap,
                      'munmap': self.munmap,
                      'brk' : self.brk }


  def getSysTotal(self):
    return self.getHeapSize() + self.getMmapSize()

  def getUserTotal(self):
    total = 0
    for item in self.allocations:
      total += self.allocations[item].getSize()

    return total

  def newallocate(self, command):
    self.counts["alloc"] += 1
    osmb.memmodel.Memory.allocate(self, command)

  def deallocate(self, command):
    self.counts["dealloc"] += 1
    osmb.memmodel.Memory.deallocate(self, command)

  def mmap(self, command):
    self.counts["mmap"] += 1
    osmb.memmodel.Memory.mmap(self, command)

  def munmap(self, command):
    self.counts["munmap"] += 1
    osmb.memmodel.Memory.munmap(self, command)

  def brk(self, command):
    self.counts["brk"] += 1
    osmb.memmodel.Memory.brk(self, command)

  def getCountAlloc(self):
    return self.counts["alloc"] / 2

  def getCountDealloc(self):
    return self.counts["dealloc"] / 2

  def getCountMmap(self):
    return self.counts["mmap"] / 2

  def getCountMunmap(self):
    return self.counts["munmap"] / 2

  def getCountBrk(self):
    return self.counts["brk"] / 2

  def getSummary(self):
    return "%s SYS:%s MMAP:%s USED:%s\n" % ( self.getTimeStamp(),
                                            self.getHeapSize(),
                                            self.getMmapSize(),
                                            self.getUserTotal() )

  def getStatistics(self):
    return  "Allocations:     %s\n"\
            "Deallocations:   %s\n\n"\
            "mmap():          %s\n"\
            "munmap():        %s\n"\
            "brk():           %s" % ( self.getCountAlloc(),
                                      self.getCountDealloc(),
                                      self.getCountMmap(),
                                      self.getCountMunmap(),
                                      self.getCountBrk() )

memory = SummaryMemory()
filename = sys.argv[1]
output = sys.argv[2]
fp = open(filename, 'r')
fout = open(output, 'w')

line = fp.readline().strip()
index =1

while line:
  command = osmb.memmodel.Command(line)
  memory.modify(command)
  fout.write(memory.getSummary())
  index += 1
  line = fp.readline().strip()

print memory.getStatistics()

fp.close()
fout.close()
