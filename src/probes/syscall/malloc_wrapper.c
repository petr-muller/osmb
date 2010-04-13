#include <stdlib.h>

void *probe_malloc(size_t size){
	return ALLOCATE(size);
}

void probe_free(void* mem){
	FREE(mem);
}
