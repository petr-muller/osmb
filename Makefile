.PHONY: all publish diplomka semestral program web clean eeict

publish: all
	@git push origin master
	scp web/index.html mesias.m6.cz:web/osmb/

all: diplomka semestral program web eeict

diplomka:
	make -C DIP all

semestral:
	make -C SEP all

program:
	make -C src all

web:
	@echo "web"
	make -C web all

eeict:
	make -C EEICT

clean:
	make -C web clean
	make -C SEP clean
	make -C src clean
	make -C DIP clean
	make -C EEICT clean
