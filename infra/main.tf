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