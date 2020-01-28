#!/bin/bash

APP="broad-bitstore-app"
CONFIG='config-prod.py'
SERVICEACCOUNT='service_account.pem'
if [ "$1" == 'dev' ]; then
  APP="broad-bitstore-app-dev"
  CONFIG='config-dev.py'
  SERVICEACCOUNT='service_account_dev.pem'
fi

cp ${CONFIG} config.py

sudo docker run -it --rm \
  -v /etc/localtime:/etc/localtime:ro \
  -v "$(pwd):/usr/src" \
  -v /local/datastore:/local/datastore:rw \
  -v "$(pwd)/tmp:/tmp:rw" \
  --expose 8000 \
  --expose 8080 \
  -p 8000:8000 \
  -p 8080:8080 \
  -w /usr/src \
  google/cloud-sdk:270.0.0 \
    dev_appserver.py \
      -A ${APP} \
      --admin_host 0.0.0.0 \
      --admin_port 8000 \
      --api_port 8081 \
      --appidentity_email_address=${APP}@appspot.gserviceaccount.com \
      --appidentity_private_key_path=service_account.pem \
      --datastore_path /local/datastore/${APP} \
      --host 0.0.0.0 \
      --port 8080 \
      --enable_host_checking false \
      --skip_sdk_update_check=True \
      --use_mtime_file_watcher true \
      app.yaml
      # --clear_datastore
