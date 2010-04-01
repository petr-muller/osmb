.PHONY: all test

all:
	@echo "Nothing to do here"

test: malloc-test
	stap -v malloc-syscall.stp -c './malloc-test' /lib64/libc-2.11.1.so
	rm -f malloc-test

malloc-test: malloc-test.c
	gcc -std=c99 malloc-test.c -o malloc-test
