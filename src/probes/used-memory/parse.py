#!/usr/bin/python

import osmb
import sys

class SummaryMemory(osmb.memmodel.Memory):
  def __init__(self):
    osmb.memmodel.Memory.__init__(self)

  def getUserTotal(self):
    total = 0
    for item in self.allocations:
      total += self.allocations[item].getSize()

    return total

  def getSummary(self):
    return "%s SYS:%s MMAP:%s USED:%s\n" % ( self.getTimeStamp(),
                                            self.getHeapSize(),
                                            self.getMmapSize(),
                                            self.getUserTotal() )

memory = SummaryMemory()
input = sys.argv[1]
output = sys.argv[2]

fin   = open(input,'r');
fout  = open(output, 'w');

line = fin.readline().strip()

while line:
  command = osmb.memmodel.Command(line)
  memory.modify(command)
  fout.write(memory.getSummary())
  line = fin.readline().strip()

fin.close()
fout.close()
