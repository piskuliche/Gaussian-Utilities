bindir=${PWD}/bin

gauss:
	mkdir -p $(bindir)
	touch $(bindir)/test
	rm $(bindir)/*
	ln -s ${PWD}/src/gen_gaussian.py $(bindir)
	ln -s ${PWD}/src/grab_gaussian.py $(bindir)
	chmod 777 $(bindir)/*.py