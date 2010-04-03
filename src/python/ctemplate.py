from datetime import date

def getHeader(ml, tl):
  return '// Malloc benchmark file generated on %s\n' \
         '// Limits:\n'\
         '//   Memory limit: %s\n' \
         '//   Threads:      %s\n' \
         '#include <stdlib.h>\n' \
         '#include <pthread.h>\n\n' % (date.today(), ml, tl)

def getWorkjobs(threads):
  body = ''
  for thread in threads:
    funcName = 'function_%s_%s' % (thread.id, thread.workjob.name)
    prototype = 'void *%s (void *arg){\n' % funcName
    bodystart = '  char helper;\n  for (long iteration = 0; iteration < %s; iteration++){\n' % thread.repetitions
    ids = []
    loopbody = ''
    for command in thread.workjob.commands:
      if command.getIdentifier() in ids:
        loopbody += '%s\n' % command.asC()
      else:
        ids.append(command.getIdentifier())
        loopbody += 'char *%s\n' % command.asC()
    endbrace = '}\n'
    body += prototype + bodystart +loopbody+endbrace + endbrace
  return body 

def getMain(threads):
  body = 'int main()\n{'
  for thread in threads:
    body += ' pthread_t thread%s;\n' % thread.id
  
  for thread in threads:
    body += ' pthread_create(&thread%s, NULL, function_%s_%s, NULL);\n' % (thread.id, thread.id, thread.workjob.name)
  
  for thread in threads:
    body += ' pthread_join(thread%s, NULL);\n' % thread.id
    
  body += 'return 0;\n}'  

  return body 
   