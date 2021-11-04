COM0 = latexmk -pdf -latexoption="-synctex=1"

all:
	${COM0} main.tex

force:
	${COM0} -f main.tex

clean:
	latexmk -C
