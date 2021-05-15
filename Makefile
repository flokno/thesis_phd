COM0 = latexmk -pdf -latexoption="-synctex=1"

all:
	${COM0} 

clean:
	latexmk -C
