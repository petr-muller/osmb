#!/usr/bin/python

import sys
import Gnuplot
import osmb

def parse_line(line):
  line = line.split()

  stamp = int(line[0])

  for item in line[1:]:
    name,value = item.split(':')
    value = int(value)

    if name == 'SYS':
      heap = value
    elif name == "MMAP":
      mmap = value
    elif name == "USED":
      used = value

  return (stamp, heap+mmap, used)

fin = open(sys.argv[1], 'r')
fout_plot_filename = sys.argv[2]
fout_raw = open(sys.argv[3], 'w')

line = fin.readline().strip()

ratios = []
ratios_in_time = []

startstamp = None

while line:
  stamp, total, busy = parse_line(line)
  if startstamp is None:
    startstamp = stamp

  stamp = stamp - startstamp
  line = fin.readline().strip()

  if total != 0:
    ratio = float(busy)/float(total)
    fout_raw.write("%s %s\n" % (stamp, ratio))

    ratios.append(ratio)
    ratios_in_time.append((stamp, ratio*100))

fout_raw.close()


ratioMetric = osmb.metric.Metric("Used memory ratio", ratios)
print ratioMetric.nonNormalStatDetails()
g = Gnuplot.Gnuplot()
g('set data style lines')
g.xlabel('time')
g.ylabel('used memory percentage [\%]')
g.plot(ratios_in_time)
g.hardcopy(fout_plot_filename, enhanced=1, color=1)
