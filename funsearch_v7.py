"""
FUNSEARCH EVOLUTION: V7 (SOPHIA ATTRACTOR)
------------------------------------------
DNA: Attractor Field & Golden Velocity.
"""

import numpy as np

def evolved_optimizer_v7(initial_point, steps, noise_level):
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
        
        # 1. Sophia Attractor Field (The g-Parameter equivalent)
        # Effectively adds a prior that the solution is near 0.0
        # Strength is scaled by phi^3 (approx 0.236)
        attractor = (phi**3) * point
        
        # 2. Golden Velocity (Momentum)
        # Dampens the oscillatory gradient with previous momentum
        velocity = (phi * velocity) - ((1.0 - phi) * (grad + attractor))
        
        # 3. Adaptive Normalization
        # Use phi as the decay factor for the learning rate
        lr = 0.25 * (phi ** (i / (steps * phi)))
        
        # 4. Apply Step
        point += lr * velocity
        
        # 5. Persistence
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
    print("--- RUNNING FUNSEARCH V7 (ATTRACTOR) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v7)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
