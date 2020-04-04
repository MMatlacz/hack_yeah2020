#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


# https://docs.celeryproject.org/en/latest/userguide/workers.html
celery \
    worker \
    -A config.celery_worker \
    --loglevel="${CELERY_LOGLEVEL:-INFO}" \
    --concurrency="${CELERY_CONCURRENCY:-2}"
