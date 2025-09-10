import random
import matplotlib.pyplot as plt

# -----------------------------
# Traffic Simulation Parameters
# -----------------------------
NUM_LANES = 4
SIMULATION_TIME = 100  # time units
time_slice = 5  # for round robin

# Vehicle arrival probability per lane per tick
ARRIVAL_PROB = 0.3

# -----------------------------
# Helper Functions
# -----------------------------
def generate_arrivals():
    """Randomly generate vehicles arriving at each lane."""
    arrivals = [0] * NUM_LANES
    for i in range(NUM_LANES):
        if random.random() < ARRIVAL_PROB:
            arrivals[i] = 1  # one vehicle arrives
    return arrivals

# -----------------------------
# Scheduling Algorithms
# -----------------------------
def round_robin_scheduler(queues, current_lane, time_left):
    if time_left > 0:
        return current_lane, time_left - 1
    next_lane = (current_lane + 1) % NUM_LANES
    return next_lane, time_slice - 1

def priority_scheduler(queues):
    # Lane with emergency vehicle (simulated by probability)
    if random.random() < 0.05:  # emergency occurs
        return random.randint(0, NUM_LANES - 1)
    # Otherwise pick the longest queue
    return max(range(NUM_LANES), key=lambda i: queues[i])

def srtf_scheduler(queues):
    return min(range(NUM_LANES), key=lambda i: queues[i])

# -----------------------------
# Simulation Engine
# -----------------------------
def simulate(scheduler="RR"):
    queues = [0] * NUM_LANES
    history = [[] for _ in range(NUM_LANES)]

    current_lane, time_left = 0, time_slice

    for t in range(SIMULATION_TIME):
        # Step 1: Arrivals
        arrivals = generate_arrivals()
        for i in range(NUM_LANES):
            queues[i] += arrivals[i]

        # Step 2: Scheduling
        if scheduler == "RR":
            current_lane, time_left = round_robin_scheduler(queues, current_lane, time_left)
        elif scheduler == "PR":
            current_lane = priority_scheduler(queues)
        elif scheduler == "SRTF":
            current_lane = srtf_scheduler(queues)

        # Step 3: Serve one vehicle from chosen lane
        if queues[current_lane] > 0:
            queues[current_lane] -= 1

        # Record state
        for i in range(NUM_LANES):
            history[i].append(queues[i])

    return history

# -----------------------------
# Run Simulations
# -----------------------------
strategies = {"RR": "Round Robin", "PR": "Priority", "SRTF": "Shortest Remaining Time"}

for sched in strategies:
    history = simulate(sched)
    plt.figure()
    for i in range(NUM_LANES):
        plt.plot(history[i], label=f"Lane {i+1}")
    plt.title(f"Traffic Queue Lengths - {strategies[sched]}")
    plt.xlabel("Time")
    plt.ylabel("Queue Length")
    plt.legend()
    plt.show()
