# plox
PLOX_SRC = plox/$(wildcard *.py)

.PHONY: plox
plox: $(PLOX_SRC)
	./plox.py

# Golox
WORKDIR = $(shell pwd)
GOLOX_DIR=golox
GO_TARGET=$(WORKDIR)/$(GOLOX_DIR)/golox.bin

golox: $(GOLOX_DIR)/*
	cd $(GOLOX_DIR); go build  -o $(GO_TARGET)

golox_fmt:
	go fmt $(WORKDIR)/$(GOLOX_DIR)

golox_run:
	$(GO_TARGET)

clean:
	go clean $(WORKDIR)/$(GOLOX_DIR)	

