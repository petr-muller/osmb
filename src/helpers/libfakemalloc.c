#include <stdlib.h>
#include <stdio.h>

#ifndef ALLOCATE
  #define ALLOCATE malloc
#endif

#ifndef FREE
  #define FREE free
#endif

void *ALLOCATE(size_t size){
	printf("Fake malloc\n");
	return NULL;
}

void FREE(void *mem){
	printf("Fake free\n");
}
