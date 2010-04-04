#include <stdlib.h>
#include <stdio.h>

void *malloc(size_t size){
	printf("Fake malloc\n");
	return NULL;
}

void free(void *mem){
	printf("Fake free\n");
}
