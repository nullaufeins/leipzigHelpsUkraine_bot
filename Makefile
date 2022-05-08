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
	PYTHON:=py -3
endif
GEN_MODELS:=datamodel-codegen

################################
# Macros
################################

define create_file_if_not_exists
	@touch "$(1)";
endef

define create_folder_if_not_exists
	if ! [ -d "$(1)" ]; then mkdir "$(1)"; fi
endef

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

define generate_models
	@${GEN_MODELS} \
		--input-file-type openapi \
		--encoding "UTF-8" \
		--disable-timestamp \
		--use-schema-description \
		--allow-population-by-field-name \
		--snake-case-field \
		--strict-nullable \
		--input $(1)/$(2).yaml \
		--output $(1)/$(2).py
endef

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

################################
# TARGETS: setup
################################
setup: system-py setup-js
system-py:
	@echo "system-py not implemented"
setup-js:
	@npm init
################################
# TARGETS: build
################################
build: build-py
build-skip-requirements: build-py-skip-requirements
build-js: build-js-requirements build-js-models build-misc
build-js-skip-requirements: build-js-models build-misc
build-js-requrements:
	@npm install --package-lock
build-js-models:
	@echo "\x1b[1mbuild-js-model\x1b[0m not implemented."
build-py: build-py-requirements build-py-models build-misc
build-py-skip-requirements: build-py-models build-misc
build-py-requirements:
	@${PYTHON} -m pip install -r requirements
build-py-models: check-system-requirements build-py-models-nochecks
build-py-models-nochecks:
	@$(call generate_models,models,config)
build-misc:
	@# create database if not exists:
	@if ! [ -d data ]; then mkdir data; fi
	@touch data/queue.db
################################
# TARGETS: run
################################
run: run-py
run-js:
	@node index.js
run-py:
	@${PYTHON} main.py
################################
# TARGETS: tests
################################
tests: tests-py
tests-logs: create-logs tests display-logs
tests-js: tests-js-unit
tests-js-unit:
	mocha \
		--require babel-core/register \
		--watch-extensions js "tests/**/*.test.js"
tests-py: tests-py-unit
tests-py-unit:
	@${PYTHON} -m pytest tests --cache-clear --verbose -k test_
################################
# TARGETS: clean
################################
clean:
	@echo "All system artefacts will be force removed."
	@$(call clean_all_files,.DS_Store)
	@echo "All test artefacts will be force removed."
	@$(call clean_all_folders,.pytest_cache)
	@$(call delete_if_folder_exists,logs)
	@echo "All build artefacts will be force removed."
	@$(call clean_all_folders,__pycache__)
	@$(call delete_if_file_exists,package-lock.json)
	@$(call delete_if_folder_exists,node_modules)
	@exit 0
################################
# TARGETS: logging
################################
create-logs:
	@# For logging purposes (since stdout is rechanneled):
	@$(call delete_if_file_exists,logs/debug.log)
	@$(call create_folder_if_not_exists,logs)
	@$(call create_file_if_not_exists,logs/debug.log)
display-logs:
	@echo ""
	@echo "Content of logs/debug.log:"
	@echo "----------------"
	@echo ""
	@cat logs/debug.log
	@echo ""
	@echo "----------------"
################################
# TARGETS: requirements
################################
check-system-requirements:
	@if ! ( ${GEN_MODELS} --help >> /dev/null 2> /dev/null ); then \
		echo "Command '${GEN_MODELS}' did not work. Ensure that the installation of 'datamodel-code-generator' worked and that system paths are set." \
		exit 1; \
	fi
