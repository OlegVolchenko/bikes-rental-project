### PREFECT BUCKETS

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


### PREFECT SA
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

resource "google_project_iam_member" "iam_secret" {
  project = var.project
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_project_iam_member" "iam_bq" {
  project = var.project
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.sa.email}"
}
### ENABLE APIs

resource "google_project_service" "compute_api" {
  project = var.project
  service = "compute.googleapis.com"
}

resource "google_project_service" "secret_api" {
  project = var.project
  service = "secretmanager.googleapis.com"
}

### PREFECT AGENT

resource "google_compute_instance" "agent" {
  name         = "prefect-agent"
  machine_type = "e2-standard-2"
  zone         = var.zone


  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20230104"
    }
  }

  metadata_startup_script = file("./startup.sh")

  network_interface {
    network = "default"
    access_config {}
  }

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.sa.email
    scopes = ["cloud-platform"]
  }
 depends_on = [google_project_service.compute_api]
}