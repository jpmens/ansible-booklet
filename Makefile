ANSIBLESOURCE=/Users/jpm/Auto/pubgit/ansible/ansible
ANSIBLEVERSION=`head -1 $(ANSIBLESOURCE)/VERSION`
FORMATTER=$(ANSIBLESOURCE)/hacking/module_formatter.py
FILE=ansible-booklet
TEXFILES= ansible-booklet.tex \
	  extending.tex \
	  playbooks.tex \
	  pullmode.tex \
	  templates.tex

all: mods $(FILE).pdf

pdf: $(FILE).pdf

mods: $(FORMATTER) $(ANSIBLESOURCE)/hacking/templates/latex.j2
	$(FORMATTER) --template-dir=$(ANSIBLESOURCE)/hacking/templates -t latex -o modules/ltx --includes-file=modules/ltx/_list
	./fixall modules/ltx/_list

$(FILE).pdf: $(FILE).tex $(TEXFILES) modules/_list.tex
	pdflatex $(FILE).tex
	pdflatex $(FILE).tex

clean:
	rm -f $(FILE).aux $(FILE).log $(FILE).out modules.aux modules.log 


