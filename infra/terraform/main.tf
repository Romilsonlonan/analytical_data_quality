# =============================================================================
# Terraform Configuration - AWS Cloud
# ATENÇÃO: Este arquivo é usado apenas para deploy em nuvem AWS
# Para ambiente local, use docker-compose.yml
# =============================================================================

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = "industrial-logistics-platform"
      ManagedBy   = "terraform"
    }
  }
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "ilp-vpc-${var.environment}"
  }
}

resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "ilp-private-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "public" {
  count                   = 3
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "ilp-public-subnet-${count.index + 1}"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "ilp-igw"
  }
}

resource "aws_security_group" "rds" {
  name        = "ilp-rds-sg"
  description = "Security group for RDS PostgreSQL"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ilp-rds-sg"
  }
}

resource "aws_security_group" "s3" {
  name        = "ilp-s3-sg"
  description = "Security group for S3/MinIO access"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  tags = {
    Name = "ilp-s3-sg"
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "ilp-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "ilp-db-subnet-group"
  }
}

resource "aws_db_instance" "postgres" {
  identifier           = "ilp-postgres-${var.environment}"
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = var.db_instance_class
  allocated_storage    = var.db_allocated_storage
  max_allocated_storage = var.db_max_storage
  storage_encrypted    = true
  storage_type         = "gp3"

  db_name  = replace(var.project_name, "-", "_")
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = var.db_backup_retention
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"

  skip_final_snapshot       = var.environment != "prod"
  final_snapshot_identifier = var.environment == "prod" ? "ilp-postgres-prod-final" : null

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = {
    Name = "ilp-postgres-${var.environment}"
  }
}

resource "aws_s3_bucket" "data_lake" {
  for_each = toset(["bronze", "silver", "gold"])

  bucket = "${var.project_name}-${each.value}-${var.environment}"

  tags = {
    Name        = "${var.project_name}-${each.value}"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "data_lake" {
  for_each = aws_s3_bucket.data_lake
  bucket   = each.value.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption" "data_lake" {
  for_each = aws_s3_bucket.data_lake
  bucket   = each.value.id

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}