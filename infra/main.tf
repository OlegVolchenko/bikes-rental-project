terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
  zone = var.zone
}

resource "google_storage_bucket" "data_lake_bucket" {
  name          = "${var.lake_bucket}_${var.project}"
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

resource "google_bigquery_dataset" "bikes_rental_intermediate_dataset" {
  dataset_id = "br_intermediate"
  project    = var.project
  location   = var.region
}

resource "google_bigquery_dataset" "bikes_rental_mart_dataset" {
  dataset_id = "br_mart"
  project    = var.project
  location   = var.region
}