#!/bin/bash

docker run \
    --rm \
    -v ${PWD}:/yt-api \
    -w /yt-api \
    -p 8888:8888 \
        doublethinklab/youtube-api:latest \
            jupyter notebook \
                --ip 0.0.0.0 \
                --port 8888 \
                --no-browser \
                --allow-root
