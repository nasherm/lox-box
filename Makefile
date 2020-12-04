ploxDir = plox
ploxSrc = $(ploxDir)/$(wildcard *.py)

.PHONY: plox
plox:
	./plox.py
