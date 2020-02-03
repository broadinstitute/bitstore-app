#!/bin/bash

APP="broad-bitstore-app"
CONFIG="config-prod.py"
if [ "$1" == 'dev' ]; then
  APP="broad-bitstore-app-dev"
  CONFIG='config-dev.py'
elif [ "$1" == 'sandbox' ]; then
  APP="broad-bitstore-app-sandbox"
  CONFIG='config.py'
fi

# deploy app
cp ${CONFIG} config.py
gcloud -q app deploy --project ${APP}