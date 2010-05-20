#!/usr/bin/python

import Gnuplot
import sys

def simplify(somelist):
  olditem = None
  retlist = []

  for item in somelist:
    if not olditem or item[1] != olditem[1]:
      if olditem:
        retlist.append(olditem)
      retlist.append(item)

    olditem = item

  retlist.append(olditem)

  return retlist[1:]

input = sys.argv[1]
output = sys.argv[2]

fp = open(input, 'r')
line = fp.readline()
g = Gnuplot.Gnuplot()

metric_sys = []
metric_mmap = []
metric_used = []

mmap = oldmmap = 0

startstamp = None

while line:
  line = line.split()

  stamp = int(line[0])
  sys = int(line[1].split(':')[1])
  mmap = int(line[2].split(':')[1])
  used = int(line[3].split(':')[1])

  if not startstamp:
    startstamp = stamp

  metric_mmap.append([stamp-startstamp, mmap])
  metric_used.append([stamp-startstamp, used])
  metric_sys.append([stamp-startstamp, sys])

  line = fp.readline()

fp.close()


mlist = simplify(metric_mmap)
ulist = simplify(metric_used)
slist = simplify(metric_sys)

g('set data style lines')
g.xlabel('time')
g.ylabel('bytes')
mdata = Gnuplot.Data(mlist, title="Memory in mmap()")
udata = Gnuplot.Data(ulist, title="Memory allocated by user program")
sdata = Gnuplot.Data(slist, title="Memory in brk()", with_="linespoints 3 3")
g.plot(mdata, udata, sdata)
g.hardcopy('%s.ps' % output, enhanced=1, color=1)
