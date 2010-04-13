import scipy.stats
import numpy

class Metric:
  def __init__(self, name, list):
    self.values = list
    self.name=name
    
  def getFormatTuple(self):
    return (self.name,
            numpy.mean(self.values),
            scipy.stats.tstd(self.values),
            scipy.stats.tsem(self.values),
            scipy.stats.tmin(self.values),
            scipy.stats.scoreatpercentile(self.values, 25),
            scipy.stats.scoreatpercentile(self.values, 50),
            scipy.stats.scoreatpercentile(self.values, 75),
            scipy.stats.tmax(self.values, None))
  
  def statDetails(self):
    return  "Statistics:  %s\n"\
            "Mean:                %8f\n"\
            "Standard deviation:  %8f\n"\
            "Standard error:      %8f\n"\
            "Min       Q1        Median    Q3        Max       \n"\
            "---       --        ------    --        ---\n"\
            "%8f  %8f  %8f  %8f  %8f\n" % self.getFormatTuple()               