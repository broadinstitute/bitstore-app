#!/bin/bash

export PATH=/opt/google-cloud-sdk/bin:$PATH

APP="broad-bitstore-app"
SERVICEACCOUNT="service_account_prod.json"
if [ "$1" == "dev" ]; then
  APP="broad-bitstore-app-dev"
  SERVICEACCOUNT="service_account_dev.json"
elif [ "$1" == "sandbox" ]; then
  APP="broad-bitstore-app-sandbox"
  SERVICEACCOUNT="service_account_sandbox.json"
fi

IMAGE="${IMAGE:-"gcr.io/${APP}/bitstore-app:latest"}"

# pull the newest image
case "${IMAGE}" in
  *gcr.io*)
    docker pull "${IMAGE}"
    ;;
esac

# run the container
docker run -it --rm \
  --expose 8080 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/usr/src/etc/${SERVICEACCOUNT} \
  -p 8080:8080 \
  -v "$(pwd)":/usr/src \
  -w /usr/src \
  "${IMAGE}" \
  python main.py
