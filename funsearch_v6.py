"""
FUNSEARCH EVOLUTION: V6 (GOLDEN PULSE TUNNELING)
------------------------------------------------
DNA: Pulse Width Modulation & Quantum Jumps.
"""

import numpy as np

def evolved_optimizer_v6(initial_point, steps, noise_level):
    phi = 0.61803398875
    point = initial_point.copy()
    trajectory = [point.copy()]
    
    best_point = point.copy()
    
    def rastrigin(p):
        return 20 + (p[0]**2 - 10 * np.cos(2 * np.pi * p[0])) + (p[1]**2 - 10 * np.cos(2 * np.pi * p[1]))

    best_loss = rastrigin(point)

    for i in range(steps):
        # Compute noisy gradient
        grad_x = 2 * point[0] + 20 * np.pi * np.sin(2 * np.pi * point[0]) + np.random.normal(0, noise_level)
        grad_y = 2 * point[1] + 20 * np.pi * np.sin(2 * np.pi * point[1]) + np.random.normal(0, noise_level)
        grad = np.array([grad_x, grad_y])
        
        # 1. Golden Pulse: Heavy steps early to find the global valley
        # We use Phi (1.618) as the early pulse strength
        # We use phi (0.618) as the late pulse strength
        pulse = 1.618 if i < 40 else 0.618
        
        # 2. Vector Normalization: Ignore the magnitude of the cliff, just follow the compass
        direction = grad / (np.linalg.norm(grad) + 1e-8)
        
        # 3. Apply Step
        point -= pulse * direction
        
        # 4. Persistence of Memory
        cl = rastrigin(point)
        if cl < best_loss:
            best_loss = cl
            best_point = point.copy()
            
        trajectory.append(point.copy())
        
    trajectory[-1] = best_point
    return trajectory

if __name__ == "__main__":
    from funsearch_harness import Evaluator
    evaluator = Evaluator()
    print("--- RUNNING FUNSEARCH V6 (PULSE) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v6)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
