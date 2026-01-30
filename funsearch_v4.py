"""
FUNSEARCH EVOLUTION: V4 (MOMENTUM & DECAY)
------------------------------------------
DNA: Exponential Phi Decay & Velocity Normalization.
"""

import numpy as np

def evolved_optimizer_v4(initial_point, steps, noise_level):
    phi = 0.61803398875
    point = initial_point.copy()
    trajectory = [point.copy()]
    
    velocity = np.zeros_like(point)
    best_point = point.copy()
    
    def rastrigin(p):
        return 20 + (p[0]**2 - 10 * np.cos(2 * np.pi * p[0])) + (p[1]**2 - 10 * np.cos(2 * np.pi * p[1]))

    best_loss = rastrigin(point)

    for i in range(steps):
        # Compute noisy gradient
        grad_x = 2 * point[0] + 20 * np.pi * np.sin(2 * np.pi * point[0]) + np.random.normal(0, noise_level)
        grad_y = 2 * point[1] + 20 * np.pi * np.sin(2 * np.pi * point[1]) + np.random.normal(0, noise_level)
        grad = np.array([grad_x, grad_y])
        
        # 1. Golden Momentum
        # phi (0.618) as the smoothing factor
        velocity = (phi * velocity) + ((1.0 - phi) * grad)
        
        # 2. Velocity Normalization
        # Prevents exploding gradients while maintaining direction
        v_norm = np.linalg.norm(velocity)
        unit_velocity = velocity / (v_norm + 1e-8)
        
        # 3. Exponential Phi Decay
        # Start aggressively (0.8) and scale down to phi (0.618) over time
        lr = 0.8 * (phi ** (i / steps))
        
        # Apply step
        point -= lr * unit_velocity
        
        # 4. Persistence
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
    print("--- RUNNING FUNSEARCH V4 (DECAY) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v4)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
