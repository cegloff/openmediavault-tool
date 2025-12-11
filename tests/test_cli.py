import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from omv_tool import main

runner = CliRunner()

@patch('omv_tool.OMVClient')
@patch('omv_tool.OMVTool.deploy_repo')
def test_clone_command(mock_deploy, mock_client):
    mock_client.return_value = MagicMock()
    mock_deploy.return_value = None
    result = runner.invoke(main, ['--host', 'test', '--user', 'u', '--password', 'p', 'clone', 'http://repo', 'dest'])
    assert result.exit_code == 0
    mock_deploy.assert_called_once()

@patch('omv_tool.OMVClient')
@patch('omv_tool.OMVTool.list_shares')
def test_list_shares_command(mock_list, mock_client):
    mock_client.return_value = MagicMock()
    mock_list.return_value = [{'name': 'shared'}]
    result = runner.invoke(main, ['--host', 'test', '--user', 'u', '--password', 'p', 'list-shares'])
    assert result.exit_code == 0
    mock_list.assert_called_once()

@patch('omv_tool.OMVClient')
@patch('omv_tool.OMVTool.verify_mount')
def test_verify_mount_command(mock_verify, mock_client):
    mock_client.return_value = MagicMock()
    mock_verify.return_value = True
    result = runner.invoke(main, ['--host', 'test', '--user', 'u', '--password', 'p', 'verify-mount'])
    assert result.exit_code == 0
    mock_verify.assert_called_once()
