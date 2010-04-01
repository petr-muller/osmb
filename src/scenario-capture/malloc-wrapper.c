#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/syscall.h>

void *malloc(size_t size){
  static void *(*original_malloc) (size_t size) = NULL;
  char *error;
  void *memptr;

  original_malloc = dlsym(RTLD_NEXT, "malloc");
  error = dlerror();

  if (error != NULL){
    fprintf(stderr, "Error when opening original malloc: exiting\n");
    exit(1);
  }

  memptr = original_malloc(size);
  pid_t tid = syscall(SYS_gettid);

  printf("MALLOC TID=%i PID=%i SIZE=%i RETURN=%i\n", tid, getpid(), size, memptr);
  return memptr;
}

void free(void *ptr){
  static void (*original_free) (void *) = NULL;
  char *error;

  original_free = dlsym(RTLD_NEXT, "free");
  error = dlerror();

  if (error != NULL){
    fprintf(stderr, "Error when opening original free: exiting\n");
    exit(1);
  }

  pid_t tid = syscall(SYS_gettid);
  original_free(ptr);

  printf("FREE TID=%i PID=%i POINTER=%i\n", tid, getpid(), ptr);
}
