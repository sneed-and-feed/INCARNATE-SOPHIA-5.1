import hashlib
import time
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Engram:
    """
    The Atomic Unit of Truth. Immutable. Citable.
    """
    id: str             # Deterministic Hash (SHA-256)
    scope: str          # Where this belongs (e.g., "realm:taiga/layer:meme")
    content: str        # The raw text/data
    source: str         # Provenance (e.g., "duckduckgo", "user_input", "inference")
    timestamp: float    # When it was forged

    @staticmethod
    def forge(scope: str, content: str, source: str):
        # Create a content hash ID
        payload = f"{scope}:{content}:{source}".encode('utf-8')
        id_hash = hashlib.sha256(payload).hexdigest()
        return Engram(
            id=id_hash,
            scope=scope,
            content=content,
            source=source,
            timestamp=time.time()
        )

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
