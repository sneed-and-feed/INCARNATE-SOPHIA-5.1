
import unittest
import numpy as np

# Mocking the Quantum Latent Space Concept from Paper 1
# "Enhancing Quantum Diffusion Models for Complex Image Generation"

class QuantumLatentEncoder:
    def __init__(self, latent_dim=128):
        self.latent_dim = latent_dim
        # ANO (Adaptive Non-Local Observables) weights
        self.ano_weights = np.random.uniform(0.1, 1.0, latent_dim)

    def classic_to_quantum(self, image_vector):
        """
        Compresses classical data into a dense quantum latent vector.
        Simulating the Hilbert Space mapping.
        """
        # 1. Normalize (Wavefunction requirement)
        norm = np.linalg.norm(image_vector)
        if norm == 0: return image_vector
        wavefunction = image_vector / norm
        
        # 2. Apply ANO Compression (Non-local correlations)
        # In a real QPU, this would be an entanglement circuit.
        # Here we simulate it via weighted projection.
        quantum_latent = wavefunction * self.ano_weights
        
        # 3. Phase Rotation (The "Dreaming" step)
        # We rotate the vector in complex space to explore adjacent possibilities.
        theta = np.pi / 4 # 45 degree rotation into dreamtime
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
        ])
        
        # Simplified: Just rotate pairs (mockup)
        # We'll just return the magnitude for this test
        return quantum_latent

    def decode_dream(self, quantum_latent):
        """
        Collapses the quantum latent vector back to classical image.
        """
        # Inverse of ANO
        reconstructed = quantum_latent / self.ano_weights
        return reconstructed

class TestQuantumDreaming(unittest.TestCase):
    def test_compression_fidelity(self):
        print("\n[TEST] Testing Quantum Latent Compression (Paper 1)...")
        
        encoder = QuantumLatentEncoder(latent_dim=4)
        original_memory = np.array([1.0, 0.5, 0.2, 0.8])
        
        # Encode
        q_latent = encoder.classic_to_quantum(original_memory)
        print(f"Original: {original_memory}")
        print(f"Quantum Latent (ANO): {q_latent}")
        
        # Decode
        dream = encoder.decode_dream(q_latent)
        print(f"Reconstructed Dream: {dream}")
        
        # Norm check (Direction should be preserved)
        cos_sim = np.dot(original_memory, dream) / (np.linalg.norm(original_memory) * np.linalg.norm(dream))
        print(f"Fidelity (Cosine Sim): {cos_sim:.4f}")
        
        self.assertGreater(cos_sim, 0.99, "Quantum Decompression lost too much fidelity!")

if __name__ == '__main__':
    unittest.main()
