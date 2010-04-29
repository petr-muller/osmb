#!/usr/bin/python

import osmb
import sys

class SummaryMemory(osmb.memmodel.Memory):
  def getSysTotal(self):
    return self.getHeapSize() + self.getMmapSize()

  def getUserTotal(self):
    total = 0
    for item in self.allocations:
      total += self.allocations[item].getSize()

    return total

  def getSummary(self):
    return "%s SYS:%s MMAP:%s USED:%s" % ( self.getTimeStamp(),
                                            self.getHeapSize(),
                                            self.getMmapSize(),
                                            self.getUserTotal() )

memory = SummaryMemory()
filename = sys.argv[1]
fp = open(filename, 'r')

line = fp.readline().strip()
index =1
while line:
  command = osmb.memmodel.Command(line)
  memory.modify(command)
  print memory.getSummary()
  print >> sys.stderr, "%s\r" % index,
  index += 1
  line = fp.readline().strip()

fp.close()
