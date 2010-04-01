#include <stdio.h>
#include <malloc.h>

int main(){
  int *pointer = NULL;
  for (int i=0; i<3; i++){
    pointer = malloc(i*sizeof(int));
    free(pointer);
  }
}
