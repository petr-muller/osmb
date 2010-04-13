import metric
import dataset
import sys

filename = sys.argv[1]

dset = dataset.Dataset(filename)

userMetric    = metric.Metric("User time", dset.getList("USER"))
realMetric    = metric.Metric("Real time", dset.getList("REAL"))
systemMetric  = metric.Metric("System time", dset.getList("SYSTEM"))
totalMetric   = metric.Metric("Total CPU time", dset.getSumList(["USER", "SYSTEM"]))

print userMetric.statDetails()
print realMetric.statDetails()
print systemMetric.statDetails()
print totalMetric.statDetails()

fp = open(filename, 'r')
for line in fp.readlines():
  print line.strip()
fp.close()