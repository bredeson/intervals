
PREFIX     := /usr/local

PACKAGE    := intervals
SOURCE_DIR := src
BUILD_DIR  := build
TEST_DIR   := test

LIB_DIR    := $(BUILD_DIR)/lib

ECHO       := echo
PYTHON     := $(filter /%,$(shell /bin/sh -c 'type python'))
INSTALL    := $(filter /%,$(shell /bin/sh -c 'type install'))
MKDIR      := $(filter /%,$(shell /bin/sh -c 'type mkdir'))
AWK        := $(filter /%,$(shell /bin/sh -c 'type awk'))
CAT        := $(filter /%,$(shell /bin/sh -c 'type cat'))
CP         := $(filter /%,$(shell /bin/sh -c 'type cp'))
RM         := $(filter /%,$(shell /bin/sh -c 'type rm'))

CP_R        = $(CP) -R
RM_R        = $(RM) -r

PYTHON_VER := $(shell $(PYTHON) --version 2>&1 | awk '{if (/Python/) {split($$2,v,".");print "python"v[1]"."v[2]}}')
INSTALL_REG = $(INSTALL) -p -m 644 -D
MKDIR_P     = $(MKDIR) -p

LICENSE     := LICENSE

INSTALL_PATH ?= \
	$(PREFIX)/lib/$(PYTHON_VER)/site-packages

SOURCE_FILES = $(wildcard $(SOURCE_DIR)/$(PACKAGE)/*.py)
BUILD_TARGETS = $(patsubst $(SOURCE_DIR)/%,$(LIB_DIR)/%,$(SOURCE_FILES))
INSTALL_TARGETS = $(patsubst $(SOURCE_DIR)/%,$(INSTALL_PATH)/%,$(SOURCE_FILES))


.SUFFIXES:
.SUFFIXES: .py

.PHONY: install activate test clean 

all: build



build: $(BUILD_TARGETS)

$(LIB_DIR):
	@$(MKDIR_P) $@

$(LIB_DIR)/%: $(SOURCE_DIR)/%
	@$(MKDIR_P) $(@D)
	@$(AWK) '{print "#",$$_}' $(LICENSE) | $(CAT) - $< >$@



test: $(BUILD_TARGETS)
	PYTHONPATH="$(PWD)/$(LIB_DIR)" $(PYTHON) -m unittest discover test -v



activate:
	@$(ECHO) 'export PYTHONPATH="$(INSTALL_PATH)$${PYTHONPATH:+:$${PYTHONPATH}}";' >activate
	@$(ECHO) '#setenv PYTHONPATH "$(INSTALL_PATH):$$PYTHONPATH";' >>activate



install: install-intervals

install-intervals: $(INSTALL_TARGETS)

$(INSTALL_PATH)/$(PACKAGE)/%.py: $(LIB_DIR)/$(PACKAGE)/%.py
	$(INSTALL_REG) $< $@



clean:
	-$(RM_R) $(BUILD_DIR)
