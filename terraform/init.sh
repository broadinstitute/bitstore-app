#!/bin/bash

SCRIPT_DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ $# -lt 1 ] ; then
    echo "USAGE: $(basename "$0") ENV"
    exit 1
fi

APP="bitstore-app"
ENV="$1"
SA_PROJECT="broad-bits-terraform"
SERVICE_ACCOUNT="${APP}@${SA_PROJECT}.iam.gserviceaccount.com"

echo "Environment: ${ENV}"

TERRAFORM="$( which terraform 2>/dev/null )"
if [ $? -ne 0 ]; then
    TERRAFORM="${SCRIPT_DIR}/terraform.sh"
fi

# check for service account
if [ ! -f "etc/service_account.json" ]; then
    echo "Creating a service account key..."
    gcloud --project "${SA_PROJECT}" iam service-accounts keys create "etc/service_account.json" \
        --iam-account "${SERVICE_ACCOUNT}" --format "json"
fi

# remove former terraform directory
if [ -e ".terraform" ]; then
    rm -rv .terraform
fi

# copy tf vars file into place
cp -v "env/${ENV}.tfvars" terraform.tfvars

# initialize terraform with the new terraform.tfvars and the
# associated backend.
$TERRAFORM init -backend-config="env/${ENV}-backend.tf"
