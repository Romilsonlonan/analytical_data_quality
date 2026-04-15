# =============================================================================
# AWS Variables - ATENÇÃO: Usar apenas para deploy em nuvem AWS
# Para ambiente local, estes valores não são utilizados
# =============================================================================

variable "aws_region" {
  description = "AWS region for resources (nuvem apenas)"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod) - nuvm apenas"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "ilp"
}

variable "vpc_cidr" {
  description = "VPC CIDR block (nuvem apenas)"
  type        = string
  default     = "10.0.0.0/16"
}

variable "db_instance_class" {
  description = "RDS instance class (nuvem apenas)"
  type        = string
  default     = "db.t3.medium"
}

variable "db_allocated_storage" {
  description = "Initial allocated storage for RDS (GB) (nuvem apenas)"
  type        = number
  default     = 100
}

variable "db_max_storage" {
  description = "Maximum allocated storage for RDS (GB) (nuvem apenas)"
  type        = number
  default     = 500
}

variable "db_username" {
  description = "Master username for RDS (nuvem apenas)"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Master password for RDS (nuvem apenas)"
  type        = string
  sensitive   = true
}

variable "db_backup_retention" {
  description = "Backup retention period in days (nuvem apenas)"
  type        = number
  default     = 7
}