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

  def __str__(self):
    return "Workjob [%s]: %i commands" % (self.name, len(self.commands))

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

  def setMemLimit(self, limit):
    self.memlimit = limit

  def setThrLimit(self, limit):
    self.threadCount = limit

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
        "\n".join(self.threads))
