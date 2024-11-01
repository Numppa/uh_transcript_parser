terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
    region = "eu-north-1"
}

resource "aws_ecr_repository" "backend_repository" {
  name = "${var.app_name}-backend"
}

resource "aws_ecr_repository" "frontend_repository" {
  name = "${var.app_name}-frontend"
}