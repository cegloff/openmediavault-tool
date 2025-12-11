# omv_client.py

import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class OMVError(Exception):
    """Custom exception for OMV-related errors."""
    pass

class OMVClient:
    """JSON-RPC client for OpenMediaVault API."""

    def __init__(self, host: str, port: int = 80, username: Optional[str] = None, password: Optional[str] = None, insecure: bool = False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.verify = not insecure  # Skip SSL verification if insecure
        self.session.timeout = 30
        self.auth_token: Optional[str] = None
        self.logged_in = False

    def login(self) -> None:
        """Authenticate and obtain session token."""
        if self.logged_in:
            return
        params = {
            'username': self.username,
            'password': self.password,
        }
        response = self.rpc_call_raw('Session', 'login', params)
        if 'error' in response:
            raise OMVError(f"Login failed: {response['error']['message']}")
        self.auth_token = response.get('result')
        self.logged_in = True
        logger.info("Logged in to OMV")

    def logout(self) -> None:
        """End the session."""
        if not self.logged_in:
            return
        self.rpc_call_raw('Session', 'logout')
        self.auth_token = None
        self.logged_in = False
        logger.info("Logged out from OMV")

    def rpc_call_raw(self, service: str, method: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Perform a raw JSON-RPC call."""
        url = f"http://{self.host}:{self.port}/rpc.php"
        payload = {
            'jsonrpc': '2.0',
            'method': f'{service}.{method}',
            'params': params,
            'id': 1
        }
        headers = {}
        if self.auth_token:
            headers['X-Authorization'] = f'Bearer {self.auth_token}'
        try:
            resp = self.session.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            raise OMVError(f"HTTP error: {e}")
        if 'error' in data:
            raise OMVError(f"RPC error: {data['error']['message']}")
        return data

    def rpc_call(self, service: str, method: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Perform an authenticated JSON-RPC call, ensuring login."""
        if not self.logged_in:
            self.login()
        return self.rpc_call_raw(service, method, params)

    def list_shares(self) -> list:
        """List shared folders."""
        response = self.rpc_call('ShareMgmt', 'enumShares')
        return response.get('result', [])

    def get_filesystem_info(self, share_name: str) -> Dict[str, Any]:
        """Get filesystem information for a share."""
        response = self.rpc_call('FileSystemMgmt', 'enumerateMountedFilesystems')
        for fs in response.get('result', []):
            if fs.get('label') == share_name:
                return fs
        raise OMVError(f"Filesystem for share '{share_name}' not found")
