set shell := [ "bash", "-uc" ]
_default:
    @- just --unsorted --choose
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Justfile
# NOTE: Do not change the contents of this file!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GEN_MODELS := "datamodel-codegen"
GEN_MODELS_DOCUMENTATION := "openapi-generator"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Macros
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_create-file-if-not-exists fname:
    @touch "{{fname}}";

_create-folder-if-not-exists path:
    @if ! [ -d "{{path}}" ]; then mkdir "{{path}}"; fi

_delete-if-file-exists fname:
    @if [ -f "{{fname}}" ]; then rm "{{fname}}"; fi

_delete-if-folder-exists path:
    @if [ -d "{{path}}" ]; then rm -rf "{{path}}"; fi

_clean-all-files pattern:
    @find . -type f -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    @- find . -type f -name "{{pattern}}" -exec rm {} \; 2> /dev/null

_clean-all-folders pattern:
    @find . -type d -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    @- find . -type d -name "{{pattern}}" -exec rm -rf {} \; 2> /dev/null

_docker-build-and-log service:
    @docker compose up --build -d {{service}} && docker compose logs -f --tail=0 {{service}}

_docker-build-and-interact service container:
    @docker compose up --build -d {{service}} && docker attach {{container}}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: docker
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

docker-prod:
    @just _docker-build-and-log "prod"
docker-staging:
    @just _docker-build-and-log "staging"
docker-local:
    @just _docker-build-and-log "local"
docker-tests:
    @just _docker-build-and-log "utests"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: build, run, tests
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

build:
    @npm run build
run:
    @npm run start
tests:
    @just _create-logs
    @npm run tests
    @just _display-logs

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: clean
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

clean:
    @echo "All system artefacts will be force removed."
    @- just _clean-all-files ".DS_Store"
    @echo "All test artefacts will be force removed."
    @- just _delete-if-folder-exists "logs"
    @echo "All build artefacts will be force removed."
    @- just _delete-if-file-exists "package-lock.json"
    @- just _delete-if-folder-exists "node_modules"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: logging, session
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_create-logs:
    @# For logging purposes (since stdout is rechanneled):
    @just _delete-if-file-exists "logs/debug.log"
    @just _create-folder-if-not-exists "logs"
    @just _create-file-if-not-exists "logs/debug.log"
_display-logs:
    @echo ""
    @echo "Content of logs/debug.log:"
    @echo "----------------"
    @echo ""
    @- cat logs/debug.log
    @echo ""
    @echo "----------------"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: requirements
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_check-system:
    @echo "Operating System detected: {{os_family()}}."
