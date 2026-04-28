#!/bin/bash
# Quick Start Script for AWS Cost Optimizer

set -e

echo "🚀 AWS Cost Optimizer - Quick Start"
echo "==================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured. Please run: aws configure"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Run scan
echo ""
echo "🔍 Scanning your AWS account..."
python3 scan.py --region us-east-1

# Generate fixes
echo ""
echo "🔨 Generating Terraform fixes..."
python3 generate-fixes.py

echo ""
echo "✅ Done! Check fixes.tf and run 'terraform plan' to review changes."
echo ""
echo "⚠️  REMEMBER: Review all changes carefully before running 'terraform apply'!"