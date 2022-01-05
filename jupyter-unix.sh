#!/bin/bash

docker run \
    --rm \
    -v ${PWD}:/youtube-api \
    -w /youtube-api \
    -p 8888:8888 \
        control.citw.io:5042/youtube-api:prod \
            jupyter notebook \
                --ip 0.0.0.0 \
                --port 8888 \
                --no-browser \
                --allow-root
