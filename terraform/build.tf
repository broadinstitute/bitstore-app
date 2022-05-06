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

resource "google_cloudbuild_trigger" "deploy-app-trigger" {
  provider       = google-beta
  name           = "deploy-app"
  description    = "Deploy App"
  filename       = "cloudbuild.yaml"
  project        = var.project_id

  included_files = [
    # "app/**",
  ]

  ignored_files = [
    # "app/*.md",
    # "app/*.sh",
  ]

  github {
    name     = "bitstore-app"
    owner    = "broadinstitute"
    push {
      branch = "^${var.branch}$"
    }
  }

}

