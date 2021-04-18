variable "gcp_project_id" {}
variable "container_image" {}
variable "linear_personal_token" {
  sensitive = true
}
variable "asana_personal_token" {
  sensitive = true
}
variable "gcp_region" {
  default = "us-central1"
}
variable "gcp_pubsub_cloud_scheduler_name" {
  default = "linear-asana-sync"
}
variable "gcp_cloud_run_service_name" {
  default = "linear-asana-sync"
}
