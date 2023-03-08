#!/bin/bash

docker run \
    --platform linux/amd64 \
    --rm \
    -v ${PWD}:/youtube-api \
    -w /youtube-api \
    -p $1:$1 \
    -e YOUTUBE_API_KEYS_DIR=api_keys \
        doublethinklab/youtube-api:dev \
            jupyter notebook \
                --ip 0.0.0.0 \
                --port $1 \
                --no-browser \
                --allow-root
