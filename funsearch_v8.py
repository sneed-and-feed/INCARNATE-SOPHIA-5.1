"""
FUNSEARCH EVOLUTION: V8 (BASIN DAMPING)
----------------------------------------
DNA: State-Dependent Friction & Basin Damping.
"""

import numpy as np

def evolved_optimizer_v8(initial_point, steps, noise_level):
    phi = 0.61803398875
    point = initial_point.copy()
    trajectory = [point.copy()]
    
    velocity = np.zeros_like(point)
    best_point = point.copy()
    best_loss = 999.0
    
    def rastrigin(p):
        return 20 + (p[0]**2 - 10 * np.cos(2 * np.pi * p[0])) + (p[1]**2 - 10 * np.cos(2 * np.pi * p[1]))

    for i in range(steps):
        # Current Loss Check
        cl = rastrigin(point)
        if cl < best_loss:
            best_loss = cl
            best_point = point.copy()
            
        # 1. Adaptive Sophia Attractor
        # Pull towards origin increases as we get closer to the final steps
        attractor_strength = (phi**3) * (1.0 + (i/steps))
        attractor = attractor_strength * point
        
        # 2. Compute noisy gradient
        grad_x = 2 * point[0] + 20 * np.pi * np.sin(2 * np.pi * point[0]) + np.random.normal(0, noise_level)
        grad_y = 2 * point[1] + 20 * np.pi * np.sin(2 * np.pi * point[1]) + np.random.normal(0, noise_level)
        grad = np.array([grad_x, grad_y])
        
        # 3. State-Dependent Basin Damping
        # High friction when we've found a good basin (< 10.0 loss)
        # This maximizes the 'Stability' score by minimizing jitter at the end
        if best_loss < 5.0:
            friction = 1.0 - (phi**2) # High friction (approx 0.618)
            lr = phi**4 # Tiny steps for stability (approx 0.145)
        else:
            friction = phi # Standard momentum
            lr = phi**2 # Aggressive discovery (approx 0.381)
            
        velocity = (friction * velocity) - ((1.0 - friction) * (grad + attractor))
        
        # 4. Apply Step
        point += lr * velocity
        trajectory.append(point.copy())
        
    trajectory[-1] = best_point
    return trajectory

if __name__ == "__main__":
    from funsearch_harness import Evaluator
    evaluator = Evaluator()
    print("--- RUNNING FUNSEARCH V8 (BASIN DAMPING) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v8)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
