FILE=ansible-booklet
TEXFILES= ansible-booklet.tex \
	  extending.tex \
	  modules.tex \
	  playbooks.tex \
	  pullmode.tex \
	  templates.tex

all: $(FILE).pdf


$(FILE).pdf: $(FILE).tex $(TEXFILES)
	pdflatex $(FILE).tex
	pdflatex $(FILE).tex

modules: 
	./mofo.py > modules.tex

clean:
	rm -f $(FILE).aux $(FILE).log $(FILE).out modules.aux modules.log 
