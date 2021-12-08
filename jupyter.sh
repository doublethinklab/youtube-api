#!/bin/bash

docker run \
    --rm \
    -v ${PWD}:/youtube-api \
    -w /youtube-api \
    -p $1:$1 \
    -e API_KEY=$(cat api.key) \
        doublethinklab/youtube-api:dev \
            jupyter notebook \
                --ip 0.0.0.0 \
                --port $1 \
                --no-browser \
                --allow-root
