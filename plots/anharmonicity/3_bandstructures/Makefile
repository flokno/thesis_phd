COM1 = python plot_bandstructure_dos.py KCaF3 --reference KCaF3/KCaF3_Raman_THz.dat --ymax 15
COM2 = python plot_bandstructure_dos.py Si --blue --ratio 2 --reference Si/patches_G-L.dat
COM3 = python plot_bandstructure_dos.py KCaF3.cub/ --ymin -4 

all:
	${COM1} 
	${COM2} 
	${COM3}

K:
	${COM1}

S:
	${COM2}

K.cub:
	${COM3}
