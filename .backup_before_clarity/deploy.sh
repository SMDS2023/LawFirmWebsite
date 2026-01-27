#!/bin/bash
# Bluehost FTP Deployment Script (for Git Bash)
# This script uploads your website files to Bluehost via FTP

echo "========================================"
echo "Bluehost Deployment Script"
echo "========================================"
echo ""

# Check if deploy-config.json exists
if [ ! -f "deploy-config.json" ]; then
    echo "ERROR: deploy-config.json not found!"
    echo ""
    echo "Please create deploy-config.json based on deploy-config-template.json"
    echo "Steps:"
    echo "  1. Copy deploy-config-template.json to deploy-config.json"
    echo "  2. Fill in your Bluehost FTP credentials"
    echo "  3. Run this script again"
    exit 1
fi

# Load configuration using Python (available in Git Bash)
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please install Python or use deploy.ps1 instead."
    exit 1
fi

# Parse JSON config
HOST=$(python -c "import json; print(json.load(open('deploy-config.json'))['host'])")
USERNAME=$(python -c "import json; print(json.load(open('deploy-config.json'))['username'])")
PASSWORD=$(python -c "import json; print(json.load(open('deploy-config.json'))['password'])")
REMOTE_PATH=$(python -c "import json; print(json.load(open('deploy-config.json'))['remote_path'])")
PORT=$(python -c "import json; print(json.load(open('deploy-config.json'))['port'])")

echo "Configuration loaded:"
echo "  Host: $HOST"
echo "  Username: $USERNAME"
echo "  Remote Path: $REMOTE_PATH"
echo ""

# Check if lftp is available
if ! command -v lftp &> /dev/null; then
    echo "WARNING: lftp not found!"
    echo ""
    echo "Please install lftp or use deploy.ps1 with WinSCP instead."
    echo ""
    echo "To install lftp on Windows:"
    echo "  - Via Chocolatey: choco install lftp"
    echo "  - Or use deploy.ps1 with WinSCP"
    exit 1
fi

echo "Starting deployment..."
echo ""

# Deploy using lftp
lftp -c "
set ftp:ssl-allow no;
open -u $USERNAME,$PASSWORD ftp://$HOST:$PORT;
cd $REMOTE_PATH;
mirror --reverse --delete --verbose --exclude .git/ --exclude deploy-config.json --exclude deploy.ps1 --exclude deploy.sh --exclude deploy.log --exclude .gitignore --exclude README.md --exclude deploy-config-template.json ./ ./;
bye
"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Deployment completed successfully!"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Deployment failed!"
    echo "========================================"
    exit 1
fi
