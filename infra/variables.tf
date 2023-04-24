variable "project" {
  default     = "de-hires-project"
  description = "GCP project name"
  }

variable "region" {
  default = "europe-west4"
}

variable "zone" {
  default = "europe-west4-a"
}

variable "lake_bucket" {
  default = "bike_rental_extract"
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}