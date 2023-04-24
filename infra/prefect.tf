
resource "google_storage_bucket" "prefect_deployments" {
  project = var.project
  name          = "prefect_deployments_${var.project}"
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  force_destroy = true
}

resource "google_storage_bucket" "data_lake_bucket" {
  project       = var.project
  name          = "bike_rental_extract_${var.project}"
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

resource "google_bigquery_dataset" "bikes_rental_staged_dataset" {
  dataset_id = "br_staged"
  project    = var.project
  location   = var.region
}

resource "google_service_account" "sa" {
  project      = var.project
  account_id   = "prefect"
  display_name = "A service account that only Jane can use"
}

resource "google_project_iam_member" "iam_storage" {
  project = var.project
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "iam_run" {
  project = var.project
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "iam_sa" {
  project = var.project
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.sa.email}"
}