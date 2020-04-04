#!/usr/bin/env bash

set -o errexit
set -o nounset

celery \
    flower \
    -A config.celery_worker \
    --broker="${CELERY_BROKER_URL}"
