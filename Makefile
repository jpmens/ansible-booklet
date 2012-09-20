ANSIBLESOURCE=/Users/jpm/Auto/pubgit/ansible/ansible
ANSIBLEVERSION=`head -1 $(ANSIBLESOURCE)/VERSION`
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
	./mofo.py --ansible-version="$(ANSIBLEVERSION)" > modules.tex

clean:
	rm -f $(FILE).aux $(FILE).log $(FILE).out modules.aux modules.log 

manuals:
	./mofo.py --ansible-version="$(ANSIBLEVERSION)" --type man --output-dir man.pages/ -m lineinfile
	(cd man.pages; make)
