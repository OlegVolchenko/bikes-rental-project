variable "project" {
  default = "zoomcamp-olvol3"
  }

variable "region" {
  default = "europe-west4"
}

variable "zone" {
  default = "europe-west4-a"
}

variable "staged_dataset" {
  default = "bike_rental_staged"
}

variable "lake_bucket" {
  default = "bike_rental_extract"
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}