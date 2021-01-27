provider "google" {
  credentials = file(var.credentials_file)
  project = var.project_id
}

provider "google-beta" {
  credentials = file(var.credentials_file)
  project = var.project_id
}
