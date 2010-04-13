
class Dataset:
  def __init__(self, filename):
    fp = open(filename, "r")
    header = fp.readline()
    self.headers = header.split()
    self.datalines = []
    
    line = fp.readline()
    while line:
      self.datalines.append([ float(x) for x in line.split()])
      line = fp.readline()
    fp.close()

  def getList(self, id):
    index = self.headers.index(id)
    return [ x[index] for x in self.datalines]
  
  def getSumList(self, ids):
    indexes = [self.headers.index(id) for id in ids ]
    return [ sum([line[x] for x in indexes ]) for line in self.datalines  ]