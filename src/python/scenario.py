class CommandFactory:
  def createAllocation(self, cmdlist):
    iden = cmdlist[1]
    amount = cmdlist[2]

    command = Allocation(iden, amount)
    if len(cmdlist) > 3:
      if cmdlist[3] == "by":
        command.setUnitLength(cmdlist[4])
      else:
        #TODO: FIX THE ERROR REPORTING WHEN PARSING
        raise ValueError("Crapz0r")

    return command

  def createWork(self, cmdlist):
    type = cmdlist[1]
    amount = cmdlist[2]
    ident = cmdlist[3]
    direction = cmdlist[4]

    return Work(type, amount, ident, direction)

  def createDeallocation(self, cmdlist):
    return Deallocation(cmdlist[1])

  def __init__(self):
    self.knownCommands = {}

    self.knownCommands["alloc"] = self.createAllocation
    self.knownCommands["work"] = self.createWork
    self.knownCommands["dealloc"] = self.createDeallocation

  def parseLine(self, line):
    commandList = line.split()
    cmdKeyword = commandList[0]

    return self.knownCommands[cmdKeyword](commandList)

class Command:
  pass

class Allocation(Command):
  def __init__(self, ident, amount):
    self.identifier = ident
    self.amount = amount
    self.unitLength = 1

  def setUnitLength(self, length):
    self.unitLength = length

  def getBefore(self):
    return (self.identifier, False)

  def getAfter(self, before):
    return (self.identifier, True)

class Work(Command):
  def __init__(self, type, amount, ident, direction):
    self.type = type
    self.amount = amount
    self.ident = ident
    self.direction = direction

  def getBefore(self):
    return (self.ident, True)

  def getAfter(self, before):
    return (self.ident, before)

class Deallocation(Command):
  def __init__(self, ident):
    self.identifier = ident

  def getBefore(self):
    return (self.identifier, True)

  def getAfter(self, before):
    return (self.identifier, False)

class Workjob:
  def __init__(self, name):
    self.name = name
    self.commands = []

  def addCommand(self, command):
    self.commands.append(command)

  def validate(self, memlimit):
    errors = []
    allocated = {}
    for command in self.commands:
      id, before = command.getBefore()
      if allocated.get(id, False) != before:
        print "Kaboom"
      id, after = command.getAfter(before)
      allocated[id] = after

    return errors

  def getID(self):
    return self.name

  def getMaxMem(self):
    return 0

class Thread:
  def __init__(self, threadId, workjob, reps):
    self.id = threadId
    self.workjob = workjob
    self.repetitions = reps

  def __str__(self):
    return "Thread %s" % self.id

  def validate(self, memlimit):
    errors = self.workjob.validate(memlimit)
    return errors

  def getMaxMem(self):
    return self.workjob.getMaxMem()

class Scenario:
  def __init__(self, memlimit=524288, threads=1):
    self.memlimit = memlimit
    self.threadCount  = threads

    self.threads = []
    self.workjobs = {}
    self.memoryOver = False

  def readFrom(self, file):
    lines = file.readlines()

    for line in lines:
      parsed = line.split()
      if len(parsed) == 0:
        continue
      drive = parsed[0]
      if drive == "memory-limit":
        self.memlimit = parsed[2]
      elif drive == "threads":
        self.thread = parsed[2]
      elif drive == "workjob":
        pass
      elif drive == "thread":
        pass
      else:
        raise ValueError("Naka mrdka: %s" % drive)

  def addWorkjob(self, workjob):
    self.workjobs[workjob.getID()] = workjob

  def addThread(self, thread):
    self.threads.append(thread)

  def validate(self):
    threadMemory = []
    errors = []
    for thread in self.threads:
      threrrors = thread.validate(self.memlimit)
      if len(threrrors) > 0:
        for error in threrrors:
          print >> sys.stderr, "%s: %s" % (thread, error)
        self.memoryOver = True

      threadMemory.append(thread.getMaxMem())

    totalMem = sum(threadMemory)
    if totalMem > self.memlimit:
      print >> sys.stderr, "Threads can consume more memory than limit: %s > %s" % (totalMem, self.memlimit)
      self.memoryOver = False
