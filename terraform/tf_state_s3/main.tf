terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.38"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = var.aws_region
}

resource "aws_s3_bucket" "devtfstate"{
  bucket = var.s3_bucket_name

  tags = {
    Name =var.s3_bucket_name
    Environment = "interview-dev"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tfstate_encryption" {
  bucket = aws_s3_bucket.devtfstate.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_acl" "tfstate_acl" {
  bucket = aws_s3_bucket.devtfstate.bucket
  acl    = "private"
}