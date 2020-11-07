ploxDir = plox
ploxSrc = $(ploxDir)/$(wildcard *.py)
ploxMain = $(ploxDir).Lox

.PHONY: plox
plox:
	python3 -m $(ploxMain)

ploxCompile: $(ploxSrc)
	python3 -m compileall plox/
