#include <stdio.h>
#include <malloc.h>

int main(){
  int *pointer = NULL;
  for (int i=1; i<4; i++){
    pointer = malloc(i*sizeof(int));
    free(pointer);
  }
}
