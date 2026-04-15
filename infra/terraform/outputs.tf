output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.endpoint
  sensitive   = true
}

output "rds_arn" {
  description = "RDS PostgreSQL ARN"
  value       = aws_db_instance.postgres.arn
}

output "s3_bucket_arns" {
  description = "S3 bucket ARNs for data lake"
  value       = { for bucket in aws_s3_bucket.data_lake : bucket.id => bucket.arn }
}

output "security_group_ids" {
  description = "Security group IDs"
  value = {
    rds = aws_security_group.rds.id
    s3  = aws_security_group.s3.id
  }
}