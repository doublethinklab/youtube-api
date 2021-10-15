#!/bin/bash

docker build \
    -t doublethinklab/youtube-api:$(cat version) \
    .
