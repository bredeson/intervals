
PREFIX     ?= /usr/local
INSTALL_PATH ?= $(PREFIX)/lib/$(PYTHON_VERSION)/site-packages

CURR_PATH  := $(shell pwd)

SRC_PATH   := $(CURR_PATH)/src
BUILD_PATH := $(CURR_PATH)/build
TEST_PATH  := $(CURR_PATH)/test
LIB_PATH   := $(BUILD_PATH)/lib

ECHO       := $(shell which echo 2>/dev/null)
PYTHON     := $(shell which python 2>/dev/null)
INSTALL    := $(shell which install 2>/dev/null)
MKDIR      := $(shell which mkdir 2>/dev/null)
AWK        := $(shell which awk 2>/dev/null)
CAT        := $(shell which cat 2>/dev/null)
CP         := $(shell which cp 2>/dev/null)
CP_R        = $(CP) -R
GIT        := $(shell which git 2>/dev/null)
RM         := $(shell which rm 2>/dev/null)
RM_R        = $(RM) -R
INSTALL_REG = $(INSTALL) -p -m 644
MKDIR_P     = $(MKDIR) -p

PACKAGE    := intervals
LIBRARY    := intervals
VERSION    := $(shell $(GIT) describe --long --tags --always)
CONTACT    := https:\/\/github.com\/bredeson\/intervals\/issues
LICENSE    := LICENSE


ifeq ($(shell uname),Linux)
INSTALL_REG += -D
else
INSTALL_REG = $(CP_R) 
endif

ifneq ($(shell which python3),)
PYTHON     := $(shell which python3)
else ifneq ($(shell which python),)
PYTHON     := $(shell which python)
else
$(error "Python interpreter not found. Please install Python and ensure it is accessible via PATH.")
endif

PYTHON_VERSION := $(shell $(PYTHON) --version 2>&1 | $(AWK) '{if (/Python/) {split($$2,v,".");print "python"v[1]"."v[2]}}')


SOURCE_FILES = $(wildcard $(SRC_PATH)/$(LIBRARY)/*.py)
BUILD_TARGETS = $(patsubst $(SRC_PATH)/%,$(LIB_PATH)/%,$(SOURCE_FILES))
INSTALL_TARGETS = $(patsubst $(SRC_PATH)/%,$(INSTALL_PATH)/%,$(SOURCE_FILES))


.SUFFIXES:
.SUFFIXES: .py

.PHONY: install activate test check clean 

all: build



build: build-intervals

build-intervals: $(LIB_PATH)/$(LIBRARY) $(BUILD_TARGETS)

$(LIB_PATH)/$(LIBRARY): $(LIB_PATH)
	@$(MKDIR_P) $@

$(LIB_PATH):
	@$(MKDIR_P) $@

$(LIB_PATH)/%: $(SRC_PATH)/%
	@$(AWK) '{print "#",$$0}' $(LICENSE) | $(CAT) - $< >$@

$(INSTALL_PATH)/$(LIBRARY): $(INSTALL_PATH)
	@$(MKDIR_P) $@

$(INSTALL_PATH):
	@$(MKDIR_P) $@



check: test
test: $(LIB_PATH)/$(LIBRARY) $(BUILD_TARGETS)
	PYTHONPATH="$(LIB_PATH)" $(PYTHON) -m unittest discover --verbose --failfast --start-directory test



activate:
	@$(ECHO) 'export PYTHONPATH="$(INSTALL_PATH)$${PYTHONPATH:+:$${PYTHONPATH}}";' >activate
	@$(ECHO) '#setenv PYTHONPATH "$(INSTALL_PATH):$$PYTHONPATH";' >>activate



install: build test install-intervals

install-intervals: $(INSTALL_PATH) $(INSTALL_PATH)/$(LIBRARY) $(INSTALL_TARGETS)

$(INSTALL_PATH)/$(LIBRARY)/%.py: $(LIB_PATH)/$(LIBRARY)/%.py
	$(INSTALL_REG) $< $@



clean:
	-$(RM_R) $(BUILD_PATH)
