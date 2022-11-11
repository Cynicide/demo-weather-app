terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.38"
    }
  }
  backend "s3" {
    bucket = "amdevtfstate"
    key    = "eks-sg"
    region = "us-east-1"
  }
}

provider "aws" {
  profile = "default"
  region  = var.aws_region
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.26.6"

  cluster_name    = var.eks_cluster_name
  cluster_version = "1.22"

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnets

  eks_managed_node_group_defaults = {
    ami_type = "AL2_x86_64"

    attach_cluster_primary_security_group = true
    create_security_group = false
  }

  node_security_group_tags = {
      "kubernetes.io/cluster/${var.eks_cluster_name}" = null
  }

  eks_managed_node_groups = {
    one = {
      name = "apps-node-group"

      instance_types = ["t3.small"]

      min_size     = 1
      max_size     = 3
      desired_size = 2

      pre_bootstrap_user_data = <<-EOT
      echo 'bootstrap data'
      EOT

      vpc_security_group_ids = [
        aws_security_group.node_sg.id
      ]
    }
  }

  tags = {
    Name = var.eks_cluster_name
    Environment = "interview-dev"
  }
}

resource "aws_security_group" "node_sg" {
  name        = var.sg_name
  vpc_id      = var.vpc_id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      "10.0.0.0/8",
    ]
  }
  
  tags = {
    Name = var.sg_name
    Environment = "interview-dev"
  }
}