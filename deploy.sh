#!/bin/bash

PROJECT="broad-bitstore-app"
if [ "$1" == 'dev' ]; then
  PROJECT="broad-bitstore-app-dev"
elif [ "$1" == 'sandbox' ]; then
  PROJECT="broad-bitstore-app-sandbox"
fi

# deploy app
gcloud -q app deploy --project ${PROJECT}