#!/bin/bash

export DOCKER_BUILDKIT=1
docker build \
    --no-cache \
    --ssh github=~/.ssh/github \
    -t doublethinklab/youtube-api:dev \
    .
