MAINDOC = principal 
DOCS = $(wildcard *.tex)
DVIFILE = $(patsubst %,%.dvi,$(MAINDOC))
PSFILE = $(patsubst %,%.ps,$(MAINDOC))
PDFFILE = $(patsubst %,%.pdf,$(MAINDOC))
TEXCODE = $(patsubst code/%.cc, code/%.tex, $(wildcard code/*.cc))

all:  $(PDFFILE) 

$(DVIFILE): $(TEXCODE) ${DOCS} 
$(PDFFILE): $(TEXCODE) ${DOCS} 

code/%.tex: code/%.cc
	cpp2latex -h -s 0 -t 4 $< > code/$*.tex 
	#lgrind -i -lc -t 4 $< > code/$*.tex

%.pdf: %.tex
	pdflatex --shell-escape $*
	bibtex $*
	pdflatex --shell-escape $*
	pdflatex --shell-escape $*

%.dvi: %.tex
	latex  $*
	bibtex $*
	latex  $*
	latex  $*

%.ps: %.dvi
	dvips $< -o $@

#%.pdf: %.ps
#	ps2pdf -dMaxSubsetPct=100 -dCompatibilityLevel=1.2 -dSubsetFonts=true -dEmbedAllFonts=true $<

clean:
	@rm -f *.bbl *.blg *.dvi *~ *.ps *.aux *.log *.pdf *.bak *.toc *.lof *.lot *.out
