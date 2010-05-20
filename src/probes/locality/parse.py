#!/usr/bin/python

import osmb
import sys

class MemDistance:
  def __init__(self, start1, start2, len1, len2):
    if start1 > start2:
      gap = start1 - (start2 + len2)
    else:
      gap = start2 - (start1 + len1)

    if gap < 0:
      print gap

    self.gap      = gap
    self.relative = float(len1+len2+gap) / float(len1+len2)

  def asTT(self):
    return "%s:%s" % ( self.gap, self.relative)


class LocalityMemory(osmb.memmodel.Memory):
  def __init__(self):
    osmb.memmodel.Memory.__init__(self)
    self.locthread = {}
    self.lastalloc = {}

    self.commands["malloc"] = self.allocate

  def getLocalityReport(self):
    lengths = [ len(x) for x in self.locthread.values() ]
    if len(lengths) > 0:
      maxlen = max( [ len(x) for x in self.locthread.values() ])
    else:
      maxlen = 0
    retval = ""

    for index in xrange(maxlen):
      line = []
      for key in self.locthread:
        if index < len(self.locthread[key]):
          line.append(self.locthread[key][index].asTT())
        else:
          line.append('-')
      line = ' '.join(line)
      retval += "%s\n" % line

    return retval

  def addAllocation(self, allocation):
    osmb.memmodel.Memory.addAllocation(self, allocation)

    tid = allocation.getTid()

    if tid not in self.locthread:
      self.locthread[tid] = []

    if tid not in self.lastalloc:
      self.lastalloc[tid] = allocation
    else:
      la = self.lastalloc[tid]
      self.locthread[tid].append(MemDistance( la.getAddress(),
                                              allocation.getAddress(),
                                              la.getSize(),
                                              allocation.getSize()))
      self.lastalloc[tid] = allocation

  def removeAllocation(self, address):
    alloc = self.allocations[address]
    tid = alloc.getTid()
    if tid in self.lastalloc:
      if self.lastalloc[tid].getAddress() == address:
        del self.lastalloc[tid]

    osmb.memmodel.Memory.removeAllocation(self, address)

memory = LocalityMemory()
input = sys.argv[1]
output = sys.argv[2]

fin   = open(input,'r');
fout  = open(output, 'w');

line = fin.readline().strip()

while line:
  command = osmb.memmodel.Command(line)
  memory.modify(command)
  line = fin.readline().strip()

fout.write(memory.getLocalityReport())
fin.close()
fout.close()
