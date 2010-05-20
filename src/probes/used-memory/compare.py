#!/usr/bin/python

import sys
import Gnuplot
import osmb
import operator
import tempfile
import os

def computeData(arg):
  name, filename = arg.split(':')
  startstamp = None

  fp = open(filename, 'r')
  line = fp.readline()

  vals = []
  items = []

  while line:
    stamp, value = line.split()
    stamp = float(stamp)
    value = float(value)

    if startstamp is None:
      startstamp = stamp

    vals.append(value)
    items.append((stamp, value*100.0))

    line = fp.readline()

  mean = (sum(vals)/len(vals)) * 100.0

  return (name, Gnuplot.Data(items, title=name), mean)

if __name__ == "__main__":
  args = sys.argv[1:]

  g = Gnuplot.Gnuplot()
  g("set data style lines")
  g.xlabel('time')
  g.ylabel('used memory percentage [\%]')

  means = {}
  print ""
  print "=" * 80
  for item in args:
    name, gdata, mean = computeData(item)
    g.replot(gdata)
    means[name] = mean

  vals = sorted(means.iteritems(), key=operator.itemgetter(1))
  vals.reverse()
  print "Allocator ordered by means (informational):"
  maxlen = max([len(x) for x in means.keys()])
  for item in vals:
    print "%s: ~%i%%" % (item[0].ljust(maxlen), int(item[1]))

  fd, filename = tempfile.mkstemp(suffix=".ps")
  os.close(fd)
  g.hardcopy(filename, enhanced=1, color=1)
  print "Comparison graph (ps format): %s" % filename
  print "=" * 80
