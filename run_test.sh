#!/bin/bash

docker run \
    --rm \
    -v ${PWD}:/youtube-api \
    -w /youtube-api \
    -e API_KEY=$(cat api.key) \
    -e YOUTUBE_API_KEYS_DIR=api_keys \
        doublethinklab/youtube-api:dev \
            python -m unittest $1
