from datetime import date

def getHeader(ml, tl):
  return '// Malloc benchmark file generated on %s\n' \
         '// Limits:\n'\
         '//   Memory limit: %s\n' \
         '//   Threads:      %s\n' \
         '#include <stdlib.h>\n' \
         '#include <pthread.h>\n\n'\
         '#ifndef ALLOCATE\n'\
         '  #define ALLOCATE malloc\n'\
         '#endif\n\n'\
         '#ifndef FREE\n'\
         '  #define FREE free\n'\
         '#endif\n\n'\
         'void *ALLOCATE(size_t);\n'\
         'void FREE(void *ptr);\n' % (date.today(), ml, tl)

def getLoopBody(thread):
  ids = []
  loopbody = ''
  for command in thread.workjob.commands:
    if command.getIdentifier() in ids:
      loopbody += '%s\n' % command.asC()
    else:
      ids.append(command.getIdentifier())
      loopbody += 'char *%s\n' % command.asC()

  return loopbody

def getWorkjobs(threads):
  body = ''
  endbrace = '}\n'
  for thread in threads:
    funcName = 'function_%s_%s' % (thread.id, thread.workjob.name)
    prototype = 'void *%s (void *arg){\n' % funcName
    bodystart = '  char helper;\n  for (long iteration = 0; iteration < %s; iteration++){\n' % thread.repetitions
    loopbody = getLoopBody(thread);
    body += prototype + bodystart +loopbody+endbrace + endbrace
  return body

def getMain(threads):
  body = 'int main(){\n'

  if len(threads) == 1: #special case: we don't want to thread for single threaded app
    thread = threads[0]
    body += "function_%s_%s(NULL);\n" % (thread.id, thread.workjob.name)
  else:
    for thread in threads:
      body += ' pthread_t thread%s;\n' % thread.id

    for thread in threads:
      body += ' pthread_create(&thread%s, NULL, function_%s_%s, NULL);\n' % (thread.id, thread.id, thread.workjob.name)

    for thread in threads:
      body += ' pthread_join(thread%s, NULL);\n' % thread.id

  body += 'return 0;\n}'

  return body
