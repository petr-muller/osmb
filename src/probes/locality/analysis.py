#!/usr/bin/python

import sys
import Gnuplot
import osmb
import scipy.stats

class HistogramMetric(osmb.metric.Metric):
  def getModus(self):
    ret = scipy.stats.mode(self.values)
    return ret

  def getPctLesser(self, treshold):
    count = len([ x for x in self.values if x <= treshold ])
    total = len(self.values)

    return (float(count) / float(total)) * 100.0

fin = open(sys.argv[1], 'r')
fout_plotabs_filename = sys.argv[2]
fout_plotrel_filename = sys.argv[3]

line = fin.readline().strip()
line = line.split()

absolutes = []
relatives = []
for x in xrange(len(line)):
  absolutes.append([])
  relatives.append([])

index = 0
for item in line:
  if item != "-":
    abs,rel = item.split(':')
    abs=int(abs)
    rel=float(rel)
    absolutes[index].append(abs)
    relatives[index].append(rel)
  index+=1

line = fin.readline().strip()
while line:
  line = line.split()
  index = 0
  for item in line:
    if item != "-":
      abs,rel = item.split(':')
      abs=int(abs)
      rel=float(rel)
      absolutes[index].append(abs)
      relatives[index].append(rel)
    index+=1
  line = fin.readline().strip()

absmetrics = []
relmetrics = []
for metric in xrange(len(absolutes)):
  if len(absolutes[metric]) != 0:
    absmetrics.append(HistogramMetric("Thread %s absolute" % metric, absolutes[metric]))
    relmetrics.append(osmb.metric.Metric("Thread %s relative" % metric, relatives[metric]))

for abs in absmetrics:
  print abs.nonNormalStatDetails()
  mode = abs.getModus()
  for i in range(len(mode[0])):
    print "Absolute distance modus:           %i bytes (%i/%i)" % (mode[0][i], mode[1][i], abs.getTotal())
  print "Percentage gaps lesser than 64B:   %.1f%%" % abs.getPctLesser(64)
  print "Percentage gaps lesser than 128B:  %.1f%%" % abs.getPctLesser(128)
  print "Percentage gaps lesser than 1KB:   %.1f%%" % abs.getPctLesser(1024)
  print "Percentage gaps lesser than 4KB:   %.1f%%" % abs.getPctLesser(4092)
  print ""
print "-" * 80

for rel in relmetrics:
  print rel.nonNormalStatDetails()

absdata = []
for metric in absmetrics:
  data = metric.getList()
  name = metric.getName()
  absdata.append(Gnuplot.Data(metric.getList(), title=metric.getName()))

reldata = []
for metric in relmetrics:
  data = metric.getList()
  name = metric.getName()
  reldata.append(Gnuplot.Data(metric.getList(), title=metric.getName()))

g = Gnuplot.Gnuplot()

g('set data style linespoints')
g.xlabel("Bytes")
g.ylabel("Order")
for metric in absdata:
  g.replot(metric)
g.hardcopy(fout_plotabs_filename, enhanced=1, color=1)

g.reset()
g('set data style linespoints')
g.xlabel("Ratio")
g.ylabel("Order")
for metric in reldata:
  g.replot(metric)
g.hardcopy(fout_plotrel_filename, enhanced=1, color=1)

