import json
import sys
from pathlib import Path

REPORT = Path("checkov-results.json")

# Block these checks because they concern public S3 exposure.
# Checkov's local report may not include severity metadata.
BLOCKING_CHECK_IDS = {
    "CKV_AWS_20",
    "CKV_AWS_57",
    "CKV2_AWS_6",
    "CKV_AWS_53",
    "CKV_AWS_54",
    "CKV_AWS_55",
    "CKV_AWS_56",
}

if not REPORT.exists():
    print("ERROR: Checkov JSON report was not generated.")
    sys.exit(2)

try:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
except (json.JSONDecodeError, OSError) as error:
    print(f"ERROR: Could not read Checkov report: {error}")
    sys.exit(2)

results = data.get("results", {})
findings = results.get("failed_checks", [])

if not isinstance(findings, list):
    print("ERROR: Unexpected Checkov report structure.")
    sys.exit(2)

blocking_findings = []

for finding in findings:
    check_id = finding.get("check_id", "Unknown")
    resource = finding.get("resource", "Unknown resource")
    severity = finding.get("severity")

    if severity and severity.upper() in {"HIGH", "CRITICAL"}:
        blocking_findings.append(finding)
        print(f"BLOCKING ({severity}): {check_id} on {resource}")
    elif check_id in BLOCKING_CHECK_IDS:
        blocking_findings.append(finding)
        print(f"BLOCKING (security policy): {check_id} on {resource}")
    else:
        print(f"WARNING: {check_id} on {resource}")

print(f"\nTotal findings: {len(findings)}")
print(f"Blocking findings: {len(blocking_findings)}")

if blocking_findings:
    print("FAILED: Blocking security findings must be resolved.")
    sys.exit(1)

print("PASSED: No blocking findings under the configured policy.")
sys.exit(0)