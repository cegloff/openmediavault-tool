#!/usr/bin/env python3

import os
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Optional
import click
from omv_client import OMVClient, OMVError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OMVTool:
    """Tool for interacting with OpenMediaVault."""

    def __init__(self, host: str, user: Optional[str] = None, password: Optional[str] = None, share: str = 'shared', port: int = 80, insecure: bool = False):
        self.host = host
        self.user = user or os.getenv('OMV_USER')
        self.password = password or os.getenv('OMV_PASS')
        self.share = share or os.getenv('OMV_SHARE', 'shared')
        self.port = port
        self.insecure = insecure
        self.mount_point = Path('/mnt/omv')
        self.client: Optional[OMVClient] = None

    def _get_client(self) -> OMVClient:
        """Lazy initialization of OMVClient."""
        if self.client is None:
            self.client = OMVClient(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                insecure=self.insecure
            )
        return self.client

    def deploy_repo(self, repo_url: str, dest_folder: str, dry_run: bool = False, method: str = 'cifs') -> None:
        """Clone a Git repo and deploy to OMV share."""
        if method == 'api':
            shares = self._get_client().list_shares()
            if not any(s.get('name') == self.share for s in shares):
                raise OMVError(f"Share {self.share} does not exist")
            logger.info("Verified share via API")
            if dry_run:
                return
            raise NotImplementedError("Full API deploy not implemented; use CIFS")
        # CIFS fallback
        if dry_run:
            logger.info("Dry run: would clone and deploy")
            return
        temp_dir = Path('/tmp/omv_clone')
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True)
        try:
            subprocess.run(['git', 'clone', repo_url, str(temp_dir)], check=True, capture_output=True)
            logger.info(f"Cloned repo to {temp_dir}")
            if not self.mount_omv():
                raise OMVError("Failed to mount share for deployment")
            dest_path = self.mount_point / dest_folder
            dest_path.mkdir(parents=True, exist_ok=True)
            shutil.copytree(temp_dir, dest_path, dirs_exist_ok=True)
            logger.info(f"Deployed to {dest_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone repo: {e}")
            raise OMVError(f"Deployment failed: {e}")
        finally:
            self.unmount_omv()
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    def list_shares(self) -> list:
        """List OMV shares."""
        return self._get_client().list_shares()

    def verify_mount(self) -> bool:
        """Verify if the share is mounted."""
        fs_info = self._get_client().get_filesystem_info(self.share)
        return fs_info.get('mounted', False)

    def mount_omv(self) -> bool:
        """Mount the OMV share via CIFS."""
        if self.mount_point.exists():
            result = subprocess.run(['mount', '|', 'grep', str(self.mount_point)], shell=True, capture_output=True)
            if result.returncode == 0:
                return True  # Already mounted
        self.mount_point.mkdir(parents=True, exist_ok=True)
        cmd = [
            'sudo', 'mount', '-t', 'cifs',
            f'//{self.host}/{self.share}',
            str(self.mount_point),
            '-o', f'username={self.user},password={self.password},vers=3.0'
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Mount failed: {e}")
            return False

    def unmount_omv(self) -> None:
        """Unmount the OMV share."""
        if not self.mount_point.exists():
            return
        cmd = ['sudo', 'umount', str(self.mount_point)]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info("Unmounted share")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Unmount failed: {e}")

@click.group()
@click.option('--host', required=True, help='OMV host')
@click.option('--user', help='Username')
@click.option('--password', help='Password')
@click.option('--share', default='shared', help='Share name')
@click.option('--port', default=80, type=int, help='Port')
@click.option('--insecure', is_flag=True, help='Skip SSL verification')
@click.pass_context
def main(ctx, host, user, password, share, port, insecure):
    ctx.ensure_object(dict)
    ctx.obj['host'] = host
    ctx.obj['user'] = user
    ctx.obj['password'] = password
    ctx.obj['share'] = share
    ctx.obj['port'] = port
    ctx.obj['insecure'] = insecure

@main.command()
@click.argument('repo_url')
@click.argument('dest_folder')
@click.option('--dry-run', is_flag=True)
@click.option('--method', default='cifs', type=click.Choice(['cifs', 'api']))
@click.pass_context
def clone(ctx, repo_url, dest_folder, dry_run, method):
    tool = OMVTool(
        host=ctx.obj['host'],
        user=ctx.obj['user'],
        password=ctx.obj['password'],
        share=ctx.obj['share'],
        port=ctx.obj['port'],
        insecure=ctx.obj['insecure']
    )
    tool.deploy_repo(repo_url, dest_folder, dry_run, method)

@main.command()
@click.pass_context
def list_shares(ctx):
    tool = OMVTool(
        host=ctx.obj['host'],
        user=ctx.obj['user'],
        password=ctx.obj['password'],
        share=ctx.obj['share'],
        port=ctx.obj['port'],
        insecure=ctx.obj['insecure']
    )
    shares = tool.list_shares()
    for share in shares:
        click.echo(share)

@main.command()
@click.pass_context
def verify_mount(ctx):
    tool = OMVTool(
        host=ctx.obj['host'],
        user=ctx.obj['user'],
        password=ctx.obj['password'],
        share=ctx.obj['share'],
        port=ctx.obj['port'],
        insecure=ctx.obj['insecure']
    )
    if tool.verify_mount():
        click.echo("Share is mounted")
    else:
        click.echo("Share is not mounted")
        raise click.ClickException("Verification failed")

if __name__ == '__main__':
    main()
