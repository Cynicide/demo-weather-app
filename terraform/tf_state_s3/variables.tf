variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket_name" {
  description = "AWS S3 Bucket"
  type        = string
  default     = "devtfstate"
}

