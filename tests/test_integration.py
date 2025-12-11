import pytest
import os
from omv_tool import OMVTool

@pytest.mark.integration
def test_real_deploy():
    if not os.getenv('OMV_TEST_HOST'):
        pytest.skip('OMV_TEST_HOST not set')
    tool = OMVTool(
        host=os.getenv('OMV_TEST_HOST'),
        user=os.getenv('OMV_USER'),
        password=os.getenv('OMV_PASS'),
        share=os.getenv('OMV_SHARE', 'shared')
    )
    tool.deploy_repo('https://github.com/example/test-repo.git', 'test_folder', dry_run=True)
    shares = tool.list_shares()
    assert len(shares) > 0
