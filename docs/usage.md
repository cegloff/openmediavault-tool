# Usage Documentation

## OMVTool API

### Methods
- `mount_share(share_path=None)`: Mounts the OMV share. Returns True on success.
- `clone_and_upload(repo_url, dest_folder, branch='main', depth=None, overwrite=False, git_username=None, git_token=None)`: Clones and uploads. Validates URL, supports private repos.
- `unmount_share()`: Unmounts the share.

## Environment Variables
- `OMV_HOST`: IP or hostname of OMV.
- `OMV_USER`: Username.
- `OMV_PASSWORD`: Password (use keyring for security).
- `OMV_SHARE_PATH`: Share path.
- `LOCAL_MOUNT_POINT`: Local mount point.

## Examples

### CIFS Mode
```python
tool = OMVTool()
tool.mount_share()
tool.clone_and_upload('https://github.com/user/repo', 'dest')
tool.unmount_share()
```

### RPC Mode
Automatically falls back if mount fails.

## Security
Use `keyring.set_password('omv', 'host', 'password')` instead of env vars.

## autoForge Registration
Tool schema: {"name": "omv_clone_upload", "description": "...", "parameters": {"repo_url": {"type": "string"}, "dest_folder": {"type": "string"}, "branch": {"type": "string"}}