# OpenMediaVault Tool

## Purpose
A CLI and programmatic tool for cloning Git repositories and uploading them to an OpenMediaVault (OMV) NAS via CIFS mounting or RPC API.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your OMV details.

## Usage

### CLI
```bash
python -m omv_tool --repo-url https://github.com/user/repo --dest-folder myfolder --branch main
```

### Programmatic
```python
from omv_tool import OMVTool
tool = OMVTool()
tool.clone_and_upload('https://github.com/user/repo', 'myfolder')
```

## autoForge Integration
```python
from langchain.agents import load_tools
tools = load_tools(['omv_clone_upload'])
agent = initialize_agent(tools, llm)
agent.run("Clone https://github.com/example/repo to myfolder")
```

## Troubleshooting
- Mount fails: Check network, credentials, and sudo permissions.
- RPC fallback: Ensure OMV RPC is enabled.
- Private repos: Provide git_username and git_token.