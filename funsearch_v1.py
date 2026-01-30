"""
FUNSEARCH EVOLUTION: V1 (MOMENTUM & DAMPING)
--------------------------------------------
DNA: Golden Ratio Weighted Momentum.
"""

import numpy as np

def evolved_optimizer_v1(initial_point, steps, noise_level):
    phi = 0.61803398875
    point = initial_point.copy()
    velocity = np.zeros_like(point)
    trajectory = [point.copy()]
    
    # Adaptive Params
    momentum = phi # 0.618
    learning_rate = 1.0 - phi # 0.381
    
    for i in range(steps):
        # Compute noisy gradient
        grad_x = 2 * point[0] + 20 * np.pi * np.sin(2 * np.pi * point[0]) + np.random.normal(0, noise_level)
        grad_y = 2 * point[1] + 20 * np.pi * np.sin(2 * np.pi * point[1]) + np.random.normal(0, noise_level)
        grad = np.array([grad_x, grad_y])
        
        # Golden Momentum: Integrate previous velocity using phi weight
        # phi determines how much of the "memory" we keep
        velocity = (momentum * velocity) - (learning_rate * grad)
        
        # Fractal Damping: Reduce the impact of noise as we converge
        # Decay factor tied to phi^2
        decay = phi ** (i / (steps * phi))
        
        point += velocity * decay
        trajectory.append(point.copy())
        
    return trajectory

if __name__ == "__main__":
    from funsearch_harness import Evaluator
    evaluator = Evaluator()
    print("--- RUNNING FUNSEARCH V1 (MOMENTUM) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v1)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
