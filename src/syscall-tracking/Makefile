.PHONY: all test

all:
	@echo "Nothing to do here"

test: malloc-test gsn
	stap -v malloc-syscall.stp -c './malloc-test' /lib64/libc-2.11.1.so ./malloc-test `./gsn`
	rm -f malloc-test

gsn: get_syscall_numbers.c
	gcc -o gsn get_syscall_numbers.c

malloc-test: malloc-test.c
	gcc -std=c99 malloc-test.c -o malloc-test

clean:
	rm -f gsn malloc-test
