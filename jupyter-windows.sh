#!/bin/bash

docker run \
    --rm \
    -v %cd%:/youtube-api \
    -w /youtube-api \
    -p $1:$1 \
        control.citw.io:5042/youtube-api:prod \
            jupyter notebook \
                --ip 0.0.0.0 \
                --port $1 \
                --no-browser \
                --allow-root
