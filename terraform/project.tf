resource "google_project" "project" {
  name            = var.project_name
  project_id      = var.project_id
  folder_id       = var.folder_id
  billing_account = var.billing_account

  labels = {
      app        = "bitstore",
      billing    = lower(var.billing_account)
      costobject = "broad-${var.costobject}",
      env        = var.env,
  }

  skip_delete = true
}

resource "google_project_service" "services" {
  for_each = toset([
    "appengine.googleapis.com",
    "firestore.googleapis.com",
  ])
  project = google_project.project.project_id
  service = each.key

  disable_dependent_services = true
  disable_on_destroy = true
}
