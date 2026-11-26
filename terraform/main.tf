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
      source                = "hashicorp/google-beta"
      version               = ">= 4.52, < 6"
      configuration_aliases = [google.service_principal_impersonation]
    }
  }
}

provider "google" {
  project = local.local_project_id
  batching {
    enable_batching = false
  }
}

provider "google" {
  alias                       = "service_principal_impersonation"
  impersonate_service_account = "${local.local_project_id}@${local.local_project_id}.iam.gserviceaccount.com"
  project                     = local.local_project_id
  billing_project             = local.local_project_id
  user_project_override       = true
  region                      = var.default_region
  zone                        = var.default_zone
  batching {
    enable_batching = false
  }
}

module "project" {
  count           = var.project_number == "" ? 1 : 0
  source          = "../terraform-modules/project"
  project_id      = local.local_project_id
  org_id          = var.org_id
  billing_account = var.billing_account
}

module "service-account" {
  source                = "../terraform-modules/service-account"
  project_id            = local.local_project_id
  org_id                = var.org_id
  impersonation_account = local.local_impersonation_account
  gcp_account_name      = var.gcp_account_name
  environment           = var.environment

  depends_on = [
    module.project
  ]
}

module "apis-batch-enable" {
  source         = "../terraform-modules/apis-batch-enable"
  project_id     = local.local_project_id
  project_number = var.project_number == "" ? module.project[0].output-project-number : var.project_number

  depends_on = [
    module.project,
    module.service-account
  ]
}

resource "time_sleep" "service_account_api_activation_time_delay" {
  create_duration = "60s"
  depends_on = [
    module.project,
    module.service-account,
    module.apis-batch-enable
  ]
}

module "org-policies" {
  count      = var.environment == "GITHUB_ENVIRONMENT" && var.org_id != "0" ? 1 : 0
  source     = "../terraform-modules/org-policies"
  providers  = { google = google.service_principal_impersonation }
  project_id = local.local_project_id

  depends_on = [
    module.project,
    module.service-account,
    module.apis-batch-enable,
    time_sleep.service_account_api_activation_time_delay
  ]
}

module "resources" {
  source    = "../terraform-modules/resources"
  providers = { google = google.service_principal_impersonation }

  gcp_account_name                = var.gcp_account_name
  project_id                      = local.local_project_id
  multi_region                    = var.multi_region
  vertex_ai_region                = var.vertex_ai_region
  random_extension                = random_string.project_random.result
  project_number                  = var.project_number == "" ? module.project[0].output-project-number : var.project_number
  deployment_service_account_name = var.deployment_service_account_name
  terraform_service_account       = module.service-account.deployment_service_account

  bigquery_citibike_tier0_dataset = var.bigquery_citibike_tier0_dataset
  bigquery_l400_ds_work_dataset   = var.bigquery_l400_ds_work_dataset
  l400_agentic_ds_bucket          = local.l400_agentic_ds_bucket
  l400_agentic_ds_code_bucket     = local.code_bucket

  depends_on = [
    module.project,
    module.service-account,
    module.apis-batch-enable,
    time_sleep.service_account_api_activation_time_delay,
    module.org-policies,
  ]
}

output "gcp_account_name" {
  value = var.gcp_account_name
}

output "project_id" {
  value = local.local_project_id
}

output "project_number" {
  value = var.project_number == "" ? module.project[0].output-project-number : var.project_number
}

output "org_id" {
  value = var.org_id
}

output "billing_account" {
  value = var.billing_account
}

output "region" {
  value = var.default_region
}

output "multi_region" {
  value = var.multi_region
}

output "vertex_ai_region" {
  value = var.vertex_ai_region
}

output "random_string" {
  value = random_string.project_random.result
}

output "deployment_service_account" {
  value = module.service-account.deployment_service_account
}

output "citibike_tier0_dataset" {
  value = var.bigquery_citibike_tier0_dataset
}

output "l400_ds_work_dataset" {
  value = var.bigquery_l400_ds_work_dataset
}

output "terraform-output-bucket" {
  value = local.code_bucket
}
