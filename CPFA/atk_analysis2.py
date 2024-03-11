import numpy as np
from scipy.integrate import quad
from math import exp, factorial
import matplotlib.pyplot as plt

# Model Parameters
lambda_f = 4.0  # Rate of foragers laying real pheromone trails
lambda_d = 1.0  # Rate of detractors laying misleading pheromone trails
lambda_decay = 0.063119269938  # Rate of exponential decay of pheromone
N_f0 = 24  # Initial number of foragers
N_d_scenarios = [2, 4, 7, 9, 12]  # Different scenarios of detractor numbers
T = 1800  # Total simulation time in seconds
dt = 1  # Time step

# Poisson distribution function
def poisson_cdf(c, lambda_p):

    P = np.sum([exp(-lambda_p) * (lambda_p**i) / factorial(i) for i in range(int(c) + 1)])
    # print ("Poisson CDF: ", P)
    return np.sum([exp(-lambda_p) * (lambda_p**i) / factorial(i) for i in range(int(c) + 1)])

# Function to calculate the expected number of trails
def expected_trails(N, lambda_p, c_max=4):
    func = lambda c: N * poisson_cdf(c, lambda_p)
    result, _ = quad(func, 0, c_max)
    return result

# Main simulation function

# def simulate_forager_captures(N_f0, N_d, lambda_decay, T, dt):
#     N_f = N_f0  # Initialize the number of foragers
#     captures_over_time = []  # Store captures at each time step
    
#     for t in range(0, T, dt):
#         N_rf = expected_trails(N_f, lambda_f)
#         print(f"N_rf: {N_rf}")
#         N_md = expected_trails(N_d, lambda_d)
#         print(f"N_md: {N_md}")
#         N_active = (N_rf + N_md) * exp(-lambda_decay * t)
#         print(f"N_active: {N_active}")
#         if N_active:
#             P_capture = N_md / N_active
#         else:
#             P_capture = 0
#             print(f"No active trails at time {t} seconds")
#         # P_capture = N_md / N_active if N_active else 0
        
#         # Estimate captures at this time step
#         captures = N_f * P_capture * dt
#         if N_d > 0:
#             print(f"Time: {t}, Captures: {captures}")
#             input("Press any key to continue...")
#         N_f -= captures  # Update the number of foragers
#         captures_over_time.append(captures)
        
#     total_captures = np.sum(captures_over_time)
#     return total_captures, captures_over_time

# Adjusted to iterate through each forager for capture probability
def simulate_forager_captures(N_f0, N_d, lambda_decay, T, dt):
    foragers = [{'captured': False, 'decision_delay': 0} for _ in range(N_f0)]
    captures_over_time = np.zeros(T // dt)  # Use numpy array for efficient computations
    
    for t in range(T // dt):
        N_rf = expected_trails(sum(not f['captured'] for f in foragers), lambda_f, 4)  # Update to include only active foragers
        N_md = expected_trails(N_d, lambda_d, 4)  # Misleading trails calculation remains the same
        N_active = (N_rf + N_md) * exp(-lambda_decay * t)
        
        captures = 0
        if foragers:
            for f in foragers:
                if not f['captured'] and f['decision_delay'] == 0:
                    P_capture = N_md / N_active if N_active else 0
                    if np.random.rand() < P_capture:  # Random decision based on P_capture
                        f['captured'] = True
                        captures += 1
                f['decision_delay'] = max(0, f['decision_delay'] - 1)  # Decrease decision delay for each forager
        else:
            print(f"All foragers Captured at time {t * dt} seconds")
        
        captures_over_time[t] = captures

        # Print captures for debugging
        # if N_d > 0:
            # print(f"Time: {t*dt}, Captures: {captures}")
            # input("Press any key to continue...")
    
    return sum(f['captured'] for f in foragers), captures_over_time.tolist()


plt.figure(figsize=(10, 6))

# Colors for the plot
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Ensure you're only calling simulate_forager_captures once per N_d and using its result directly
for index, N_d in enumerate(N_d_scenarios):
    total_captures, captures_over_time = simulate_forager_captures(N_f0, N_d, lambda_decay, T, dt)
    time_steps = np.arange(0, T, dt)
    cumulative_captures = np.cumsum(captures_over_time)

    print(f"Total captures with {N_d} detractors: {total_captures}")
    
    # Ensure time_steps and cumulative_captures have the same length
    plt.plot(time_steps[:len(cumulative_captures)], cumulative_captures, label=f'{N_d} detractors', color=colors[index % len(colors)])

plt.title('Cumulative Forager Captures Over Time for Different Detractor Scenarios')
plt.xlabel('Time (seconds)')
plt.ylabel('Cumulative Number of Foragers Captured')
plt.legend()
plt.grid(True)
plt.savefig('simulated_captures_over_time.png')
