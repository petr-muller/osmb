.PHONY: all clean

libfakemalloc.so: malloc-wrapper.c
	gcc -shared -fPIC malloc-wrapper.c -o libfakemalloc.so -ldl -lpthread -Wall -pedantic -std=c99

all: libfakemalloc.so

clean:
	rm -f libfakemalloc.so
