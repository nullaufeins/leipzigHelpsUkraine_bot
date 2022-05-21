################################################################
# BUILD STAGE 0
################################################################
FROM python:3.10-slim AS stage-basic

################################################
# ARGUMENTS
################################################
ARG USER
ARG WORKDIR

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
# BUILD STAGE 1
################################################################
FROM stage-basic AS stage-build
RUN make build
