provider "google" {
  project = var.gcp_project_id
  region = var.gcp_region
  credentials = "service-account.json"
}

resource "google_cloud_run_service" "default" {
  name = var.gcp_cloud_run_service_name
  location = var.gcp_region

  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "1"
      }
    }
    spec {
      timeout_seconds = 3600
      containers {
        image = var.container_image
        env {
          name = "LINEAR_PERSONAL_TOKEN"
          value = var.linear_personal_token
        }
        env {
          name = "ASANA_PERSONAL_TOKEN"
          value = var.asana_personal_token
        }
      }
    }
  }

  metadata {
    annotations = {
      "autoscaling.knative.dev/maxScale" = "1"
    }
  }

  traffic {
    percent = 100
    latest_revision = true
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.default.location
  project = google_cloud_run_service.default.project
  service = google_cloud_run_service.default.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

resource "google_cloud_scheduler_job" "job" {
  depends_on = [
    google_cloud_run_service.default
  ]

  name = var.gcp_pubsub_cloud_scheduler_name
  description = "Triggers a Linear to Asana data sync"
  schedule = "0 * * * *"
  time_zone = "America/New_York"
  attempt_deadline = "3600s"

  http_target {
    http_method = "GET"
    uri = "${google_cloud_run_service.default.status[0].url}/linear-asana-sync/"
  }
}
