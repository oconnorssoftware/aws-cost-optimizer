#!/usr/bin/env python3
"""
AWS Cost Optimizer - Scan your AWS account for waste
"""

import boto3
import json
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class CostScanner:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.findings = []

    def add_finding(self, resource_type, resource_id, issue, monthly_cost, severity):
        self.findings.append({
            'type': resource_type,
            'id': resource_id,
            'issue': issue,
            'monthly_cost': monthly_cost,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        })

    def scan_unattached_ebs(self):
        """Find unattached EBS volumes"""
        console.print("[yellow]🔍 Scanning for unattached EBS volumes...[/yellow]")

        volumes = self.ec2.describe_volumes(Filters=[
            {'Name': 'status', 'Values': ['available']}
        ])

        total_cost = 0
        for vol in volumes['Volumes']:
            size_gb = vol['Size']
            volume_type = vol.get('VolumeType', 'gp2')

            # Rough cost estimates (us-east-1 pricing)
            cost_per_gb = {
                'gp2': 0.10,
                'gp3': 0.08,
                'io1': 0.125,
                'io2': 0.125,
                'standard': 0.05,
                'st1': 0.045,
                'sc1': 0.025
            }

            monthly_cost = size_gb * cost_per_gb.get(volume_type, 0.10)
            total_cost += monthly_cost

            self.add_finding(
                'EBS Volume',
                vol['VolumeId'],
                'Unattached volume',
                round(monthly_cost, 2),
                'HIGH' if monthly_cost > 10 else 'MEDIUM'
            )

        console.print(f"[green]✓ Found {len(volumes['Volumes'])} unattached volumes, costing ~${round(total_cost, 2)}/month[/green]")
        return total_cost

    def scan_idle_ec2(self):
        """Find EC2 instances with low CPU utilization"""
        console.print("[yellow]🔍 Scanning for idle EC2 instances...[/yellow]")

        instances = self.ec2.describe_instances()
        total_cost = 0

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] != 'running':
                    continue

                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']

                # Check CPU over last 7 days
                end_time = datetime.utcnow()
                start_time = end_time - timedelta(days=7)

                try:
                    stats = self.cloudwatch.get_metric_statistics(
                        Namespace='AWS/EC2',
                        MetricName='CPUUtilization',
                        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                        StartTime=start_time,
                        EndTime=end_time,
                        Period=86400,  # Daily stats
                        Statistics=['Average']
                    )

                    if stats['Datapoints']:
                        avg_cpu = sum(d['Average'] for d in stats['Datapoints']) / len(stats['Datapoints'])

                        # Rough instance pricing (simplified)
                        hourly_cost = {
                            't2.micro': 0.0116,
                            't2.small': 0.023,
                            't2.medium': 0.0464,
                            't3.micro': 0.0105,
                            't3.small': 0.0208,
                            't3.medium': 0.0416,
                            'm5.large': 0.096,
                            'm5.xlarge': 0.192,
                            'c5.large': 0.085,
                            'c5.xlarge': 0.17,
                        }

                        hourly = hourly_cost.get(instance_type, 0.1)
                        monthly_cost = hourly * 730  # hours in a month

                        if avg_cpu < 5:  # Less than 5% CPU average
                            total_cost += monthly_cost
                            self.add_finding(
                                'EC2 Instance',
                                instance_id,
                                f'Low CPU utilization ({avg_cpu:.1f}%)',
                                round(monthly_cost, 2),
                                'HIGH' if monthly_cost > 50 else 'MEDIUM'
                            )
                        elif avg_cpu < 15:
                            self.add_finding(
                                'EC2 Instance',
                                instance_id,
                                f'Underutilized (CPU {avg_cpu:.1f}%) - consider downsizing',
                                round(monthly_cost * 0.4, 2),  # Potential savings if downsized
                                'LOW'
                            )

                except Exception as e:
                    console.print(f"[red]⚠ Could not get metrics for {instance_id}: {e}[/red]")

        console.print(f"[green]✓ Found potentially idle instances, could save ~${round(total_cost, 2)}/month[/green]")
        return total_cost

    def scan_unassociated_eips(self):
        """Find Elastic IPs not associated with instances"""
        console.print("[yellow]🔍 Scanning for unassociated Elastic IPs...[/yellow]")

        addresses = self.ec2.describe_addresses(Filters=[
            {'Name': 'association-id', 'Values': ['']}
        ])

        # Elastic IP costs $0.005/hour when not attached = ~$3.65/month
        cost_per_eip = 3.65
        total_cost = len(addresses['Addresses']) * cost_per_eip

        for addr in addresses['Addresses']:
            self.add_finding(
                'Elastic IP',
                addr.get('PublicIp', addr['AllocationId']),
                'Unassociated Elastic IP',
                cost_per_eip,
                'LOW'
            )

        console.print(f"[green]✓ Found {len(addresses['Addresses'])} unassociated Elastic IPs, costing ~${round(total_cost, 2)}/month[/green]")
        return total_cost

    def scan_old_snapshots(self):
        """Find old EBS snapshots"""
        console.print("[yellow]🔍 Scanning for old EBS snapshots...[/yellow]")

        snapshots = self.ec2.describe_snapshots(OwnerIds=['self'])

        # Assume 30-day retention is standard, anything older is waste
        cutoff_date = datetime.now() - timedelta(days=30)
        total_cost = 0

        for snap in snapshots['Snapshots']:
            snap_date = snap['StartTime'].replace(tzinfo=None)
            if snap_date < cutoff_date:
                size_gb = snap['VolumeSize']
                monthly_cost = size_gb * 0.05  # Rough snapshot cost

                total_cost += monthly_cost
                self.add_finding(
                    'EBS Snapshot',
                    snap['SnapshotId'],
                    f'Snapshot older than 30 days ({snap_date.strftime("%Y-%m-%d")})',
                    round(monthly_cost, 2),
                    'LOW'
                )

        console.print(f"[green]✓ Found old snapshots, could save ~${round(total_cost, 2)}/month[/green]")
        return total_cost

    def display_findings(self):
        """Display all findings in a nice table"""
        if not self.findings:
            console.print("[green]🎉 No cost issues found! Your AWS account is optimized.[/green]")
            return

        console.print("\n")
        console.print(Panel.fit("[bold red]COST FINDINGS[/bold red]", padding=(1, 2)))

        table = Table(title="Potential Savings")
        table.add_column("Type", style="cyan")
        table.add_column("ID", style="yellow")
        table.add_column("Issue", style="white")
        table.add_column("Monthly Cost", style="red", justify="right")
        table.add_column("Severity", style="bold")

        total_savings = 0

        for finding in sorted(self.findings, key=lambda x: x['monthly_cost'], reverse=True):
            severity_color = {
                'HIGH': 'red',
                'MEDIUM': 'yellow',
                'LOW': 'green'
            }[finding['severity']]

            table.add_row(
                finding['type'],
                finding['id'],
                finding['issue'],
                f"${finding['monthly_cost']}",
                f"[{severity_color}]{finding['severity']}[/{severity_color}]"
            )
            total_savings += finding['monthly_cost']

        console.print(table)
        console.print(f"\n[bold green]Total Potential Monthly Savings: ${round(total_savings, 2)}[/bold green]\n")

        return total_savings

    def save_findings(self, filename='findings.json'):
        """Save findings to JSON for the fix generator"""
        with open(filename, 'w') as f:
            json.dump(self.findings, f, indent=2)
        console.print(f"[cyan]💾 Findings saved to {filename}[/cyan]")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Scan AWS account for cost waste')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--output', default='findings.json', help='Output JSON file')
    args = parser.parse_args()

    console.print("[bold cyan]🚀 AWS Cost Optimizer Scanner[/bold cyan]")
    console.print(f"Scanning region: {args.region}\n")

    scanner = CostScanner(region=args.region)

    scanner.scan_unattached_ebs()
    scanner.scan_idle_ec2()
    scanner.scan_unassociated_eips()
    scanner.scan_old_snapshots()

    savings = scanner.display_findings()
    scanner.save_findings(args.output)

    console.print("\n[cyan]Next: Run 'python generate-fixes.py' to create Terraform code for fixes[/cyan]")


if __name__ == '__main__':
    main()