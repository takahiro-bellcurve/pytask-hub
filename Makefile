PACKAGE=

# to use `make install PACKAGE=django`
install:
	pipenv install $(PACKAGE)
	pipenv requirements > requirements.txt

# to use `make uninstall PACKAGE=django`
uninstall:
	pipenv uninstall $(PACKAGE)
	pipenv requirements > requirements.txt