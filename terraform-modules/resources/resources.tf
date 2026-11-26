####################################################################################
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
####################################################################################

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google-beta"
      version = "5.35.0"
    }
  }
}

variable "gcp_account_name" {}
variable "project_id" {}
variable "multi_region" {}
variable "vertex_ai_region" {}
variable "random_extension" {}
variable "project_number" {}
variable "deployment_service_account_name" {}
variable "terraform_service_account" {}

variable "bigquery_citibike_tier0_dataset" {}
variable "bigquery_l400_ds_work_dataset" {}
variable "l400_agentic_ds_bucket" {}
variable "l400_agentic_ds_code_bucket" {}

locals {
  # Pre-provision "default" subnets with Private Google Access across all 4 US compute fallback
  # regions (plus var.vertex_ai_region if customized) so Dataproc Serverless, Dataflow, and
  # Vertex AI jobs work out-of-the-box in any US compute region during a regional stockout.
  compute_subnet_cidrs = merge(
    {
      "us-central1" = "10.1.0.0/16"
      "us-east1"    = "10.2.0.0/16"
      "us-east4"    = "10.3.0.0/16"
      "us-west1"    = "10.4.0.0/16"
    },
    contains(["us-central1", "us-east1", "us-east4", "us-west1"], var.vertex_ai_region) ? {} : {
      (var.vertex_ai_region) = "10.5.0.0/16"
    }
  )

  # Default Compute Engine SA worker roles required when Dataproc Serverless, Dataflow,
  # Vertex AI CustomJob, or Cloud Build executes in an Argolis project.
  compute_sa_roles = toset([
    "roles/dataproc.worker",
    "roles/dataflow.worker",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/bigquery.readSessionUser",
    "roles/storage.objectAdmin",
    "roles/aiplatform.user",
    "roles/cloudbuild.builds.builder",
  ])
}

# Data bucket stays in US multi-region alongside BigQuery datasets (citibike_tier0, l400_ds_work)
# and bigquery-public-data.* so LOAD DATA, BigLake, and spark-bigquery-connector temporaryGcsBucket
# operate without cross-location load errors.
resource "google_storage_bucket" "google_storage_bucket_l400_agentic_ds_bucket" {
  project                     = var.project_id
  name                        = var.l400_agentic_ds_bucket
  location                    = var.multi_region
  force_destroy               = true
  uniform_bucket_level_access = true
}

# Code & compute staging bucket is single-region (var.vertex_ai_region, default us-central1)
# because Vertex AI Custom Training (staging_bucket) and Dataproc Serverless (--deps-bucket)
# require a single-region bucket in the compute region.
resource "google_storage_bucket" "google_storage_bucket_l400_agentic_ds_code_bucket" {
  project                     = var.project_id
  name                        = var.l400_agentic_ds_code_bucket
  location                    = var.vertex_ai_region
  force_destroy               = true
  uniform_bucket_level_access = true
}

####################################################################################
# Default VPC Network (Auto-Mode), Multi-Region US Private Google Access, Firewall & NAT
# Argolis projects do not create a default network automatically. Creating "default"
# with auto_create_subnetworks = true and enabling Private Google Access on the
# auto-created regional "default" subnets allows Dataproc Serverless and Dataflow jobs
# in us-central1, us-east1, us-east4, or us-west1 to launch without --subnet flags.
####################################################################################
data "google_client_config" "current" {}

resource "google_compute_network" "default_network" {
  project                 = var.project_id
  name                    = "default"
  description             = "Default auto-mode VPC network for serverless Spark, Dataflow, and Vertex AI"
  auto_create_subnetworks = true
  mtu                     = 1460
}

resource "terraform_data" "enable_subnet_pga" {
  for_each = local.compute_subnet_cidrs

  triggers_replace = [
    google_compute_network.default_network.id,
    each.key,
  ]

  provisioner "local-exec" {
    command = <<-EOT
      for attempt in 1 2 3 4 5 6; do
        code=$(curl -s -o /dev/null -w "%%{http_code}" -X POST \
          -H "Authorization: Bearer ${data.google_client_config.current.access_token}" \
          -H "Content-Type: application/json" \
          -d '{"privateIpGoogleAccess": true}' \
          "https://compute.googleapis.com/compute/v1/projects/${var.project_id}/regions/${each.key}/subnetworks/default/setPrivateIpGoogleAccess")
        if [ "$code" = "200" ]; then
          exit 0
        fi
        sleep 3
      done
      exit 1
    EOT
  }

  depends_on = [
    google_compute_network.default_network
  ]
}

# Dataproc Serverless and Dataflow require internal communication across driver/worker nodes.
resource "google_compute_firewall" "default_allow_internal" {
  project   = var.project_id
  name      = "default-allow-internal"
  network   = google_compute_network.default_network.id
  direction = "INGRESS"

  allow {
    protocol = "icmp"
  }
  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }
  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  source_ranges = ["10.0.0.0/8"]

  depends_on = [
    terraform_data.enable_subnet_pga
  ]
}

resource "google_compute_router" "nat_router" {
  for_each = local.compute_subnet_cidrs
  project  = var.project_id
  name     = "nat-router-${each.key}"
  region   = each.key
  network  = google_compute_network.default_network.id

  depends_on = [
    google_compute_firewall.default_allow_internal
  ]
}

resource "google_compute_router_nat" "nat_config" {
  for_each                           = local.compute_subnet_cidrs
  project                            = var.project_id
  name                               = "nat-config-${each.key}"
  router                             = google_compute_router.nat_router[each.key].name
  region                             = each.key
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  depends_on = [
    google_compute_router.nat_router
  ]
}

resource "google_project_iam_member" "compute_sa_roles" {
  for_each = local.compute_sa_roles
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${var.project_number}-compute@developer.gserviceaccount.com"
}

resource "google_bigquery_dataset" "google_bigquery_dataset_citibike_tier0" {
  project                    = var.project_id
  dataset_id                 = var.bigquery_citibike_tier0_dataset
  friendly_name              = var.bigquery_citibike_tier0_dataset
  description                = "Part 1 Guided Tier 0 NYC Citi Bike demand forecasting baseline dataset."
  location                   = var.multi_region
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "google_bigquery_dataset_l400_ds_work" {
  project                    = var.project_id
  dataset_id                 = var.bigquery_l400_ds_work_dataset
  friendly_name              = var.bigquery_l400_ds_work_dataset
  description                = "Part 2 Solo Tier 1 / Tier 2 Agentic Data Science build workspace dataset."
  location                   = var.multi_region
  delete_contents_on_destroy = true
}

resource "google_project_iam_member" "gcp_roles_datalineage_admin" {
  project = var.project_id
  role    = "roles/datalineage.admin"
  member  = "user:${var.gcp_account_name}"
}

resource "google_bigquery_connection" "vertex_ai_connection" {
  project       = var.project_id
  connection_id = "vertex-ai"
  location      = var.multi_region
  friendly_name = "vertex-ai"
  description   = "Vertex AI connection for BigQuery ML and Foundation Models"
  cloud_resource {}
}

resource "google_project_iam_member" "vertex_ai_connection_vertex_user_role" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_bigquery_connection.vertex_ai_connection.cloud_resource[0].service_account_id}"

  depends_on = [
    google_bigquery_connection.vertex_ai_connection
  ]
}

resource "google_bigquery_connection" "biglake_connection" {
  project       = var.project_id
  connection_id = "biglake-connection"
  location      = var.multi_region
  friendly_name = "biglake-connection"
  description   = "BigLake connection for Cloud Storage tables"
  cloud_resource {}
}

resource "time_sleep" "biglake_connection_time_delay" {
  depends_on      = [google_bigquery_connection.biglake_connection]
  create_duration = "15s"
}

resource "google_project_iam_member" "bq_connection_iam_object_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_bigquery_connection.biglake_connection.cloud_resource[0].service_account_id}"

  depends_on = [
    time_sleep.biglake_connection_time_delay
  ]
}

resource "google_storage_bucket_iam_member" "bq_connection_data_bucket_user" {
  bucket = google_storage_bucket.google_storage_bucket_l400_agentic_ds_bucket.name
  role   = "roles/storage.objectUser"
  member = "serviceAccount:${google_bigquery_connection.biglake_connection.cloud_resource[0].service_account_id}"

  depends_on = [
    time_sleep.biglake_connection_time_delay
  ]
}

resource "google_storage_bucket_iam_member" "bq_connection_data_bucket_reader" {
  bucket = google_storage_bucket.google_storage_bucket_l400_agentic_ds_bucket.name
  role   = "roles/storage.legacyBucketReader"
  member = "serviceAccount:${google_bigquery_connection.biglake_connection.cloud_resource[0].service_account_id}"

  depends_on = [
    time_sleep.biglake_connection_time_delay
  ]
}
