import sys
import osmb

filename = sys.argv[1]

dset = osmb.dataset.Dataset(filename)

userMetric    = osmb.metric.Metric("User time", dset.getList("USER"))
realMetric    = osmb.metric.Metric("Real time", dset.getList("REAL"))
systemMetric  = osmb.metric.Metric("System time", dset.getList("SYSTEM"))
totalMetric   = osmb.metric.Metric("Total CPU time", dset.getSumList(["USER", "SYSTEM"]))
print "=" * 80
print userMetric.statDetails()
print realMetric.statDetails()
print systemMetric.statDetails()
print totalMetric.statDetails()

fp = open(filename, 'r')
for line in fp.readlines():
  print line.strip()
fp.close()
print "=" * 80