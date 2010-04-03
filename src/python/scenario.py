import ctemplate

class Command:
  pass

class Allocation(Command):
  def __init__(self, ident, amount):
    self.identifier = ident
    self.amount = amount

  def getBefore(self):
    return (self.identifier, False)

  def getAfter(self, before):
    return (self.identifier, True)
  
  def getIdentifier(self):
    return self.identifier
  
  def asC(self):
    return '%s = malloc(%s);' % (self.identifier, self.amount)

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
  
  def getIdentifier(self):
    return self.ident
  
  def asC(self):
    return ''

class Deallocation(Command):
  def __init__(self, ident):
    self.identifier = ident

  def getBefore(self):
    return (self.identifier, True)

  def getAfter(self, before):
    return (self.identifier, False)
  
  def getIdentifier(self):
    return self.identifier
  
  def asC(self):
    return 'free(%s);' % self.identifier

class Workjob:
  def __init__(self, name):
    self.name = name
    self.commands = []
    self.valid = False
    self.messages = []

  def addCommand(self, command):
    self.commands.append(command)

  def validate(self, memlimit):
    self.valid = True
    errors = []
    allocated = {}
    for command in self.commands:
      id, before = command.getBefore()
      if allocated.get(id, False) != before:
        self.messages.append('Workjob %s: command "%s" in wrong state (unallocated)' % (self.name, command))
        self.valid = False
      id, after = command.getAfter(before)
      allocated[id] = after

    return errors
  
  def isValid(self):
    return self.valid
  
  def getMessages(self):
    return self.messages

  def getID(self):
    return self.name

  def getMaxMem(self):
    return 0

  def __str__(self):
    return "Workjob [%s]: %i commands" % (self.name, len(self.commands))

class Thread:
  def __init__(self, threadId, workjob, reps):
    self.id = threadId
    self.workjob = workjob
    self.repetitions = reps
    self.valid = False

  def __str__(self):
    return "Thread %s: workjob %s" % (self.id, self.workjob.name)

  def validate(self, memlimit):
    errors = self.workjob.validate(memlimit)
    return errors
  
  def isValid(self):
    return self.workjob.isValid()
  
  def getMessages(self):
    return self.workjob.getMessages()

  def getMaxMem(self):
    return self.workjob.getMaxMem()

class Scenario:
  def __init__(self, memlimit=524288, threads=1):
    self.memlimit = memlimit
    self.threadCount  = threads

    self.threads = []
    self.workjobs = {}
    self.memoryOver = False
    self.valid = False
    self.messages = ['Scenario was not validated']

  def setMemLimit(self, limit):
    self.memlimit = limit

  def setThrLimit(self, limit):
    self.threadCount = limit

  def addWorkjob(self, workjob):
    self.workjobs[workjob.getID()] = workjob

  def addThread(self, thread):
    self.threads.append(thread)

  def isValid(self):
    return self.valid
  
  def getMessages(self):
    return self.messages

  def validate(self):
    self.valid = True
    memorySum = 0

    for thread in self.threads:
      thread.validate(self.memlimit)
      if not thread.isValid():
        self.messages.append(thread.getMessages())
        self.valid = False
      memorySum += thread.getMaxMem()
        
    if memorySum > self.memlimit:
      self.messages.append("Threads can consume more memory than limit: %s > %s" % (memorySum, self.memlimit))
      self.valid = False
      
  def translateToC(self):
    source =  ctemplate.getHeader(self.memlimit, self.threadCount)
    source += ctemplate.getWorkjobs(self.threads)
    source += ctemplate.getMain(self.threads)
    return source 

  def __str__(self):
    return """Memory limit: %i
Threads: %i
===============================================================================
Workjobs:
%s
===============================================================================
Threads:
%s
""" % ( self.memlimit,
        self.threadCount,
        "\n".join(["%s" % x for x in self.workjobs.values()]),
        "\n".join(['%s' % x for x in self.threads]))
