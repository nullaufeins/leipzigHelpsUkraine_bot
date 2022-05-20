################################################################
# BUILD STAGE 0
################################################################
FROM python:3.10-slim AS stage-basic

################################################
# ARGUMENTS
################################################
ARG PROJECT
ARG USER
ARG TOKEN
ARG WORKDIR

LABEL org.name.project=${PROJECT}

################################################
# INSTALL BASICS FOR SYSTEM
################################################

# NOTE: Install Python dependencies early for more efficient cache usage.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apt-get update && apt-get install -y make \
    && rm -rf /var/lib/apt/lists/*

################################################
# SET USERS, ACCESS
################################################

# Create a non-privileged user to run the bot.
RUN groupadd --gid 1000 ${USER} \
    && useradd --uid 1000 --gid 1000 --create-home ${USER}

# Running instance should own the code, as `make build` leads to changess.
COPY . "${WORKDIR}"
RUN chown -R ${USER}:${USER} ${WORKDIR}

USER ${USER}
WORKDIR ${WORKDIR}

################################################################
# BUILD STAGE 1a
################################################################
FROM stage-basic AS stage-build

ARG TOKEN
ARG WORKDIR

RUN [ "bash", "-c", "echo \"token=${TOKEN}\" >| ${WORKDIR}/.env" ]
RUN make build

################################################################
# BUILD STAGE 1b
################################################################
FROM stage-basic AS stage-build-no-env

ARG TOKEN
ARG WORKDIR

RUN make build

# FIXME: interactive mode does not work
# ################################################################
# # BUILD STAGE 1b
# ################################################################
# FROM stage-build-no-env AS stage-build-and-session-no-env

# ARG DEBIAN_FRONTEND=interactive
# RUN make create-session
