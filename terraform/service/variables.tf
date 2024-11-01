variable "app_name" {
  description = "The name of the application"
  type = string
  default = "uh-transcript-parser"
}

variable "az_count" {
    description = "The number of availability zones to use"
    type        = number
    default     = 2
}

variable "region" {
    description = "The AWS region to deploy to"
    type        = string
    default     = "eu-north-1"
}

variable "domain-name" {
    description = "The domain name to use for the application"
    type        = string
}
