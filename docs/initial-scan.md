# TerraGuard — Initial Security Scan

## Scan details

* **Tool:** Checkov
* **Version:** 3.3.30
* **Framework:** Terraform
* **Scanned directory:** `terraform/`
* **Branch:** `feature/vulnerable-s3-module`

## Baseline results

| Result         | Count |
| -------------- | ----: |
| Passed checks  |     6 |
| Failed checks  |    10 |
| Skipped checks |     0 |

## Key findings

The initial scan identified a publicly readable S3 ACL, a bucket policy allowing `s3:GetObject` to any principal, missing public access blocking, missing access logging, disabled versioning, and missing KMS encryption configuration.

Additional findings concerned event notifications, cross-region replication, and lifecycle configuration.

## Remediation plan

Remediate the required S3 security issues incrementally, using separate commits for individual fixes where practical. Re-run Checkov after each change and record the results to demonstrate the reduction in findings.

The final pipeline will be configured to block HIGH-severity findings while reporting lower-severity findings without blocking merges.
