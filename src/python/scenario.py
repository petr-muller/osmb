class Command:
  pass

class Allocation(Command):
  pass

class Work(Command):
  pass

class Deallocation(Command):
  pass

class Workjob:
  pass

class Thread:
  pass

class Scenario:
  def __init__(self, memlimit, threads):
    pass

  def readFrom(self, file):
    pass
