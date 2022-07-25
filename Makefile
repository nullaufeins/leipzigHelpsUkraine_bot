# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Makefile
# NOTE: Do not change the contents of this file!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

define _create-file-if-not-exists
	@touch "$(1)";
endef

define _create-folder-if-not-exists
	@if ! [ -d "$(1)" ]; then mkdir "$(1)"; fi
endef

define _delete-if-file-exists
	@if [ -f "$(1)" ]; then rm "$(1)"; fi
endef

define _delete-if-folder-exists
	@if [ -d "$(1)" ]; then rm -rf "$(1)"; fi
endef

define _clean-all-files
	@find . -type f -name "$(1)" -exec basename {} \; 2> /dev/null
	@- find . -type f -name "$(1)" -exec rm {} \; 2> /dev/null
endef

define _clean-all-folders
	@find . -type d -name "$(1)" -exec basename {} \; 2> /dev/null
	@- find . -type d -name "$(1)" -exec rm -rf {} \; 2> /dev/null
endef

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

################################
# BASIC TARGETS: setup, build, run
################################

build:
	@npm run build
run:
	@npm run start
tests:
	@make _create-logs
	@npm run tests
	@make _display-logs

################################
# TARGETS: clean
################################

clean:
	@echo "All system artefacts will be force removed."
	@$(call _clean-all-files,".DS_Store")
	@echo "All test artefacts will be force removed."
	@$(call _delete-if-folder-exists,"logs")
	@echo "All build artefacts will be force removed."
	@$(call _delete-if-file-exists,"package-lock.json")
	@$(call _delete-if-folder-exists,"node_modules")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: logging, session
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_create-logs:
	@# For logging purposes (since stdout is rechanneled):
	@$(call _delete-if-file-exists,"logs/debug.log")
	@$(call _create-folder-if-not-exists,"logs")
	@$(call _create-file-if-not-exists,"logs/debug.log")
_display-logs:
	@echo ""
	@echo "Content of logs/debug.log:"
	@echo "----------------"
	@echo ""
	@- cat logs/debug.log
	@echo ""
	@echo "----------------"
