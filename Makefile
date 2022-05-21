SHELL:=/usr/bin/env bash
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Makefile
# NOTE: Do not change the contents of this file!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

################################
# VARIABLES
################################

os:=$(OS)
ifeq (${os},Windows_NT)
	os:=Windows
else
	os:=$(shell uname)
endif

PYTHON:=python3
ifeq (${os},Windows)
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
	@find . -type f -name "$(1)" -exec basename {} \; 2> /dev/null
	@find . -type f -name "$(1)" -exec rm {} \; 2> /dev/null
endef

define clean_all_folders
	@find . -type d -name "$(1)" -exec basename {} \; 2> /dev/null
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
		--input $(1)/$(2)-schema.yaml \
		--output $(1)/generated/$(2).py
endef

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

################################
# TARGETS: docker
################################
docker-prod:
	@docker-compose up -d prod && docker-compose logs -f prod
docker-staging:
	@docker-compose up -d staging && docker-compose logs -f staging
docker-local:
	@docker-compose up -d local && docker-compose logs -f local
docker-tests: docker-tests-unit docker-tests-integration
docker-utests:
	@docker-compose up -d utests && docker-compose logs -f utests
docker-itests:
	@docker-compose up -d itests && docker attach bot_itests
################################
# TARGETS: build
################################
build: build-requirements build-skip-requirements
build-skip-requirements: build-models build-misc
build-requirements:
	@${PYTHON} -m pip install -r requirements.txt
build-models: check-system-requirements build-models-nochecks
build-models-nochecks:
	@$(call create_folder_if_not_exists,models/generated)
	@$(call generate_models,models,config)
	@$(call generate_models,models,tests)
build-misc:
	@# create database if not exists:
	@if ! [ -d data ]; then mkdir data; fi
	@touch data/queue.db
################################
# TARGETS: run
################################
run:
	@${PYTHON} main.py
################################
# TARGETS: tests
################################
tests: tests-unit tests-integration
tests-logs: create-logs tests display-logs
tests-unit-logs: create-logs tests-unit display-logs
tests-integration-logs: create-logs tests-integration display-logs
tests-unit:
	@${PYTHON} -m pytest tests \
		--cache-clear \
		--verbose \
		--ignore=tests/integration \
		-k test_ \
		2> /dev/null
tests-integration: create-session tests-integration-skip-session
tests-integration-skip-session:
	@${PYTHON} -m pytest tests/integration \
		--cache-clear \
		--verbose \
		-k test_ \
		2> /dev/null
################################
# TARGETS: clean
################################
clean:
	@echo "All system artefacts will be force removed."
	@$(call clean_all_files,.DS_Store)
	@echo "All test artefacts will be force removed."
	@$(call clean_all_files,*.session)
	@$(call clean_all_files,*.session-journal)
	@$(call clean_all_folders,.pytest_cache)
	@$(call delete_if_folder_exists,logs)
	@echo "All build artefacts will be force removed."
	@$(call clean_all_folders,__pycache__)
	@$(call delete_if_folder_exists,models/generated)
	@exit 0
################################
# TARGETS: logging, session
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
create-session:
	@$(call create_folder_if_not_exists,secrets)
	@${PYTHON} tests/intialise.py
################################
# TARGETS: requirements
################################
check-system:
	@echo "Operating System detected: ${os}."
	@echo "Python command used: ${PYTHON}."
check-system-requirements:
	@if ! ( ${GEN_MODELS} --help >> /dev/null 2> /dev/null ); then \
		echo "Command '${GEN_MODELS}' did not work. Ensure that the installation of 'datamodel-code-generator' worked and that system paths are set." \
		exit 1; \
	fi
