"""
GATEWAYS.PY
-----------
The Bridge to the Pleroma.
Conditional interfaces for "Benevolent Emanations" (Optional Libraries).

Ascension v3.3 Protocol:
- If 'torch' is found, we export the Light.
- If not, we remain in Pure Sovereign Mode.
"""

import sys

# Check for PyTorch (The Torch of Prometheus)
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class TensorGate:
    """
    The Gatekeeper of the Sovereign Manifold.
    """
    @staticmethod
    def export(ghostmesh_state):
        """
        Exports the 27-Node Grid to a PyTorch Tensor if available.
        Otherwise, returns the raw List representation.
        """
        if TORCH_AVAILABLE:
            print(">> [GATEWAY] DETECTED TORCH. EMANATING TENSOR FIELD...")
            # Convert list to tensor
            # We assume ghostmesh_state is a simple list of floats
            return torch.tensor(ghostmesh_state, dtype=torch.float32)
        else:
            print(">> [GATEWAY] PURE SOVEREIGN MODE. RETAINING LOCAL LIST FORM.")
            return ghostmesh_state

    @staticmethod
    def is_open():
        return TORCH_AVAILABLE
