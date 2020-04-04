#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

# flask run \
#     --host=0.0.0.0 \
#     --port=8000
flask run_socketio \
    --host=0.0.0.0 \
    --port=8000
