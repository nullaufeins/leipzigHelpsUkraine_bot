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
ARG MODE
ARG SERVICE

LABEL org.project.bot=${PROJECT}
LABEL org.mode.bot=${MODE}
LABEL org.service.bot=${SERVICE}}

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
