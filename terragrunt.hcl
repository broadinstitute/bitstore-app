# Global terragrunt configuration

locals {
  settings_vars = read_terragrunt_config("settings.hcl")

  bucket         = local.settings_vars.locals.bucket
  bucket_project = local.settings_vars.locals.bucket_project
  env            = local.settings_vars.locals.env
  project_id     = local.settings_vars.locals.project_id
  region         = local.settings_vars.locals.region
}

# Backend state configuration
remote_state {
  backend      = "gcs"
  disable_init = tobool(get_env("DISABLE_INIT", "false"))
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
  config = {
    bucket   = local.bucket
    location = "us"
    prefix   = local.env
    project  = local.bucket_project
  }
}

# stage/terragrunt.hcl
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "google" {
  project = var.project_id
  region  = var.region
}
provider "google-beta" {
  project = var.project_id
  region  = var.region
}
EOF
}

inputs = merge(local.settings_vars.locals)
