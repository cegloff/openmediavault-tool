#!/usr/bin/env python3

import os
import subprocess
import shutil
import argparse
from pathlib import Path

# Configuration
OMV_HOST = 'store-g9.egloff.tech'
OMV_SHARE = '//{}/shared'  # Assuming a shared folder named 'shared'; adjust as needed
OMV_USER = 'your_username'  # Replace with your OMV username
OMV_PASS = 'your_password'  # Replace with your OMV password (consider using env vars for security)
LOCAL_MOUNT_POINT = '/mnt/omv'

# Ensure mount point exists
def ensure_mount_point():
    if not os.path.exists(LOCAL_MOUNT_POINT):
        os.makedirs(LOCAL_MOUNT_POINT)

# Mount the OMV share
def mount_omv():
    ensure_mount_point()
    cmd = ['sudo', 'mount', '-t', 'cifs', OMV_SHARE.format(OMV_HOST), LOCAL_MOUNT_POINT, '-o', f'username={OMV_USER},password={OMV_PASS}']
    try:
        subprocess.run(cmd, check=True)
        print(f"Mounted OMV share at {LOCAL_MOUNT_POINT}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to mount OMV share: {e}")
        return False
    return True

# Unmount the OMV share
def unmount_omv():
    cmd = ['sudo', 'umount', LOCAL_MOUNT_POINT]
    try:
        subprocess.run(cmd, check=True)
        print("Unmounted OMV share")
    except subprocess.CalledProcessError as e:
        print(f"Failed to unmount: {e}")

# Clone a git repository to a temporary location and copy to OMV
def clone_and_save(repo_url, dest_folder):
    temp_dir = '/tmp/git_clone'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Clone the repo
    try:
        subprocess.run(['git', 'clone', repo_url, temp_dir], check=True)
        print(f"Cloned {repo_url} to {temp_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repo: {e}")
        return
    
    # Mount OMV if not already mounted
    if not mount_omv():
        return
    
    # Copy to OMV
    omv_dest = Path(LOCAL_MOUNT_POINT) / dest_folder
    if not omv_dest.exists():
        omv_dest.mkdir(parents=True)
    
    try:
        shutil.copytree(temp_dir, omv_dest, dirs_exist_ok=True)
        print(f"Copied files to {omv_dest}")
    except Exception as e:
        print(f"Failed to copy files: {e}")
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
        unmount_omv()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clone a git repo and save to OpenMediaVault')
    parser.add_argument('repo_url', help='URL of the git repository to clone')
    parser.add_argument('dest_folder', help='Destination folder on OMV share')
    args = parser.parse_args()
    
    clone_and_save(args.repo_url, args.dest_folder)