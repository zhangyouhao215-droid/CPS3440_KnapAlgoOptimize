# CPS3440_KnapAlgoOptimize
# Optimizing the 0/1 Knapsack Problem: Memory Compression & Heuristic Analysis

**Course:** CPS 3440 Algorithm Analysis | **Final Project**

## 📖 Project Overview
This project explores the **0/1 Knapsack Problem**, focusing on the trade-offs between exact algorithms (Dynamic Programming) and heuristic strategies (Greedy).

The primary goals of this project are:
1.  **Optimization**: Implementing a space-optimized **1D Dynamic Programming** algorithm to reduce memory consumption from $O(N \cdot W)$ to $O(W)$.
2.  **Adversarial Testing**: Generating **Strongly Correlated** datasets to identify "hard" inputs that break the Greedy heuristic.
3.  **Empirical Evaluation**: Comparing the performance (Time, Memory, and Accuracy) of four different algorithmic approaches.

## 👥 Team Members
* **Zhang Youhao** (1308322)
* **Lian Kexing** (1305903)
* **Sun Shijie** (1305921)
* **Zhu He** (1306014)
* **Pan Yucheng** (1306033)

## 🚀 Algorithms Implemented

| Algorithm | Type | Complexity | Role in Project |
| :--- | :--- | :--- | :--- |
| **Brute Force** | Exact | $O(2^n)$ | **Control Group**: Used to verify correctness on small inputs ($N \le 20$). |
| **Standard 2D DP** | Exact | $O(N \cdot W)$ | **Baseline**: Textbook implementation. Memory heavy for large capacities. |
| **Optimized 1D DP** | Exact | $O(W)$ | **Optimization**: Reduces memory usage by ~99% using reverse iteration and a rolling array. |
| **Greedy Heuristic** | Approx | $O(N \log N)$ | **Heuristic**: Sorts by Value Density ($v_i/w_i$). Fast but fails on correlated data. |

## 🛠️ Requirements
* Python 3.x
* No external libraries required (uses standard `random`, `time`, `sys`, `heapq`).

## 💻 Usage
To run the comparative experiment and see the empirical results:

```bash
python knapsack_final_english.py
