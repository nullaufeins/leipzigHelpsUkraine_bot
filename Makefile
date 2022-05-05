# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Makefile
# NOTE: Do not change the contents of this file!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

include .env

################################
# VARIABLES
################################

PYTHON:=python3
ifeq ($(OS),Windows_NT)
PYTHON=py -3
endif

################################
# Macros
################################

define delete_if_file_exists
	@if [ -f "$(1)" ]; then rm "$(1)"; fi
endef

define delete_if_folder_exists
	@if [ -d "$(1)" ]; then rm -rf "$(1)"; fi
endef

define clean_all_files
	@find . -type f -name "$(1)" -exec basename {} \;
	@find . -type f -name "$(1)" -exec rm {} \; 2> /dev/null
endef

define clean_all_folders
	@find . -type d -name "$(1)" -exec basename {} \;
	@find . -type d -name "$(1)" -exec rm -rf {} \; 2> /dev/null
endef

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

################################
# BASIC TARGETS: setup, build, run
################################
setup: setup-py
setup-node:
	@echo "Call \x1b[93;1mnpm init\x1b[0m in order to set up src/package.json, if it does not exist."
	@npm upgrade
setup-py:
	@${PYTHON} -m pip install -r requirements
build:
	@# create database if not exists:
	@if ! [ -d data ]; then mkdir data; fi
	@touch data/queue.db
	@npm install --package-lock
run:
	@#node index.js &
	@${PYTHON} main.py
all: setup build run
################################
# TESTING
################################
tests: unit-tests-py
unit-tests-js:
	mocha \
		--require babel-core/register \
		--watch-extensions js "tests/**/*.test.js"
unit-tests-py:
	@# For logging purposes (since stdout is rechanneled):
	@$(call delete_if_file_exists,logs/debug.log)
	@$(call create_folder_if_not_exists,logs)
	@$(call create_file_if_not_exists,logs/debug.log)
	@# for python unit tests:
	@${PYTHON} -m pytest tests --cache-clear --verbose -k test_
	@cat logs/debug.log
################################
# TARGETS: clean
################################
clean:
	@echo "All system artefacts will be force removed."
	@$(call clean_all_files,.DS_Store)
	@echo "All build artefacts will be force removed."
	@$(call clean_all_folders,__pycache__)
	@$(call clean_all_folders,.pytest_cache)
	@$(call delete_if_file_exists,package-lock.json)
	@$(call delete_if_folder_exists,node_modules)
	@exit 0
