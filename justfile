set shell := [ "bash", "-uc" ]
default:
    @just --list
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Justfile
# NOTE: Do not change the contents of this file!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

################################
# VARIABLES
################################

PYTHON := if os_family() == "windows" { "py -3" } else { "python3" }
GEN_MODELS := "datamodel-codegen"

################################
# Macros
################################

create_file_if_not_exists fname:
    @touch "{{fname}}";

create_folder_if_not_exists path:
    @if ! [ -d "{{path}}" ]; then mkdir "{{path}}"; fi

delete_if_file_exists fname:
    @if [ -f "{{fname}}" ]; then rm "{{fname}}"; fi

delete_if_folder_exists path:
    @if [ -d "{{path}}" ]; then rm -rf "{{path}}"; fi

clean_all_files pattern:
    @find . -type f -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    @find . -type f -name "{{pattern}}" -exec rm {} \; 2> /dev/null

clean_all_folders pattern:
    @find . -type d -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    @find . -type d -name "{{pattern}}" -exec rm -rf {} \; 2> /dev/null

generate_models path name:
    @{{GEN_MODELS}} \
        --input-file-type openapi \
        --encoding "UTF-8" \
        --disable-timestamp \
        --use-schema-description \
        --allow-population-by-field-name \
        --snake-case-field \
        --strict-nullable \
        --input {{path}}/{{name}}-schema.yaml \
        --output {{path}}/generated/{{name}}.py

docker_build_and_log service:
    @docker compose up --build -d {{service}} && docker compose logs -f {{service}}

docker_build_and_interact service container:
    @docker compose up --build -d {{service}} && docker attach {{container}}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

################################
# TARGETS: docker
################################
docker-prod:
    @just docker_build_and_log "prod"
docker-staging:
    @just docker_build_and_log "staging"
docker-local:
    @just docker_build_and_log "local"
docker-tests: docker-utests docker-itests
docker-utests:
    @just docker_build_and_log "utests"
docker-itests:
    @just docker_build_and_interact "itests" "bot_itests"
    @docker stop "bot_local"
################################
# TARGETS: build
################################
build: build-requirements build-skip-requirements
build-skip-requirements: build-models build-misc
build-requirements:
    @{{PYTHON}} -m pip install -r requirements.txt
build-models: check-system-requirements build-models-nochecks
build-models-nochecks:
    @echo "Generate data models from schemata..."
    @just create_folder_if_not_exists "models/generated"
    @just generate_models "models" "config"
    @just generate_models "models" "tests"
build-misc:
    @# create database if not exists:
    @if ! [ -d data ]; then mkdir data; fi
    @touch data/queue.db
################################
# TARGETS: run
################################
run:
    @{{PYTHON}} main.py
################################
# TARGETS: tests
################################
tests: tests-unit tests-integration
tests-logs: create-logs tests display-logs
tests-unit-logs: create-logs tests-unit display-logs
tests-integration-logs: create-logs tests-integration display-logs
tests-unit:
    @{{PYTHON}} -m pytest tests \
        --cache-clear \
        --verbose \
        --ignore=tests/integration \
        -k test_ \
        2> /dev/null
tests-integration: create-session tests-integration-skip-session
tests-integration-skip-session:
    @{{PYTHON}} -m pytest tests/integration \
        --cache-clear \
        --verbose \
        -k test_ \
        2> /dev/null
################################
# TARGETS: clean
################################
clean: clean-basic clean-sessions
clean-sessions:
    @echo "All sessions will be force removed."
    @just delete_if_folder_exists "secrets"
clean-basic:
    @echo "All system artefacts will be force removed."
    @just clean_all_files ".DS_Store"
    @echo "All test artefacts will be force removed."
    @just clean_all_folders ".pytest_cache"
    @just delete_if_folder_exists "logs"
    @echo "All build artefacts will be force removed."
    @just clean_all_folders "__pycache__"
    @just delete_if_folder_exists "models/generated"
################################
# TARGETS: logging, session
################################
create-logs:
    @# For logging purposes (since stdout is rechanneled):
    @just delete_if_file_exists "logs/debug.log"
    @just create_folder_if_not_exists "logs"
    @just create_file_if_not_exists "logs/debug.log"
display-logs:
    @echo ""
    @echo "Content of logs/debug.log:"
    @echo "----------------"
    @echo ""
    @cat logs/debug.log
    @echo ""
    @echo "----------------"
create-session:
    @just create_folder_if_not_exists "secrets"
    @{{PYTHON}} tests/intialise.py
################################
# TARGETS: requirements
################################
check-system:
    @echo "Operating System detected: {{os_family()}}."
    @echo "Python command used: {{PYTHON}}."
check-system-requirements:
    if ! ( {{GEN_MODELS}} --help >> /dev/null 2> /dev/null ); then \
        echo "Command '{{GEN_MODELS}}' did not work. Ensure that the installation of 'datamodel-code-generator' worked and that system paths are set." \
        exit 1; \
    fi
