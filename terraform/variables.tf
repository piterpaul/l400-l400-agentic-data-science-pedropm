####################################################################################
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
####################################################################################

variable "gcp_account_name" {
  type        = string
  description = "The user account running the deployment (e.g. admin@argolis.altostrat.com)."
  validation {
    condition     = length(var.gcp_account_name) > 0
    error_message = "The gcp_account_name is required."
  }
}

variable "project_id" {
  type        = string
  description = "The GCP Project ID or prefix to generate (e.g. l400-agentic-ds-xxxxxxxxxx)."
  validation {
    condition     = length(var.project_id) > 0
    error_message = "The project_id is required."
  }
}

variable "project_number" {
  type        = string
  description = "The GCP Project Number (only set when deploying into an existing project)."
  default     = ""
}

variable "deployment_service_account_name" {
  type        = string
  description = "Optional existing service account for deployment."
  default     = ""
}

variable "org_id" {
  type        = string
  description = "The organization ID for the deployment (use '0' for existing project non-org-admin)."
  default     = ""
  validation {
    condition     = length(var.org_id) > 0
    error_message = "The org_id is required."
  }
}

variable "billing_account" {
  type        = string
  description = "The billing account ID used when creating a new greenfield GCP project."
  default     = ""
}

variable "default_region" {
  type        = string
  description = "Default GCP region for deployment."
  default     = "us-central1"
  validation {
    condition     = length(var.default_region) > 0
    error_message = "The region is required."
  }
}

variable "default_zone" {
  type        = string
  description = "Default GCP zone in the region."
  default     = "us-central1-a"
  validation {
    condition     = length(var.default_zone) > 0
    error_message = "The zone is required."
  }
}

variable "bigquery_citibike_tier0_dataset" {
  type        = string
  description = "BigQuery dataset for Part 1 Guided Tier 0 NYC Citi Bike baseline."
  default     = "citibike_tier0"
  validation {
    condition     = length(var.bigquery_citibike_tier0_dataset) > 0
    error_message = "The bigquery_citibike_tier0_dataset is required."
  }
}

variable "bigquery_l400_ds_work_dataset" {
  type        = string
  description = "BigQuery dataset for Part 2 Solo Tier 1 / Tier 2 build."
  default     = "l400_ds_work"
  validation {
    condition     = length(var.bigquery_l400_ds_work_dataset) > 0
    error_message = "The bigquery_l400_ds_work_dataset is required."
  }
}

variable "multi_region" {
  type        = string
  description = "Multi-region location for BigQuery datasets and GCS buckets ('US' or 'EU')."
  default     = "US"
  validation {
    condition     = length(var.multi_region) > 0
    error_message = "The multi_region is required."
  }
}

variable "vertex_ai_region" {
  type        = string
  description = "The GCP region for Vertex AI."
  default     = "us-central1"
  validation {
    condition     = length(var.vertex_ai_region) > 0
    error_message = "The vertex_ai_region is required."
  }
}

variable "environment" {
  type        = string
  description = "Deployment environment marker."
  default     = "GITHUB_ENVIRONMENT" #_REPLACEMENT_MARKER (do not remove this text of change the spacing)
}

resource "random_string" "project_random" {
  length  = 10
  upper   = false
  lower   = true
  numeric = true
  special = false
}

locals {
  local_project_id            = var.project_number == "" ? "${var.project_id}-${random_string.project_random.result}" : var.project_id
  l400_agentic_ds_bucket      = "l400-agentic-ds-data-${random_string.project_random.result}"
  code_bucket                 = "l400-agentic-ds-code-${random_string.project_random.result}"
  local_impersonation_account = var.deployment_service_account_name == "" ? "user:${var.gcp_account_name}" : length(regexall("^serviceAccount:", var.deployment_service_account_name)) > 0 ? "${var.deployment_service_account_name}" : "serviceAccount:${var.deployment_service_account_name}"
}
