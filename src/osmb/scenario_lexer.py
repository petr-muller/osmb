import ply.lex as lex

reserved= {
    'memory-limit'  : 'MEMLIMIT',
    'threads'       : 'THREADLIMIT',
    'workjob'       : 'WORKJOB',
    'thread'        : 'THREAD',
    'alloc'         : 'COMM_ALLOC',
    'work'          : 'COMM_WORK',
    'dealloc'       : 'COMM_DEALLOC',
    'read'          : 'WTYPE_READ',
    'write'         : 'WTYPE_WRITE',
    'rw'            : 'WTYPE_RW',
    'wr'            : 'WTYPE_WR',
    'whole'         : 'WPART_WHOLE',
    'random'        : 'WPART_RANDOM',
    'sequential'    : 'WDIR_SEQ',
    'backwards'     : 'WDIR_BACK',
    'does'          : 'DOES',
    'times'         : 'TIMES',
}

tokens = (
  'NUMBER',
  'EQUALS',
  'IDENTIFIER',
  'OPENBRACE',
  'CLOSEBRACE',
) + tuple(reserved.values())

t_EQUALS      = r'='
t_OPENBRACE   = r'\{'
t_CLOSEBRACE  = r'\}'

def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_IDENTIFIER(t):
  r'[a-zA-Z][a-zA-Z0-9\-]*'
  t.type = reserved.get(t.value, 'IDENTIFIER')
  return t

t_ignore = " \t\n"

lexer = lex.lex()
