import ply.yacc as yacc

from scenario_lexer import tokens
import scenario

class Statement:
  def __init__(self, type, data):
    self.type = type
    self.data = data

def p_scenario(p):
  'scenario : fstatement_list'
  scen = scenario.Scenario()

  for fstatement in p[1]:
    if   fstatement.type == "MEMLIMIT":
      scen.setMemLimit(fstatement.data)
    elif fstatement.type == "THRLIMIT":
      scen.setThrLimit(fstatement.data)
    elif fstatement.type == "WJ":
      scen.addWorkjob(fstatement.data)
    elif fstatement.type == "THDEF":
      thread = fstatement.data
      wjname = thread.workjob
      wj = scen.workjobs[wjname]
      thread.workjob = wj
      scen.addThread(thread)

  p[0] = scen

def p_fstatenent_list(p):
  """fstatement_list : fstatement fstatement_list
                     | fstatement"""
  p[0] = []
  p[0].append(p[1])
  if len(p) == 3:
    p[0].extend(p[2])

def p_fstatement(p):
  """fstatement : fstatement_memlimit
                | fstatement_threadlimit
                | fstatement_wjdef
                | fstatement_thdef"""
  p[0] = p[1]

def p_fstatement_memlimit(p):
  """fstatement_memlimit : MEMLIMIT EQUALS NUMBER"""
  p[0] = Statement("MEMLIMIT", p[3])

def p_fstatement_threadlimit(p):
  """fstatement_threadlimit : THREADLIMIT EQUALS NUMBER"""
  p[0] = Statement("THRLIMIT", p[3])

def p_fstatement_wjdef(p):
  """fstatement_wjdef : WORKJOB IDENTIFIER EQUALS OPENBRACE command_list CLOSEBRACE"""
  job = scenario.Workjob(p[2])
  for comm in p[5]:
    job.addCommand(comm)
  p[0] = Statement("WJ", job)

def p_command_list(p):
  """command_list : command command_list
                  | command"""
  p[0] = []
  p[0].append(p[1])
  if len(p) == 3:
    p[0].extend(p[2])

def p_command(p):
  """command : comm_alloc
             | comm_work
             | comm_dealloc"""
  p[0] = p[1]

def p_comm_alloc(p):
  """comm_alloc : COMM_ALLOC IDENTIFIER NUMBER"""
  p[0] = scenario.Allocation(p[2], p[3])

def p_comm_work(p):
  """comm_work : COMM_WORK work_type work_part IDENTIFIER work_dir"""
  p[0] = scenario.Work(p[2], p[3], p[4], p[5])

def p_comm_dealloc(p):
  """comm_dealloc : COMM_DEALLOC IDENTIFIER"""
  p[0] = scenario.Deallocation(p[2])

def p_work_type(p):
  """work_type : WTYPE_READ
               | WTYPE_WRITE
               | WTYPE_RW
               | WTYPE_WR"""
  p[0] = p[1]

def p_work_part(p):
  """work_part : WPART_WHOLE
               | WPART_RANDOM"""
  p[0] = p[1]

def p_work_dir(p):
  """work_dir : WDIR_SEQ
              | WDIR_BACK
              | WPART_RANDOM"""
  p[0] = p[1]
  
def p_fstatement_thdef(p):
  """fstatement_thdef : THREAD NUMBER DOES WORKJOB IDENTIFIER TIMES NUMBER"""
  p[0] = Statement("THDEF", scenario.Thread(p[2], p[5], p[7]))

def p_error(p):
  print "Syntax error in input!"

def parseScenario(fp):
  parser = yacc.yacc()
  contents = fp.read()
  result = parser.parse(contents)

  return result
