resource "google_cloudbuild_trigger" "build-docker-image" {
  provider = google-beta
  name = "build-docker-image"
  description = "Build Docker Image from ${var.branch} branch"
  project = var.project_id

  github {
    name = var.repo
    owner = "broadinstitute"
    push {
      branch = "^${var.branch}$"
    }
  }

  build {
    step {
      name = "gcr.io/cloud-builders/docker"
      args = [
        "build",
        "-t",
        "gcr.io/${var.project_id}/${var.repo}:latest",
        ".",
      ]
    }
    images = [
      "gcr.io/${var.project_id}/${var.repo}:latest",
    ]
  }
}
