.PHONY: all clean

libfakemalloc.so: malloc-wrapper.c
	gcc -shared -fPIC malloc-wrapper.c -o libfakemalloc.so -ldl -lc

all: libfakemalloc.so

clean:
	rm -f libfakemalloc.so
