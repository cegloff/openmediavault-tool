from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from omv_tool import OMVTool
from typing import Optional

class OMVCloneToolInput(BaseModel):
    repo_url: str = Field(description="URL of the Git repository to clone")
    dest_folder: str = Field(description="Destination folder in OMV share")
    branch: Optional[str] = Field(default='main', description="Branch to clone")

class OMVCloneTool(BaseTool):
    name = "omv_clone_upload"
    description = "Clones a Git repository and uploads it to an OpenMediaVault NAS share. Requires environment variables: OMV_HOST, OMV_USER, OMV_PASSWORD, OMV_SHARE_PATH."
    args_schema = OMVCloneToolInput

    def _run(self, repo_url: str, dest_folder: str, branch: Optional[str] = 'main') -> str:
        tool = OMVTool()
        if tool.clone_and_upload(repo_url, dest_folder, branch=branch):
            return f"Successfully cloned and uploaded {repo_url} to {dest_folder}."
        else:
            return f"Failed to clone and upload {repo_url}."

    async def _arun(self, repo_url: str, dest_folder: str, branch: Optional[str] = 'main') -> str:
        # Async version if needed
        return self._run(repo_url, dest_folder, branch)

# Example usage:
# from langchain.agents import load_tools
# tools = load_tools(['omv_clone_upload'])  # Assuming registered
# agent = ...