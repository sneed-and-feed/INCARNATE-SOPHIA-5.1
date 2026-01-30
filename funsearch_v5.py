"""
FUNSEARCH EVOLUTION: V5 (GOLDEN ADAM)
-------------------------------------
DNA: Golden Ratio Biased Adaptive Moment Estimation.
"""

import numpy as np

def evolved_optimizer_v5(initial_point, steps, noise_level):
    phi = 0.61803398875
    point = initial_point.copy()
    trajectory = [point.copy()]
    
    # State for Golden Adam
    m = np.zeros_like(point)
    v = np.zeros_like(point)
    best_point = point.copy()
    
    def rastrigin(p):
        return 20 + (p[0]**2 - 10 * np.cos(2 * np.pi * p[0])) + (p[1]**2 - 10 * np.cos(2 * np.pi * p[1]))

    best_loss = rastrigin(point)
    
    # High base learning rate to escape local basins quickly
    lr_base = 0.4 

    for i in range(1, steps + 1):
        # Compute noisy gradient
        grad_x = 2 * point[0] + 20 * np.pi * np.sin(2 * np.pi * point[0]) + np.random.normal(0, noise_level)
        grad_y = 2 * point[1] + 20 * np.pi * np.sin(2 * np.pi * point[1]) + np.random.normal(0, noise_level)
        grad = np.array([grad_x, grad_y])
        
        # 1. Golden Adam Updates
        # Beta1 = phi (0.618), Beta2 = phi^2 (0.381)
        m = (phi * m) + (1.0 - phi) * grad
        v = ((phi**2) * v) + (1.0 - phi**2) * (grad**2)
        
        # 2. Bias Correction (Phi-weighted)
        m_hat = m / (1.0 - phi**i)
        v_hat = v / (1.0 - (phi**2)**i)
        
        # 3. Fractal Learning Rate
        # Decays with the golden ratio to ensure precision at the end
        lr = lr_base * (phi ** (i / steps))
        
        # 4. Apply Step
        point -= lr * m_hat / (np.sqrt(v_hat) + 1e-8)
        
        # 5. Persistence of Memory
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
    print("--- RUNNING FUNSEARCH V5 (GOLDEN ADAM) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v5)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
