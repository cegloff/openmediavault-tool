import pytest
import tempfile
import os
import shutil
from unittest.mock import patch, MagicMock
from omv_tool import OMVTool

class TestOMVTool:
    @patch('omv_tool.subprocess.run')
    @patch('omv_tool.os.path.ismount')
    def test_mount_share_success(self, mock_ismount, mock_run):
        mock_ismount.return_value = False
        mock_run.return_value = MagicMock(returncode=0)
        tool = OMVTool(host='test', user='user', password='pass')
        assert tool.mount_share() == True
        mock_run.assert_called()

    @patch('omv_tool.subprocess.run')
    @patch('omv_tool.os.path.ismount')
    def test_mount_share_fail_fallback(self, mock_ismount, mock_run):
        mock_ismount.return_value = False
        mock_run.return_value = MagicMock(returncode=1)
        tool = OMVTool(host='test', user='user', password='pass')
        with patch.object(tool, 'upload_via_rpc_prepare', return_value=False):
            assert tool.mount_share() == False

    @patch('omv_tool.Repo.clone_from')
    @patch('omv_tool.shutil.copytree')
    @patch('omv_tool.os.path.exists')
    def test_clone_and_upload(self, mock_exists, mock_copytree, mock_clone):
        mock_exists.return_value = False
        tool = OMVTool(dry_run=False)
        tool.mounted = True
        assert tool.clone_and_upload('https://github.com/test/repo', 'dest') == True
        mock_clone.assert_called()
        mock_copytree.assert_called()

    @patch('omv_tool.Repo.clone_from')
    def test_clone_and_upload_invalid_url(self, mock_clone):
        tool = OMVTool()
        with pytest.raises(ValueError):
            tool.clone_and_upload('invalid-url', 'dest')

    @patch('omv_tool.Repo.clone_from')
    def test_clone_and_upload_dry_run(self, mock_clone):
        tool = OMVTool(dry_run=True)
        assert tool.clone_and_upload('https://github.com/test/repo', 'dest') == True
        mock_clone.assert_not_called()

    @patch('omv_tool.requests.post')
    def test_get_session_token(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200, json=MagicMock(return_value={'result': 'token'}))
        tool = OMVTool(host='test', user='user', password='pass')
        assert tool.get_session_token() == 'token'

# Integration test placeholder
# def test_integration():
#     # Would require actual setup, mocked here
#     pass