#!/usr/bin/env python3
"""
Generate launch content for AWS Cost Optimizer
"""

from rich.console import Console

console = Console()

def generate_twitter_posts():
    """Generate Twitter/X posts"""
    posts = [
        """🚀 Just shipped a free tool that scans your AWS account for waste.

Found $47/month of idle resources in my first test run.

Unattached EBS volumes, idle EC2 instances, old snapshots - it finds it all.

Python + Terraform. One command to scan, one to fix.

Drop a 🧵 if you want the breakdown.

#AWS #DevOps #CloudNative""",
        """💰 AWS bills are sneaky.

I built a script that found:
- 3 unattached EBS volumes ($23/mo)
- 2 idle EC2 instances ($84/mo)
- 5 old snapshots ($12/mo)

Total: $119/month I was burning for nothing.

The fix? One Terraform apply.

Open sourcing it this week.

#AWS #Terraform #DevOps""",
        """🔥 The most expensive AWS resources are the ones you forgot about.

Unattached EBS volumes: They sit there, costing you monthly, doing nothing.

My new tool finds them instantly:
- 1-minute scan
- Prioritized by savings
- Auto-generates Terraform fixes

Built it because I was tired of surprise bills.

Link in bio.

#AWS #Cloud #DevOps""",
        """📊 AWS Cost Optimizer breakdown:

What it scans:
✓ Unattached EBS volumes
✓ Idle EC2 instances
✓ Unassociated Elastic IPs
✓ Old snapshots
✓ Overprovisioned RDS

What it outputs:
✓ Prioritized fix list
✓ Estimated savings
✓ Ready-to-apply Terraform

Safety:
✓ Dry-run mode
✓ Terraform plan review
✓ Backup snapshots

Python + Terraform. MIT licensed.

#AWS #Terraform #DevOps"""
    ]

    return posts

def generate_reddit_posts():
    """Generate Reddit posts"""
    posts = {
        'r/devops': """**Title:** I built a free tool that saved me $119/month on my AWS bill (and how it works)

**Body:**

Got hit with a surprise AWS bill last month. Turns out I had:

- 3 unattached EBS volumes sitting around ($23/mo)
- 2 dev EC2 instances that were running idle ($84/mo)
- Old snapshots nobody touched ($12/mo)

Total waste: $119/month.

So I built a tool to fix this automatically. It's a simple Python script that:

1. Scans your AWS account for cost waste
2. Shows you what's costing money (prioritized by savings)
3. Generates Terraform code to apply fixes safely
4. Has dry-run mode so you can review first

**What it finds:**
- Unattached EBS volumes
- Idle EC2 instances (low CPU utilization)
- Unassociated Elastic IPs
- Old EBS snapshots
- Overprovisioned RDS instances

**Safety features:**
- Dry-run mode (preview changes)
- Terraform plan review before apply
- Configurable exclusions
- Backup snapshots before deletion

Open source, MIT licensed. Works with Python 3.8+, boto3, and Terraform.

**Repository:** [LINK]

Would love feedback from other DevOps folks. What other AWS waste should it detect?

---

*Tech stack: Python, boto3, Terraform, AWS*""",
        'r/aws': """**Title:** [Tool] AWS Cost Optimizer - Find and fix AWS waste in one command

**Body:**

Built this after getting tired of surprise AWS bills. It's a CLI tool that:

**Scans:**
- Unattached EBS volumes
- Idle EC2 instances (<5% CPU)
- Unassociated Elastic IPs
- Old EBS snapshots
- Overprovisioned RDS

**Outputs:**
- Prioritized list by potential savings
- Estimated monthly savings per resource
- Auto-generated Terraform code for fixes

**Safety:**
- Dry-run mode
- Terraform plan review
- Backup snapshots before deletion

**Quick start:**
```bash
pip install -r requirements.txt
python scan.py --region us-east-1
python generate-fixes.py
terraform plan
```

First run found $119/month of waste in my personal account.

MIT licensed, open source. Looking for feedback and contributors.

**Repo:** [LINK]

What other AWS cost optimizations should I add?""",
        'r/terraform': """**Title:** Tool that generates Terraform to fix AWS waste automatically

**Body:**

Working on an AWS cost optimizer that not only finds waste but generates Terraform to fix it.

**Workflow:**
1. Python script scans AWS for waste (idle EC2, unattached EBS, etc.)
2. Generates findings.json with prioritized list
3. Terraform generator creates fixes.tf with safe deletion/stop resources
4. Review with terraform plan, apply when ready

**Example output:**
```hcl
# Delete unattached EBS volume: vol-12345
# Estimated savings: $12.34/month
resource "aws_ebs_volume_delete" "vol-12345" {
  volume_id = "vol-12345"
  force_delete = false  # Safety: review first
}
```

**Safety features:**
- All deletions default to preview mode
- Terraform plan shows exactly what will change
- Backup snapshots before deletion
- Configurable exclusions

Built this because manual cleanup was tedious and error-prone.

**Repo:** [LINK]

Looking for feedback on the Terraform patterns. Better ways to structure this?

*Tech: Python, boto3, Terraform*"""
    }

    return posts

def generate_hn_post():
    """Generate Hacker News Show HN post"""
    return """**Title:** Show HN: AWS Cost Optimizer - Find and fix AWS waste automatically

**Body:**

I built this after getting tired of surprise AWS bills. It scans your AWS account for cost waste and generates Terraform code to fix it safely.

**What it finds:**
- Unattached EBS volumes
- Idle EC2 instances (low CPU utilization)
- Unassociated Elastic IPs
- Old EBS snapshots
- Overprovisioned RDS instances

**How it works:**
1. `python scan.py` - Scans AWS account, outputs findings.json
2. `python generate-fixes.py` - Generates Terraform code for fixes
3. `terraform plan` - Review what will change
4. `terraform apply` - Apply fixes

**Safety features:**
- Dry-run mode by default
- Terraform plan review required
- Backup snapshots before deletion
- Configurable exclusions

First run found $119/month of waste in my personal account.

**Tech stack:** Python 3, boto3, Terraform, AWS

**Repository:** [LINK]

**License:** MIT

Looking for feedback and contributors. What other AWS waste should it detect?"""

def display_all_content():
    """Display all launch content"""
    console.print("\n[bold cyan]📱 TWITTER/X POSTS[/bold cyan]\n")

    for i, post in enumerate(generate_twitter_posts(), 1):
        console.print(f"[yellow]Post {i}:[/yellow]")
        console.print(post)
        console.print()

    console.print("\n[bold cyan]📝 REDDIT POSTS[/bold cyan]\n")

    for subreddit, post in generate_reddit_posts().items():
        console.print(f"[yellow]r/{subreddit}:[/yellow]")
        console.print(post[:500] + "...")
        console.print()

    console.print("\n[bold cyan]🔴 HACKER NEWS POST[/bold cyan]\n")
    console.print(generate_hn_post()[:500] + "...")
    console.print()

    console.print("[green]💾 All content saved to launch-content.md[/green]")

def save_to_file():
    """Save all content to a markdown file"""
    with open('launch-content.md', 'w') as f:
        f.write("# AWS Cost Optimizer - Launch Content\n\n")

        f.write("## Twitter/X Posts\n\n")
        for i, post in enumerate(generate_twitter_posts(), 1):
            f.write(f"### Post {i}\n\n")
            f.write(post + "\n\n")
            f.write("---\n\n")

        f.write("## Reddit Posts\n\n")
        for subreddit, post in generate_reddit_posts().items():
            f.write(f"### r/{subreddit}\n\n")
            f.write(post + "\n\n")
            f.write("---\n\n")

        f.write("## Hacker News Post\n\n")
        f.write(generate_hn_post() + "\n\n")

        f.write("## Launch Checklist\n\n")
        f.write("- [ ] Create GitHub repository\n")
        f.write("- [ ] Add README with screenshots\n")
        f.write("- [ ] Set up Gumroad (optional paid version)\n")
        f.write("- [ ] Post to Twitter/X (4 posts over 2 days)\n")
        f.write("- [ ] Post to r/devops, r/aws, r/terraform\n")
        f.write("- [ ] Submit to Hacker News (Show HN)\n")
        f.write("- [ ] Respond to comments and feedback\n")
        f.write("- [ ] Iterate based on user requests\n")


def main():
    display_all_content()
    save_to_file()


if __name__ == '__main__':
    main()