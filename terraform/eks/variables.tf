variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "eks_cluster_name" {
  description = "EKS Cluster Name"
  type        = string
  default     = ""
}

variable "vpc_id" {
  description = "EKS VPC ID"
  type        = string
  default     = ""
}

variable "sg_name" {
  description = "AWS EKS Security Group Name"
  type        = string
  default     = "node_sg_dev"
}

variable "private_subnets" {
  description = "EKS VPC Private Subnets"
  type        = list(string)
  default     = []
}

variable "sg_id" {
  description = "EKS SG ID"
  type        = string
  default     = ""
}
