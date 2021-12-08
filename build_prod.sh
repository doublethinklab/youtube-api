#!/bin/bash

docker build \
    -f prod.Dockerfile \
    -t doublethinklab/youtube-api:prod \
    .
