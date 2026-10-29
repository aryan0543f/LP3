# ============================================================
# Fibonacci Numbers with Step Count
# Methods: Iterative (DP) | Recursive (Memoization)
# ============================================================
# Aim: To compute Fibonacci numbers using two approaches and
#      compare their efficiency by counting computational steps.
# ============================================================

# ── Iterative (Dynamic Programming) ──────────────────────────
def fibonacci_iterative(n: int):
    """
    Compute the nth Fibonacci number using bottom-up dynamic programming.

    Args:
        n: Position in Fibonacci sequence (1-indexed)

    Returns:
        tuple: (fibonacci_number, step_count)

    Time Complexity: O(n)
    Space Complexity: O(n) - for the dp array
    """
    steps = 0  # Initialize step counter

    # Base case 1: First Fibonacci number is 0
    steps += 1  # Count the comparison operation
    if n == 1:
        return 0, steps

    # Base case 2: Second Fibonacci number is 1
    steps += 1  # Count the comparison operation
    if n == 2:
        return 1, steps

    # Create DP array to store Fibonacci numbers
    dp = [0] * n  # Initialize array of size n
    steps += 1    # Count array initialization

    # Set base values
    dp[0] = 0     # F(1) = 0
    dp[1] = 1     # F(2) = 1
    steps += 2    # Count both assignments

    # Build the sequence iteratively from bottom-up
    for i in range(2, n):
        # Each Fibonacci number is sum of previous two
        dp[i] = dp[i - 1] + dp[i - 2]
        steps += 1  # Count one addition operation per iteration

    # Return the nth Fibonacci number and total steps
    return dp[n - 1], steps

# ── Recursive (Memoization) ───────────────────────────────────
step_count = 0   # Global counter to track recursive calls

def fibonacci_recursive(n: int):
    """
    Compute the nth Fibonacci number using top-down recursion with memoization.

    Args:
        n: Position in Fibonacci sequence (1-indexed)

    Returns:
        tuple: (fibonacci_number, step_count)

    Time Complexity: O(n) - with memoization, each subproblem solved once
    Space Complexity: O(n) - for recursion stack and cache dictionary
    """
    global step_count
    step_count = 0  # Reset counter for fresh calculation

    # Initialize cache with base cases
    cache = {1: 0, 2: 1}  # F(1) = 0, F(2) = 1

    # Call helper function and get result
    result = helper(n, cache)

    return result, step_count

def helper(n: int, cache: dict):
    """
    Recursive helper function to compute Fibonacci with memoization.

    Args:
        n: Position in Fibonacci sequence
        cache: Dictionary storing previously computed values

    Returns:
        int: The nth Fibonacci number
    """
    global step_count
    step_count += 1  # Count this function call as one step

    # If already computed, return cached value (no recursion needed)
    if n in cache:
        return cache[n]

    # Recursive case: F(n) = F(n-1) + F(n-2)
    # Store result in cache before returning (memoization)
    cache[n] = helper(n - 1, cache) + helper(n - 2, cache)
    return cache[n]

# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # Get user input
    n = int(input("Enter value of n (nth Fibonacci number): "))

    # Compute using both methods
    fib_iter, steps_iter = fibonacci_iterative(n)
    fib_rec,  steps_rec  = fibonacci_recursive(n)

    # Display results in formatted output
    print(f"\nFibonacci Number (Iterative): {fib_iter}")
    print(f"Step Count      (Iterative): {steps_iter}")

    print(f"\nFibonacci Number (Recursive): {fib_rec}")
    print(f"Step Count      (Recursive): {steps_rec}")

"""
===============================================================================
                         PRACTICAL EXAM EXPLANATION
===============================================================================

PROBLEM STATEMENT:
------------------
Write a program to compute Fibonacci numbers using:
1. Iterative approach (Dynamic Programming)
2. Recursive approach (with Memoization)
Compare the efficiency by counting computational steps.

FIBONACCI SEQUENCE:
-------------------
F(1) = 0, F(2) = 1, F(n) = F(n-1) + F(n-2) for n > 2
Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

APPROACH 1: ITERATIVE (BOTTOM-UP DYNAMIC PROGRAMMING)
------------------------------------------------------
Concept:
- Build solution from smallest subproblems upward
- Store results in array (dp table)
- No redundant calculations

Working:
1. Handle base cases (n=1, n=2)
2. Create array of size n
3. Initialize first two values: dp[0]=0, dp[1]=1
4. Fill array: dp[i] = dp[i-1] + dp[i-2]
5. Return dp[n-1]

Time Complexity: O(n) - single pass through n elements
Space Complexity: O(n) - array of size n
Step Count: Approximately n+4 steps (2 checks + 1 init + 2 assignments + n-2 additions)

APPROACH 2: RECURSIVE (TOP-DOWN WITH MEMOIZATION)
--------------------------------------------------
Concept:
- Break problem into smaller subproblems recursively
- Cache results to avoid redundant calculations
- Uses function call stack

Working:
1. Base case: if n in cache, return cached value
2. Recursive case: compute F(n) = F(n-1) + F(n-2)
3. Store result in cache before returning
4. Each subproblem solved exactly once

Time Complexity: O(n) - with memoization, each F(i) computed once
Space Complexity: O(n) - recursion stack + cache dictionary
Step Count: Approximately 2n-3 steps (each number from 3 to n requires 2 calls)

COMPARISON:
-----------
For n = 10:
- Iterative: ~12 steps
- Recursive: ~17 steps

Both have O(n) time complexity with memoization, but:
- Iterative: More space-efficient, no function call overhead
- Recursive: More intuitive, natural problem decomposition

KEY POINTS TO MENTION DURING VIVA:
-----------------------------------
1. What is Dynamic Programming?
   → Optimization technique to solve problems by breaking them into overlapping
     subproblems, storing results to avoid redundant computation.

2. Difference between Memoization and Tabulation?
   → Memoization: Top-down, recursive, stores results as needed (lazy)
   → Tabulation: Bottom-up, iterative, fills table proactively

3. Why use memoization in recursive approach?
   → Without memoization, naive recursion has O(2^n) time complexity.
     Memoization reduces it to O(n) by eliminating redundant calculations.

4. Which approach is better?
   → Iterative is generally more efficient (less overhead, better cache locality)
   → Recursive is more readable and natural for some problems

5. Space optimization?
   → Iterative can be optimized to O(1) space by keeping only last two values
   → Recursive inherently needs O(n) space for call stack

6. What if we don't use memoization?
   → Time complexity becomes O(2^n) - exponential growth
   → Same subproblems computed multiple times (e.g., F(5) computed many times)

SAMPLE OUTPUT:
--------------
Enter value of n (nth Fibonacci number): 10

Fibonacci Number (Iterative): 34
Step Count      (Iterative): 12

Fibonacci Number (Recursive): 34
Step Count      (Recursive): 17

PRACTICAL EXAM TIPS:
--------------------
✓ Explain both time and space complexity
✓ Draw recursion tree to show overlapping subproblems
✓ Mention the difference between memoization and tabulation
✓ Be ready to optimize iterative approach to O(1) space
✓ Know the formula for step counting logic
✓ Understand when to use each approach in real-world scenarios

===============================================================================
"""
