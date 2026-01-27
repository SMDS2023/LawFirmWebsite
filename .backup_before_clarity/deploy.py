#!/usr/bin/env python3
"""
Bluehost FTP Deployment Script
Simple Python script to deploy website to Bluehost via FTP
Requires Python 3.x (built into most systems)
"""

import json
import os
import sys
from ftplib import FTP
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50 + "\n")

def load_config():
    """Load FTP configuration from deploy-config.json"""
    config_file = "deploy-config.json"

    if not os.path.exists(config_file):
        print("ERROR: deploy-config.json not found!")
        print("\nPlease create deploy-config.json based on deploy-config-template.json")
        print("Steps:")
        print("  1. Copy deploy-config-template.json to deploy-config.json")
        print("  2. Fill in your Bluehost FTP credentials")
        print("  3. Run this script again")
        sys.exit(1)

    with open(config_file, 'r') as f:
        return json.load(f)

def upload_file(ftp, local_path, remote_path):
    """Upload a single file to FTP server"""
    try:
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)
        return True
    except Exception as e:
        print(f"  ERROR uploading {local_path}: {e}")
        return False

def ensure_remote_dir(ftp, remote_dir):
    """Create remote directory if it doesn't exist"""
    try:
        ftp.cwd(remote_dir)
    except:
        # Directory doesn't exist, create it
        try:
            ftp.mkd(remote_dir)
            ftp.cwd(remote_dir)
        except Exception as e:
            print(f"  Warning: Could not create directory {remote_dir}: {e}")

def deploy_website(config):
    """Main deployment function"""
    print_header("Bluehost Deployment Script")

    print("Configuration loaded:")
    print(f"  Host: {config['host']}")
    print(f"  Username: {config['username']}")
    print(f"  Remote Path: {config['remote_path']}")
    print(f"  Port: {config.get('port', 21)}")

    # Files and folders to exclude
    exclude = {'.git', 'deploy-config.json', 'deploy.ps1', 'deploy.sh',
               'deploy.py', 'deploy.log', '.gitignore', 'README.md',
               'deploy-config-template.json', '__pycache__'}

    try:
        print("\nConnecting to FTP server...")
        ftp = FTP()
        ftp.connect(config['host'], config.get('port', 21))
        ftp.login(config['username'], config['password'])

        print(f"Connected successfully!")
        print(f"Changing to remote directory: {config['remote_path']}")

        # Change to remote directory
        ftp.cwd(config['remote_path'])

        print("\nStarting file upload...\n")

        uploaded_count = 0
        error_count = 0

        # Upload all HTML and CSS files in root
        for file in Path('.').glob('*.html'):
            if file.name not in exclude:
                print(f"  Uploading: {file.name}")
                if upload_file(ftp, file, file.name):
                    uploaded_count += 1
                else:
                    error_count += 1

        for file in Path('.').glob('*.css'):
            if file.name not in exclude:
                print(f"  Uploading: {file.name}")
                if upload_file(ftp, file, file.name):
                    uploaded_count += 1
                else:
                    error_count += 1

        # Upload subdirectories
        subdirs = ['assets', 'blog', 'practice-areas']

        for subdir in subdirs:
            if os.path.isdir(subdir):
                print(f"\n  Uploading {subdir}/ directory...")

                # Ensure remote directory exists
                ftp.cwd(config['remote_path'])
                ensure_remote_dir(ftp, subdir)

                # Upload all files in subdirectory
                for file in Path(subdir).rglob('*'):
                    if file.is_file() and file.name not in exclude:
                        relative_path = str(file.relative_to(subdir))

                        # Create subdirectories if needed
                        if '/' in relative_path or '\\' in relative_path:
                            parent_dir = str(Path(relative_path).parent)
                            ensure_remote_dir(ftp, f"{subdir}/{parent_dir}")

                        remote_file_path = relative_path.replace('\\', '/')
                        print(f"    Uploading: {subdir}/{remote_file_path}")

                        if upload_file(ftp, file, remote_file_path):
                            uploaded_count += 1
                        else:
                            error_count += 1

        ftp.quit()

        print_header("Deployment Summary")
        print(f"Files uploaded: {uploaded_count}")
        if error_count > 0:
            print(f"Errors: {error_count}")
            print("\nDeployment completed with errors!")
            sys.exit(1)
        else:
            print("\nDeployment completed successfully!")
            sys.exit(0)

    except Exception as e:
        print(f"\nERROR: Deployment failed!")
        print(f"Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    config = load_config()
    deploy_website(config)
