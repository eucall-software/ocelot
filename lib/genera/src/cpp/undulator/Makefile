# first 

TO_BUILD = undulator

all: $(TO_BUILD)
#all: $(TO_BUILD) static
COMPILER = g++
#sCOMPILER = g++-4.8

CFLAGS = -Wall -fPIC -fopenmp

SOURCE = integral.cpp spline.cpp motion.cpp u_field.cpp u_magfield.cpp u_rungekutta.cpp u_traject.cpp u_spline2d.cpp 

OBJ = integral.o spline.o motion.o u_field.o u_magfield.o u_rungekutta.o u_traject.o u_spline2d.o

$(OBJ): $(SOURCE)
	$(COMPILER) -c $(CFLAGS) $(SOURCE)
	
$(TO_BUILD): $(SOURCE)
	$(COMPILER) -shared $(CFLAGS) -o $(TO_BUILD).so $(SOURCE)
#-static

#static:$(OBJ)
#	ar -cr  libundulator.a *.o

.PHONY : clean

clean: 
	rm *.o *.a
