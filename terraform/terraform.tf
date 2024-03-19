terraform {
  backend "gcs" {
    credentials = "etc/service_account.json"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.51.1"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "3.51.1"
    }
  }
}
