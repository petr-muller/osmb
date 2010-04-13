#include <stdlib.h>
#include <stdio.h>

#ifndef ALLOCATE
  #define ALLOCATE malloc
#endif

#ifndef FREE
  #define FREE free
#endif

extern void *ALLOCATE(size_t);
extern void FREE(void*);

int main(){
  int *a;
  a = (int *)ALLOCATE(32*sizeof(int));
  FREE(a);
  return 0;
}
