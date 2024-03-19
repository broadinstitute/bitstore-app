#!/bin/bash

CONTAINER_IMAGE='hashicorp/terraform:latest'
SUDO=

SCRIPT_DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if hash docker >/dev/null; then
    CONTAINER_APP='docker'
elif hash podman >/dev/null; then
    CONTAINER_APP='podman'
else
    echo 'Container environment cannot be found. Exiting!'
    exit 2
fi

if [ "$TERM" != "dumb" ] ; then
    TTY=( -it )
fi

if [ "$( uname -s )" != 'Darwin' ]; then
    if [ ! -w '/var/run/docker.sock' ]; then
       SUDO='sudo'
    fi
fi

# If we already have a gcloud config, try to mount it in
GCLOUD_MOUNT=
if [ -d "${HOME}/.config/gcloud" ]; then
    GCLOUD_MOUNT=( -v "${HOME}/.config/gcloud:/root/.config/gcloud" )
fi

$SUDO $CONTAINER_APP pull "$CONTAINER_IMAGE" >&2

$SUDO $CONTAINER_APP run "${TTY[@]}" \
    --rm \
    -w /data/terraform \
    "${GCLOUD_MOUNT[@]}" -v "${SCRIPT_DIR}:/data" \
    "$CONTAINER_IMAGE" "$@"
