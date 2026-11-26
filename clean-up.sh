#!/bin/bash
# Reset local Terraform lock, state, and output files
rm -rf ./terraform/.terraform
rm -f ./terraform/.terraform.lock.hcl
rm -f ./terraform/terraform.tfstate
rm -f ./terraform/terraform.tfstate.backup
rm -f ./terraform/tf-output.json
rm -f ./tf.log
