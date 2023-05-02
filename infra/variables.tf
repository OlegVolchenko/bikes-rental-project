variable "project" {
  default     = <project name>
  description = "GCP project name"
  }

variable "region" {
  default = <region>
}

variable "zone" {
  default = <zone>
}

variable "lake_bucket" {
  default = "bike_rental_extract"
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}