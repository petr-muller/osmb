all: frags.pdf fragmentation.pdf

frags.pdf : frags.eps
	epstopdf frags.eps

fragmentation.pdf: fragmentation.eps
	epstopdf fragmentation.eps

clean:
	rm  -f frags.pdf fragmentation.pdf
