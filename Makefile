bindir=${PWD}/bin

gauss:
	mkdir -p $(bindir)
	ln -s src/gen_gaussian.py $(bindir)/gen_gaussian.py
	ln -s src/grab_gaussian.py $(bindir)/grab_gaussian.py