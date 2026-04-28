# AWS Cost Optimizer

**Stop overpaying for AWS. Automatically detect waste and fix it in one command.**

## What It Does

- Scans your AWS account for cost waste (idle resources, unattached volumes, overprovisioned instances)
- Prioritizes fixes by estimated savings
- Generates Terraform code to apply fixes safely
- Shows you exactly what you'll save before making changes

## Quick Start

```bash
pip install -r requirements.txt
python scan.py --region us-east-1
python generate-fixes.py
terraform apply
```

## What It Finds

- [x] Unattached EBS volumes costing you money
- [x] Idle EC2 instances (low CPU utilization)
- [x] Overprovisioned RDS instances
- [x] Old EBS snapshots (past retention period)
- [x] Unassociated Elastic IPs
- [x] Unused NAT Gateways
- [x] S3 buckets with low/no usage

## Safety First

- Dry-run mode shows what would change
- Terraform plan reviewed before apply
- Backup snapshots before deletion
- Configurable exclusions (never tag production resources as deletable)

## License

MIT - Use freely, improvements welcome

**GitHub:** https://github.com/oconnorssoftware/aws-cost-optimizer

---

**Built by:** O'Connor's Software