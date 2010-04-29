#include <syscall.h>
#include <stdio.h>
#include <sys/mman.h>


int main(){
  printf("%i %i %i %i", SYS_brk, SYS_mmap, SYS_munmap, MAP_ANONYMOUS);
  return 0;
}
