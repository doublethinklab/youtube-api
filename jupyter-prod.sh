#!/bin/bash

./build_prod.sh

docker run \
    --rm \
    -it \
    doublethinklab/youtube-api:prod
