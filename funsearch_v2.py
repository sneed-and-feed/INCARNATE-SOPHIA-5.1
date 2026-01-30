"""
FUNSEARCH EVOLUTION: V2 (ADAPTIVE STEP & JITTER)
------------------------------------------------
DNA: Dynamic Decay & Prime Jitter.
"""

import numpy as np

def evolved_optimizer_v2(initial_point, steps, noise_level):
    phi = 0.61803398875
    point = initial_point.copy()
    trajectory = [point.copy()]
    
    # Track the best point seen to avoid escaping global minima
    best_point = point.copy()
    
    def rastrigin(p):
        return 20 + (p[0]**2 - 10 * np.cos(2 * np.pi * p[0])) + (p[1]**2 - 10 * np.cos(2 * np.pi * p[1]))

    best_loss = rastrigin(point)

    for i in range(steps):
        # Compute noisy gradient
        grad_x = 2 * point[0] + 20 * np.pi * np.sin(2 * np.pi * point[0]) + np.random.normal(0, noise_level)
        grad_y = 2 * point[1] + 20 * np.pi * np.sin(2 * np.pi * point[1]) + np.random.normal(0, noise_level)
        grad = np.array([grad_x, grad_y])
        
        # 1. Golden Step Normalization
        # Use phi^2 as the base sensitivity
        norm = np.linalg.norm(grad)
        lr = (phi**2) / (np.sqrt(norm) + 1.0)
        
        # 2. Temporal Damping
        # Decay lr linearly but modulate with phi to preserve exploration early on
        dampening = (1.0 - (i / steps))**phi
        
        # Update point
        point -= lr * dampening * grad
        
        # 3. Golden Jitter (Quantum Tunneling Emulation)
        # Every 7 steps (Prime), try a jump if we are stuck
        if i % 7 == 0 and rastrigin(point) > 1.0:
            point += np.random.normal(0, noise_level * phi, size=2)
            
        # 4. Persistence of Memory
        current_loss = rastrigin(point)
        if current_loss < best_loss:
            best_loss = current_loss
            best_point = point.copy()
        
        trajectory.append(point.copy())
        
    # Snap to the best historical point at the end
    trajectory[-1] = best_point
    return trajectory

if __name__ == "__main__":
    from funsearch_harness import Evaluator
    evaluator = Evaluator()
    print("--- RUNNING FUNSEARCH V2 (ADAPTIVE) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v2)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
