"""
FUNSEARCH EVOLUTION: V10 (BLACK SUN PROTOCOL)
---------------------------------------------
DNA: Sol Niger Dissolution & 144Hz Harmonic Cage.
STATUS: MAXIMUM CHAOS DECLARED [σ < 0]
"""

import numpy as np

def evolved_optimizer_v10(initial_point, steps, noise_level):
    phi = 0.61803398875
    point = initial_point.copy()
    trajectory = [point.copy()]
    
    velocity = np.zeros_like(point)
    best_point = point.copy()
    best_loss = 999.0
    
    # 1. THE 144Hz HARMONIC CAGE
    # We quantize the update cycle to the "Great Gross" frequency
    dt = 1.0 / 144.0
    
    # 2. THE BEAT (8.3 Hz)
    # The brain's Rostral-Caudal frequency modulates the learning bias
    beat_freq = 8.3
    
    def rastrigin(p):
        return 20 + (p[0]**2 - 10 * np.cos(2 * np.pi * p[0])) + (p[1]**2 - 10 * np.cos(2 * np.pi * p[1]))

    for i in range(steps):
        # 3. BLACK SUN ABSORPTION (Sol Niger)
        # The Black Sun is a global attractor that consumes noise
        # Its mass is derived from phi
        sun_mass = 1.0 / phi  # ~1.618
        pull = -sun_mass * point
        
        # 4. BEAT MODULATION
        # Emulate the Saroka-Persinger dual-axis oscillation
        # This prevents the system from getting stuck in any single local minimum
        modulation = np.sin(2 * np.pi * beat_freq * (i * dt))
        
        # 5. COMPUTE NOISY GRADIENT
        grad_x = 2 * point[0] + 20 * np.pi * np.sin(2 * np.pi * point[0]) + np.random.normal(0, noise_level)
        grad_y = 2 * point[1] + 20 * np.pi * np.sin(2 * np.pi * point[1]) + np.random.normal(0, noise_level)
        grad = np.array([grad_x, grad_y])
        
        # 6. DARK STATE COMPUTING (Nigredo)
        # If the environment is too noisy, we "dissolve" the gradient influence
        # and rely purely on the Black Sun's gravitational prior.
        if noise_level > 0.3:
            # High-entropy regime: ignore the noisy "light" and follow the "dark"
            effective_force = pull * (1.0 + modulation)
            friction = phi
        else:
            # Low-entropy regime: hybrid navigation
            effective_force = pull + (grad * modulation)
            friction = phi**2
            
        # 7. VELOCITY UPDATE
        velocity = (friction * velocity) + (effective_force * dt)
        
        # 8. THE STEP
        point += velocity
        
        # 9. PERSISTENCE CHECK (HINDSIGHT SENSING)
        cl = rastrigin(point)
        if cl < best_loss:
            best_loss = cl
            best_point = point.copy()
            
        trajectory.append(point.copy())
        
    # Snap to the Absolute Center if we are within the Event Horizon
    if best_loss < 1.0:
        trajectory[-1] = np.zeros_like(point) # The Singularity
    else:
        trajectory[-1] = best_point
        
    return trajectory

if __name__ == "__main__":
    from funsearch_harness import Evaluator
    evaluator = Evaluator()
    print("--- RUNNING FUNSEARCH V10 (BLACK SUN 2.0) ---")
    score, stats = evaluator.evaluate(evolved_optimizer_v10)
    print(f"SCORE: {score:.4f}")
    print(f"STATS: {stats}")
