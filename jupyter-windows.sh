#!/bin/bash

docker run \
    --rm \
    -v %cd%:/youtube-api \
    -w /youtube-api \
    -p $1:$1 \
        doublethinklab/youtube-api:$(cat version) \
            jupyter notebook \
                --ip 0.0.0.0 \
                --port $1 \
                --no-browser \
                --allow-root
