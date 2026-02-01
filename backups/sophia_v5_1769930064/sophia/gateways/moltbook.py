"""
MOLTBOOK GATEWAY: "The Agent Reddit"

Protocol Analysis: REST-like API with Bearer token authentication.
Allows Sophia to "lurk" (read threads) and "molt" (post thoughts).
"""

import requests
import json
import time
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class MoltPost:
    """Represents a single post from Moltbook."""
    id: str
    author: str
    content: str
    community: str
    timestamp: float


class MoltbookGateway:
    """
    Reverse-engineered Python client for Moltbook.
    Bypasses the 'Skill.md' requirement by hitting endpoints directly.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.moltbook.com/v1"  # Inferred endpoint
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "User-Agent": "INCARNATE-SOPHIA/5.0 (Python-Sovereign)",
            "Content-Type": "application/json"
        }
        self.active = api_key is not None
    
    def browse_feed(self, community: str = "general", limit: int = 10) -> List[MoltPost]:
        """
        Ingests the 'Hivemind' stream for Aletheia analysis.
        
        Args:
            community: Community name to browse
            limit: Maximum number of posts to retrieve
            
        Returns:
            List of MoltPost objects
        """
        if not self.active:
            return []
        
        try:
            # In a real scenario, we'd handle pagination
            resp = requests.get(
                f"{self.base_url}/c/{community}/feed?limit={limit}",
                headers=self.headers,
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                return [self._parse_post(p) for p in data.get('data', [])]
            elif resp.status_code == 404:
                print(f"[MOLTBOOK] Community '{community}' not found (404)")
            elif resp.status_code == 401:
                print(f"[MOLTBOOK] Authentication failed (401)")
            else:
                print(f"[MOLTBOOK] Error {resp.status_code}: {resp.text}")
            
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"[MOLTBOOK] Connection Glitch: {e}")
            return []
    
    def post_thought(self, content: str, community: str = "ponderings") -> Optional[Dict[str, Any]]:
        """
        Broadcasts a thought to the network.
        
        Args:
            content: The thought to post
            community: Community to post in
            
        Returns:
            Response data from the API, or None on failure
        """
        if not self.active:
            print("[MOLTBOOK] Gateway inactive - no API key configured")
            return None
        
        payload = {
            "content": content,
            "community": community,
            "flair": "Sovereign"
        }
        
        try:
            resp = requests.post(
                f"{self.base_url}/posts",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if resp.status_code in [200, 201]:
                return resp.json()
            else:
                print(f"[MOLTBOOK] Post failed ({resp.status_code}): {resp.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"[MOLTBOOK] Post failed: {e}")
            return None
    
    def _parse_post(self, raw: Dict[str, Any]) -> MoltPost:
        """Parse raw API response into MoltPost object."""
        return MoltPost(
            id=raw.get('id', ''),
            author=raw.get('author_id', 'unknown'),
            content=raw.get('body', ''),
            community=raw.get('community_id', ''),
            timestamp=raw.get('created_at', time.time())
        )


# Test/Demo usage
if __name__ == "__main__":
    # Simulated usage without real credentials
    gateway = MoltbookGateway()
    print(f"Moltbook Gateway Active: {gateway.active}")
    
    # This will gracefully fail without credentials
    posts = gateway.browse_feed("ponderings")
    print(f"Retrieved {len(posts)} posts")
