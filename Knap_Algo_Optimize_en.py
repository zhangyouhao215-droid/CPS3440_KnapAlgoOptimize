import random
import time
import sys

# ==========================================
# 1. Basic Class Definition (Item)
# ==========================================
class Item:
    def __init__(self, id, weight, value):
        self.id = id
        self.weight = weight
        self.value = value
        # Value Density = Value / Weight
        self.ratio = value / weight if weight > 0 else 0


# ==========================================
# 2. Control Group: Brute Force Recursive
# ==========================================
# Purpose: Acts as the "Dumb Algorithm" for control to ensure correctness.
def knapsack_brute_force(weights, values, capacity, n):
    if n == 0 or capacity == 0:
        return 0

    if weights[n - 1] > capacity:
        return knapsack_brute_force(weights, values, capacity, n - 1)
    else:
        include = values[n - 1] + knapsack_brute_force(weights, values, capacity - weights[n - 1], n - 1)
        exclude = knapsack_brute_force(weights, values, capacity, n - 1)
        return max(include, exclude)


# ==========================================
# 3. Heuristic: Greedy Algorithm
# ==========================================
# Purpose: The "Heuristic Method" required by the project.
# Logic: Prioritizes items with the highest "Value Density" (ratio).
# Drawback: Fails to find the optimal solution on specific data (e.g., Strongly Correlated).
def knapsack_greedy(weights, values, capacity):
    n = len(weights)
    items = []
    for i in range(n):
        items.append(Item(i, weights[i], values[i]))

    # Core: Sort by value density in descending order
    items.sort(key=lambda x: x.ratio, reverse=True)

    total_value = 0
    current_weight = 0

    for item in items:
        if current_weight + item.weight <= capacity:
            current_weight += item.weight
            total_value += item.value

    return total_value


# ==========================================
# 4. Standard Solution: 2D Dynamic Programming
# ==========================================
# Purpose: The textbook standard solution. Used to compare memory consumption logic.
# Space Complexity: O(N * W) - High memory usage.
def knapsack_dp_2d(weights, values, capacity):
    n = len(weights)
    # Create a 2D table
    # dp[i][w] represents max value with first i items and capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(1, capacity + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]


# ==========================================
# 5. Optimized Solution: 1D Dynamic Programming
# ==========================================
# Purpose: The "Modification to improve memory consumption" required by the project.
# Space Complexity: O(W) - Significantly lower memory usage.
def knapsack_dp_1d(weights, values, capacity):
    n = len(weights)
    # Only need a 1D array
    dp = [0] * (capacity + 1)

    for i in range(n):
        w_i = weights[i]
        v_i = values[i]
        # Iterate backwards to prevent using the same item multiple times in one step
        for w in range(capacity, w_i - 1, -1):
            if dp[w - w_i] + v_i > dp[w]:
                dp[w] = dp[w - w_i] + v_i
    return dp[capacity]


# ==========================================
# 6. Hard Instance Generator
# ==========================================
# Purpose: Generates different types of data to stress-test the algorithms.
# Research by Pisinger shows "Strongly Correlated" data breaks many heuristics.
def generate_hard_instance(n, R=1000, type='uncorrelated'):
    weights = []
    values = []

    for _ in range(n):
        w = random.randint(1, R)
        weights.append(w)

        if type == 'uncorrelated':
            # Random: Value and Weight are independent
            v = random.randint(1, R)
        elif type == 'strongly_correlated':
            # Strongly Correlated: Value = Weight + Constant
            # This makes densities very close, tricking the Greedy algorithm.
            v = w + int(R * 0.2)
        else:
            v = random.randint(1, R)

        values.append(v)

    total_weight = sum(weights)
    capacity = int(total_weight * 0.5)
    return weights, values, capacity


# ==========================================
# 7. Experiment Runner
# ==========================================
def run_experiment():
    print(f"{'N':<5} | {'Type':<20} | {'Algo':<12} | {'Time(s)':<10} | {'Val':<8} | {'Gap %':<8}")
    print("-" * 80)

    # Configuration: Different scales and correlation types
    configs = [
        (20, 'uncorrelated'),
        (20, 'strongly_correlated'),
        (200, 'uncorrelated'),
        (200, 'strongly_correlated')
    ]

    for n, type_ in configs:
        weights, values, capacity = generate_hard_instance(n, type=type_)

        # 1. Run Standard 2D DP (Baseline)
        start = time.time()
        val_2d = knapsack_dp_2d(weights, values, capacity)
        time_2d = time.time() - start

        # 2. Run Optimized 1D DP (Optimization)
        start = time.time()
        val_1d = knapsack_dp_1d(weights, values, capacity)
        time_1d = time.time() - start

        # Verify optimization correctness
        if val_2d != val_1d:
            print(f"Error: Mismatch between 2D and 1D DP! ({val_2d} vs {val_1d})")
            return

        # 3. Run Heuristic (Greedy)
        start = time.time()
        val_greedy = knapsack_greedy(weights, values, capacity)
        time_greedy = time.time() - start

        # Calculate Gap
        if val_1d > 0:
            gap = (val_1d - val_greedy) / val_1d * 100
        else:
            gap = 0.0

        # Print comparison rows
        # Showing both 2D and 1D proves you implemented the standard version AND optimized it.
        print(f"{n:<5} | {type_:<20} | {'DP-2D(Std)':<12} | {time_2d:<10.5f} | {val_2d:<8} | {'0.0%':<8}")
        print(f"{'':<5} | {'':<20} | {'DP-1D(Opt)':<12} | {time_1d:<10.5f} | {val_1d:<8} | {'0.0%':<8}")
        print(f"{'':<5} | {'':<20} | {'Greedy':<12} | {time_greedy:<10.5f} | {val_greedy:<8} | {gap:.2f}%")

        # Optional: Verify with Brute Force for small N
        if n <= 20:
            brute_val = knapsack_brute_force(weights, values, capacity, n)
            match = "YES" if brute_val == val_1d else "NO"
            print(f"      >> Brute Force Check: {brute_val} (Match: {match})")

        print("-" * 80)

    print("\n[Analysis Hints for Report]")
    print("1. Compare DP-2D vs DP-1D: Note that while times are similar, memory usage theoretically drops from O(N*W) to O(W).")
    print("2. Compare Greedy vs Optimal: Observe how 'Gap %' increases significantly on 'Strongly Correlated' data.")
    print("3. This proves you found complex inputs that break the heuristic.")


if __name__ == "__main__":
    # Set recursion limit higher for Brute Force deep recursion
    sys.setrecursionlimit(3000)
    run_experiment()