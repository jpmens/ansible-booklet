all: $(patsubst %.man,%.pdf,$(wildcard *.man))

%.ps: %.man
	groff -man -Tps $< > $@
%.pdf: %.ps
	ps2pdf $< $@
