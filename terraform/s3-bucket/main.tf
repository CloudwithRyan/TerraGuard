terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

# ShipFleet shipment data bucket.
# INTENTIONALLY VULNERABLE: This configuration is for security testing only.

resource "aws_s3_bucket" "shipment_data" {
  bucket = "shipfleet-shipment-data-insecure-demo"

  tags = {
    Name = "ShipFleet Shipment Data"
  }
}

# VULNERABILITY: Allows objects in the bucket to be publicly readable.
resource "aws_s3_bucket_acl" "shipment_data" {
  bucket = aws_s3_bucket.shipment_data.id
  acl    = "public-read"
}

# VULNERABILITY: Allows anyone to download objects from the bucket.
resource "aws_s3_bucket_policy" "shipment_data" {
  bucket = aws_s3_bucket.shipment_data.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = "s3:GetObject"
        Resource = "${aws_s3_bucket.shipment_data.arn}/*"
      }
    ]
  })
}
# Remediation 1: Block public access to the S3 bucket.
resource "aws_s3_bucket_public_access_block" "shipment_data" {
  bucket = aws_s3_bucket.shipment_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Remediation 2: Enable server-side encryption using AES-256.
resource "aws_s3_bucket_server_side_encryption_configuration" "shipment_data" {
  bucket = aws_s3_bucket.shipment_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}