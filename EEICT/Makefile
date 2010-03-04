prispevek.pdf: prispevek.tex
	pdfcslatex prispevek.tex
	pdfcslatex prispevek.tex

check: prispevek.pdf
	evince prispevek.pdf
	make clean

clean:
	rm -f	prispevek.pdf prispevek.aux prispevek.log
