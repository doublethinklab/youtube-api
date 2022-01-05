#!/bin/bash

export DOCKER_BUILDKIT=1
docker build \
    -f prod.Dockerfile \
    --ssh github=~/.ssh/github \
    -t control.citw.io:5042/youtube-api:prod \
    .
docker push control.citw.io:5042/youtube-api:prod
