.PHONY: all publish diplomka semestral program web clean

publish: all
	@git push origin master
	scp web/index.html mesias.m6.cz:web/osmb/

all: diplomka semestral program web

diplomka:
	make -C DIP all

semestral:
	make -C SEP all

program:
	make -C src all

web:
	@echo "web"
	make -C web all

clean:
	make -C web clean
	make -C SEP clean
	make -C src clean
	make -C DIP clean
