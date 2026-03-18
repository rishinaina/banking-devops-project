variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "banking-api"
}

variable "db_username" {
  description = "RDS username"
  type        = string
  default     = "bankuser"
}

variable "db_password" {
  description = "RDS password"
  type        = string
  sensitive   = true
}

variable "public_key_path" {
  description = "Path to SSH public key"
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to SSH"
  type        = string
  default     = "0.0.0.0/0"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}
