#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

pthread_mutex_t mallmutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t mallcond = PTHREAD_COND_INITIALIZER;

pthread_mutex_t frmutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t frcond = PTHREAD_COND_INITIALIZER;
int mallock = 0;
int frlock = 0;

void *malloc(size_t size){
  static void *(*original_malloc) (size_t size) = NULL;
  char *error;
  void *memptr;

//  pthread_mutex_lock(&mallmutex);
//  while (mallock > 0){
//    pthread_cond_wait(&mallcond, &mallmutex);
//  }
//  mallock++;

  original_malloc = dlsym(RTLD_NEXT, "malloc");
//  error = dlerror();

//  if (error != NULL){
//    fprintf(stderr, "Error when opening original malloc: exiting\n");
//    exit(1);
//  }

  memptr = original_malloc(size);
//  pid_t tid = syscall(SYS_gettid);

//  char buffer[256];
//  snprintf(buffer, 255, "MALLOC TID=%li PID=%li SIZE=%li RETURN=%p\n", (long)tid, (long)getpid(), (long)size, memptr);
//  int fp = open("memdump.out", O_APPEND|O_CREAT|O_WRONLY, S_IRUSR|S_IWUSR);
//  write(fp, buffer, strlen(buffer));
//  close(fp);

//  mallock--;
//  pthread_mutex_unlock(&mallmutex);
//  pthread_cond_broadcast(&mallcond);
  return memptr;
}

void free(void *ptr){
  static void (*original_free) (void *) = NULL;
  char *error;

//  pthread_mutex_lock(&frmutex);
//  while (frlock > 0){
//    pthread_cond_wait(&frcond, &frmutex);
//  }
//  frlock++;

  original_free = dlsym(RTLD_NEXT, "free");
//  error = dlerror();

//  if (error != NULL){
//    fprintf(stderr, "Error when opening original free: exiting\n");
//    exit(1);
//  }

//  pid_t tid = syscall(SYS_gettid);
  original_free(ptr);

//  char buffer[256];
//  snprintf(buffer, 255, "FREE TID=%li PID=%li POINTER=%p\n", (long)tid, (long)getpid(), ptr);
//  int fp = open("memdump.out", O_APPEND|O_CREAT|O_WRONLY, S_IRUSR|S_IWUSR);
//  write(fp, buffer, strlen(buffer));
//  close(fp);

//  frlock--;
//  pthread_mutex_unlock(&frmutex);
//  pthread_cond_broadcast(&frcond);
}
