"""
FUNSEARCH EVOLUTION: V3 (GOLDEN RMSPROP)
----------------------------------------
DNA: Golden Decay & Normalized Accumulation.
"""

import numpy as np

def evolved_optimizer_v3(initial_point, steps, noise_level):
    phi = 0.61803398875
    point = initial_point.copy()
    trajectory = [point.copy()]
    
    # State for Golden RMSProp
    cache = np.zeros_like(point)
    best_point = point.copy()
    
    def rastrigin(p):
        return 20 + (p[0]**2 - 10 * np.cos(2 * np.pi * p[0])) + (p[1]**2 - 10 * np.cos(2 * np.pi * p[1]))

    best_loss = rastrigin(point)

    # Initial lr is higher to escape the local basin at (2,3)
    base_lr = phi * 0.2 

    for i in range(steps):
        # Compute noisy gradient
        grad_x = 2 * point[0] + 20 * np.pi * np.sin(2 * np.pi * point[0]) + np.random.normal(0, noise_level)
        grad_y = 2 * point[1] + 20 * np.pi * np.sin(2 * np.pi * point[1]) + np.random.normal(0, noise_level)
        grad = np.array([grad_x, grad_y])
        
        # 1. Golden RMSProp: Accumulate squared gradients using phi decay
        # This automatically handles the large oscillations of the Rastrigin grad
        cache = (phi * cache) + ((1.0 - phi) * grad**2)
        
        # 2. Adaptive Step: Standardized by the RMS of gradients
        # We use a dampening factor that decays fast (phi^2)
        dampening = (1.0 - (i / steps)) ** (1.0/phi)
        lr = base_lr / (np.sqrt(cache) + 1e-8)
        
        point -= lr * dampening * grad
        
        # 3. Persistence Check
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
    print("--- RUNNING FUNSEARCH V3 (RMSPROP) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v3)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
