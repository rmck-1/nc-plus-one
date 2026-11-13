terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "6.72"
      }
    }
    backend "s3" {
    bucket = "rm-tf-remote-state-240837126900-eu-west-2-an"
    key    = "state/terraform.tfstate"
    region = "eu-west-2"
    use_lockfile = true
  }
}

provider "aws" {
    region = "eu-west-2"

default_tags {
  tags = {
    environment = "Test"
    purpose = "Learning API terraform and AWS"
    managed_by = "terraform"
    iaac_location = "northcoders/projects/nc-plus-one/terra"
  }
}
}