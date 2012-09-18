FILE=ansible-booklet

all: $(FILE).pdf

$(FILE).pdf: $(FILE).tex modules.tex
	pdflatex $(FILE).tex
	pdflatex $(FILE).tex

modules.tex: modules2.py Makefile inc/*.tex templates/latex.j2
	./modules2.py > modules.tex

clean:
	rm -f $(FILE).aux $(FILE).log $(FILE).out modules.aux modules.log 
