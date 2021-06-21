COM0 = latexmk -pdf -latexoption="-synctex=1"

all:
	${COM0} main.tex

clean:
	latexmk -C
