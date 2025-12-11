# OpenMediaVault Tool

A Python CLI tool for interacting with OpenMediaVault (OMV), a Debian-based NAS solution.

## Features

- Clone Git repositories and deploy to OMV shares via CIFS mount or API verification.
- List shared folders and verify mounts using OMV's JSON-RPC API.
- Supports dry-run mode for testing.
- Library mode for integration with tools like autoForge.

## Installation

1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Install the tool: `pip install -e .`

## Configuration

Set environment variables for credentials:

- `OMV_HOST`: OMV server IP or hostname
- `OMV_PORT`: Port (default 80)
- `OMV_USER`: Username
- `OMV_PASS`: Password
- `OMV_SHARE`: Default share name (e.g., 'shared')

Or pass via CLI options.

## Usage

### CLI

```bash
omv-tool --host omv.local --user admin --password pass clone https://github.com/example/repo dest_folder --dry-run
omv-tool --host omv.local list-shares
omv-tool --host omv.local verify-mount
```

### Python API

```python
from omv_tool import OMVTool
tool = OMVTool(host='omv.local', user='admin', password='pass')
tool.deploy_repo('https://github.com/example/repo.git', 'dest_folder')
```

## Security Notes

- Use environment variables or keyring for credentials.
- Enable passwordless sudo for mount operations.
- API calls use session tokens; logout after use.

## Integration with autoForge

```python
from omv_tool import OMVTool
tool = OMVTool(host=os.getenv('OMV_HOST'), user=os.getenv('OMV_USER'), password=os.getenv('OMV_PASS'))
tool.deploy_repo(repo_url, dest_folder)
```

## Testing

Run tests: `pytest tests/`

For integration tests, set `OMV_TEST_HOST` and related env vars.

## RPC Integration

Refer to docs.openmediavault.org for OMV JSON-RPC API details (e.g., Session.login, ShareMgmt.enumShares).

## Troubleshooting

- Auth errors: Check credentials.
- Mount failures: Ensure sudo without password.
- Network issues: Verify host/port.
