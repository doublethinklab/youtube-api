#!/bin/bash

docker run \
    --rm \
    -v ${PWD}:/youtube-api \
    -w /youtube-api \
    -e API_KEY=$(cat api_key) \
        doublethinklab/youtube-api:$(cat version) \
            python -m unittest discover
