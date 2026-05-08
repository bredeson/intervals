
PREFIX     ?= /usr/local
INSTALL_PATH ?= $(PREFIX)/lib/$(PYTHON_VERSION)/site-packages

CURR_DIR   := $(shell pwd)

PACKAGE    := intervals
LICENSE    := LICENSE
SRC_DIR    := $(CURR_DIR)/src
BUILD_DIR  := $(CURR_DIR)/build
TEST_DIR   := $(CURR_DIR)/test
LIB_DIR    := $(BUILD_DIR)/lib

ECHO       := $(shell which echo 2>/dev/null)
PYTHON     := $(shell which python 2>/dev/null)
INSTALL    := $(shell which install 2>/dev/null)
MKDIR      := $(shell which mkdir 2>/dev/null)
AWK        := $(shell which awk 2>/dev/null)
CAT        := $(shell which cat 2>/dev/null)
RM         := $(shell which rm 2>/dev/null)
RM_R        = $(RM) -R
INSTALL_REG = $(INSTALL) -p -m 644
MKDIR_P     = $(MKDIR) -p

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

SOURCE_FILES = $(wildcard $(SRC_DIR)/$(PACKAGE)/*.py)
BUILD_TARGETS = $(patsubst $(SRC_DIR)/%,$(LIB_DIR)/%,$(SOURCE_FILES))
INSTALL_TARGETS = $(patsubst $(SRC_DIR)/%,$(INSTALL_PATH)/%,$(SOURCE_FILES))


.SUFFIXES:
.SUFFIXES: .py

.PHONY: install activate test check clean 

all: build



build: build-intervals

build-intervals: $(BUILD_TARGETS)

$(LIB_DIR):
	@$(MKDIR_P) $@

$(LIB_DIR)/%: $(SRC_DIR)/%
	@$(MKDIR_P) $(@D)
	@$(AWK) '{print "#",$$_}' $(LICENSE) | $(CAT) - $< >$@


check: test
test: $(BUILD_TARGETS)
	PYTHONPATH="$(LIB_DIR)" $(PYTHON) -m unittest discover test -v



activate:
	@$(ECHO) 'export PYTHONPATH="$(INSTALL_PATH)$${PYTHONPATH:+:$${PYTHONPATH}}";' >activate
	@$(ECHO) '#setenv PYTHONPATH "$(INSTALL_PATH):$$PYTHONPATH";' >>activate



install: build test install-intervals

install-intervals: $(INSTALL_TARGETS)

$(INSTALL_PATH)/$(PACKAGE)/%.py: $(LIB_DIR)/$(PACKAGE)/%.py
	$(INSTALL_REG) $< $@



clean:
	-$(RM_R) $(BUILD_DIR)
