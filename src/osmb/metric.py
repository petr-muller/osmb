import scipy.stats
import numpy
import sys

class Metric:
  def __init__(self, name, list):
    self.values = list
    self.name=name

  def getList(self):
    return self.values

  def getName(self):
    return self.name

  def getTotal(self):
    return len(self.values)

  def getFormatNonNormalTuple(self):
    return (self.name,
            numpy.mean(self.values),
            scipy.stats.tstd(self.values),
            scipy.stats.tsem(self.values),
            scipy.stats.tmin(self.values),
            scipy.stats.scoreatpercentile(self.values, 25),
            scipy.stats.scoreatpercentile(self.values, 50),
            scipy.stats.scoreatpercentile(self.values, 75),
            scipy.stats.tmax(self.values, None))

  def getFormatNormalTuple(self):
    mean = numpy.mean(self.values)
    sem = scipy.stats.tsem(self.values)

    rse = sem/mean;

    #RSE sufficiency treshold = 3%
    if rse > 0.03:
      sufficiency = "insufficient"
    else:
      sufficiency = "sufficient"


    return (self.name,
            mean, scipy.stats.tstd(self.values),
            sem, rse, sufficiency,
            scipy.stats.tmin(self.values),
            scipy.stats.scoreatpercentile(self.values, 25),
            scipy.stats.scoreatpercentile(self.values, 50),
            scipy.stats.scoreatpercentile(self.values, 75),
            scipy.stats.tmax(self.values, None))

  def normalStatDetails(self):
    return  "Statistics:  %s (assumed normal distribution)\n"\
            "Mean:                    %8f\n"\
            "Standard deviation:      %8f\n"\
            "Standard error:          %8f\n"\
            "Relative standard error: %8f (%s)\n"\
            "Min       Q1        Median    Q3        Max       \n"\
            "---       --        ------    --        ---\n"\
            "%8f  %8f  %8f  %8f  %8f\n" % self.getFormatNormalTuple()

  def nonNormalStatDetails(self):
    return  "Statistics:  %s\n"\
            "Mean:                %8f\n"\
            "Standard deviation:  %8f\n"\
            "Standard error:      %8f\n"\
            "Min       Q1        Median    Q3        Max       \n"\
            "---       --        ------    --        ---\n"\
            "%8f  %8f  %8f  %8f  %8f\n" % self.getFormatNonNormalTuple()



