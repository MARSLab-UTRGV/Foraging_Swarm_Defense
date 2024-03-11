import numpy as np
from scipy.integrate import quad
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Constants
lambda_f = 4.0  # Rate at which foragers lay pheromone trails
lambda_d = 1.0  # Rate at which detractors lay misleading trails
N_f = 24        # Number of foragers
lambda_decay = 0.063119269938  # Decay rate of pheromone trails

# Detractor scenarios
detractor_counts = [0,2,4,7,9,12]

def poisson_probability(lambda_, c):
    """Calculate Poisson probability for a given lambda and c using the distribution's CDF."""
    # This function is correctly aimed at computing the sum for the Poisson CDF,
    # but for clarity, let's name it according to what it calculates - a probability.
    return np.exp(-lambda_) * sum([np.power(lambda_, i) / np.math.factorial(i) for i in range(int(c) + 1)])

def expected_trails(lambda_, N, c_range):
    """Calculate expected number of trails integrated over the continuous range of c."""
    # This function calculates the expected number of trails by integrating the Poisson probability over c.
    # Corrected to use 'N' to accurately reflect either N_f or N_d depending on the caller.
    result, _ = quad(lambda c: N * poisson_probability(lambda_, c), 0, c_range)
    return result

def simulate_captures(detractor_counts, c_range=8):
    """Simulate the percentage of total foragers captured for different numbers of detractors."""
    captures_percentage = []
    for N_d in detractor_counts:
        # Calculate expected number of real and misleading trails for each scenario
        N_rf = expected_trails(lambda_f, N_f, c_range)  # For foragers
        N_md = expected_trails(lambda_d, N_d, c_range)  # For detractors, corrected to pass N_d
        
        # Calculate capture probability and expected captures
        P_capture = N_md / (N_rf + N_md)
        E_captures_percentage = (N_f * P_capture) / N_f * 100  # Convert to percentage
        
        captures_percentage.append(E_captures_percentage)
    return captures_percentage

# Perform simulation and plot
simulated_captures_percentage = simulate_captures(detractor_counts)

# Plotting results with percentage on the y-axis
plt.figure(figsize=(10, 6))
plt.plot(detractor_counts, simulated_captures_percentage, label='Simulated Captures Percentage', marker='o')
plt.xlabel('Number of Detractors')
plt.ylabel('Percentage of Foragers Captured')
plt.title('Simulated Forager Captures Percentage')
plt.legend()
plt.grid(True)
plt.savefig('simulated_captures_percentage.png')
