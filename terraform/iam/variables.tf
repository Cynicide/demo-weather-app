variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "eks_role_name" {
  description = "EKS Role Name"
  type        = string
  default     = "dev-eks-iam-role"
}

