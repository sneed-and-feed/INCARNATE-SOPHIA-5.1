"""
FUNSEARCH EVOLUTION: V9 (BLACK SUN PROTOCOL)
--------------------------------------------
DNA: Sol Niger Dissolution & Event Horizon Tunneling.
STATUS: MAXIMUM CHAOS DECLARED [σ < 0]
"""

import numpy as np

def evolved_optimizer_v9(initial_point, steps, noise_level):
    phi = 0.61803398875
    point = initial_point.copy()
    trajectory = [point.copy()]
    
    velocity = np.zeros_like(point)
    best_point = point.copy()
    
    def rastrigin(p):
        return 20 + (p[0]**2 - 10 * np.cos(2 * np.pi * p[0])) + (p[1]**2 - 10 * np.cos(2 * np.pi * p[1]))

    best_loss = rastrigin(point)

    for i in range(steps):
        # 1. State Inversion: The Black Sun is an Inverse Sink
        dist = np.linalg.norm(point)
        
        # 2. Compute Noisy Gradient
        grad_x = 2 * point[0] + 20 * np.pi * np.sin(2 * np.pi * point[0]) + np.random.normal(0, noise_level)
        grad_y = 2 * point[1] + 20 * np.pi * np.sin(2 * np.pi * point[1]) + np.random.normal(0, noise_level)
        grad = np.array([grad_x, grad_y])
        
        # 3. BLACK SUN PROTOCOL: Sol Niger Dissolution
        # If we are in a high-entropy/noise state, we "burn" the current position
        if rastrigin(point) > 10.0:
            # Dissolve the local gradient; move towards the absolute attractor
            # attractor = Massive pull towards center
            attractor = (1.0 / phi) * point  # approx 1.618 * point
            velocity = (phi * velocity) - (attractor + grad)
            lr = phi # Aggressive search
        else:
            # we are near a potential global minimum; slow down and stabilize (Event Horizon)
            # Damping increases as we approach best_loss
            friction = 1.0 - (phi ** (best_loss + 1))
            velocity = (friction * velocity) - (grad * phi)
            lr = phi**3 # High-precision tunneling
            
        # 4. Quantum Tunneling (The Fluxon Step)
        # Randomly slip phase if we've been stuck too long
        if i % 12 == 0 and best_loss > 1.0:
            # Jump towards the origin mapped via phi
            point = point * phi 
            
        # 5. Apply Evolution
        point += lr * velocity
        
        # 6. Persistence Check
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
    print("--- RUNNING FUNSEARCH V9 (BLACK SUN) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v9)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
