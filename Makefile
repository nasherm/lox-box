ploxDir = plox
ploxSrc = $(ploxDir)/$(wildcard *.py)

.PHONY: plox
plox:
	./plox.py

goSrc = golox

golox:
	make -f $(goSrc)/Makefile clean all
