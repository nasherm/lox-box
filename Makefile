ploxDir = plox
ploxSrc = $(ploxDir)/$(wildcard *.py)
ploxMain = $(ploxDir)/Lox.py

.PHONY: plox
plox:
	python3 $(ploxMain)

ploxCompile: $(ploxSrc)
	python3 -m compileall plox/
