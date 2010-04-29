import resource
import sys

class Malloc:
  def __init__(self, tid, size, stamp):
    self.tid = tid
    self.size = size
    self.stamp = stamp
    self.address = None

  def setAdress(self, address):
    self.address = address

  def getSize(self):
    return self.size

class Heap:
  def __init__(self):
    self.address = None
    self.size = 0

  def setNewAddress(self, address):
    if self.address is not None:
      self.size += address - self.address

    self.address = address

  def getSize(self):
    return self.size

class MMap:
  def __init__(self, length):
    self.length = length
    self.address = None

  def setAddress(self, address):
    self.address = address

  def getAddress(self):
    return self.address

  def getLength(self):
    return int(self.length)

  def addrIn(self, address):
    min = self.address
    max = self.address + self.length

    return address in xrange(min,max)

  def unmap(self, start, length):
    pagesize = resource.getpagesize()

    if length % pagesize != 0:
      length = ((length / pagesize) + 1) * pagesize
      print length

    prefix = None
    suffix = None

    if start > self.address:
      prefix = MMap(start-self.address)
      prefix.setAddress(self.address)

    end = start + length

    myend = self.address + self.length
    if end < myend:
      suffix = MMap(myend - end)
      suffix.setAddress(end)

    retval = []
    if prefix:
      retval.append(prefix)

    if suffix:
      retval.append(suffix)

    return retval

class Memory:
  def __init__(self):
    self.heap = Heap()
    self.mmaps = {}

    self.allocations = {}
    self.unfinishedAllocations = {}
    self.unfinishedMMaps = {}
    self.unfinishedBrks = {}
    self.unfinishedFrees = {}
    self.timestamp = None

    self.commands = { 'malloc' : self.allocate,
                      'free' : self.deallocate,
                      'mmap' : self.mmap,
                      'munmap': self.munmap,
                      'brk' : self.brk }

  def getHeapSize(self):
    return self.heap.getSize()

  def getMmapSize(self):
    return sum([self.mmaps[x].getLength() for x in self.mmaps ])

  def getTimeStamp(self):
    return self.timestamp

  def allocate(self, command):
    tid = command.getTID()

    if command.getType() == "start":
      size = int(command.getArg())
      stamp = command.getStamp()

      self.unfinishedAllocations[tid] = Malloc(tid,size, stamp)
    elif command.getType() == "end" and tid in self.unfinishedAllocations:
      address = command.getRet()
      if address != "0":
        self.allocations[address] = self.unfinishedAllocations[tid]

      del self.unfinishedAllocations[tid]

  def deallocate(self, command):
    address = command.getArg()
    if command.getType() == "end":
      del self.allocations[address]

  def mmap(self, command):
    type = command.getType()
    tid = command.getTID()
    stamp = command.getStamp()

    if type == "start":
      length = int(command.getArg())
      self.unfinishedMMaps[tid] = MMap(length)
    elif type == "end" and tid in self.unfinishedMMaps:
      address = int(command.getRet())
      if address != -1:
        self.mmaps[address] = self.unfinishedMMaps[tid]
        self.mmaps[address].setAddress(address)

      del self.unfinishedMMaps[tid]

  def munmap(self, command):
    type = command.getType()

    if type == 'end':
      return

    raw = command.getArg()
    start, length = raw.split(',')

    start = int(start)
    length = int(length)

    startaddress = None
    for address in self.mmaps:
      if self.mmaps[address].addrIn(start):
        startaddress = address
        break

    if startaddress:
      map = self.mmaps[startaddress]
      del self.mmaps[startaddress]
      replacements = map.unmap(start, length)

      for map in replacements:
        self.mmaps[map.getAddress()] = map
    else:
      print >> sys.stderr, "munmap() wasn't recognized"

  def brk(self, command):
    type = command.getType()

    if type == "end":
      self.heap.setNewAddress(int(command.getRet()))

  def modify(self, command):
    type = command.getName()
    self.timestamp = command.getStamp()

    self.commands[type](command)

class Command:
  def __init__(self, line):
    line = line.split()
    linedict = {}
    for item in line:
      key, value = item.split(':')
      linedict[key] = value

    self.timestamp  = int(linedict['TS'])
    self.thread     = int(linedict['TID'])
    self.event      = linedict['NAME']
    self.args       = linedict['ARG']
    self.type       = linedict['TYPE']
    self.ret        = linedict['RET']

  def getType(self):
    return self.type

  def getName(self):
    return self.event

  def getTID(self):
    return self.thread

  def getArg(self):
    return self.args

  def getStamp(self):
    return self.timestamp

  def getRet(self):
    return self.ret
