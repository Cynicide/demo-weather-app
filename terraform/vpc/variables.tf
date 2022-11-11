variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_name" {
  description = "AWS EKS VPC"
  type        = string
  default     = "eks-vpc"
}
