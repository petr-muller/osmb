#include <stdlib.h>
#include <stdio.h>

int main(){
  int *a;
  a = malloc(32*sizeof(int));
  free(a);
  return 0;
}
