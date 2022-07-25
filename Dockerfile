################################################################
# BUILD STAGE 0
################################################################
FROM node:18-slim AS stage-basic

################################################
# ARGUMENTS
################################################
ARG USER
ARG WORKDIR

################################################
# INSTALL BASICS FOR SYSTEM
################################################

RUN apt-get update && apt-get install -y make \
    && rm -rf /var/lib/apt/lists/*

################################################
# SET USERS, ACCESS
################################################

# Create a non-privileged user to run the bot.
RUN groupadd --gid 2000 ${USER} \
    && useradd --uid 2000 --gid 2000 --create-home ${USER}

# Running instance should own the code, as `make build` leads to changess.
COPY . "${WORKDIR}"
RUN chown -R ${USER}:${USER} ${WORKDIR}

USER ${USER}
WORKDIR ${WORKDIR}

################################################################
# BUILD STAGE 1
################################################################
FROM stage-basic AS stage-build
RUN make build
