# ============================================================
# 0/1 Knapsack Problem – Dynamic Programming
# ============================================================
# Aim: Maximize the value of items in a knapsack with limited
#      capacity, where items CANNOT be broken (all or nothing)
# ============================================================
# Items CANNOT be split — either take whole item or leave it
# Time Complexity : O(n * W)  — n items × W capacity
# Space Complexity: O(n * W)  — DP table
# ============================================================

def knapsack(values, weights, capacity):
    """
    Solve 0/1 Knapsack problem using Dynamic Programming.

    Args:
        values: List of item values/profits
        weights: List of item weights
        capacity: Maximum weight capacity of knapsack

    Returns:
        int: Maximum value achievable

    DP Definition:
        dp[i][w] = maximum value achievable using first i items
                   with knapsack capacity w

    Recurrence Relation:
        If weights[i-1] <= w:
            dp[i][w] = max(
                dp[i-1][w],                              # Don't take item i
                dp[i-1][w - weights[i-1]] + values[i-1]  # Take item i
            )
        Else:
            dp[i][w] = dp[i-1][w]  # Item too heavy, can't take

    Base Cases:
        dp[0][w] = 0  for all w (no items = 0 value)
        dp[i][0] = 0  for all i (0 capacity = 0 value)
    """

    n = len(values)  # Number of items

    # Step 1: Create DP table
    # dp[i][w] represents max value with first i items and capacity w
    # Dimensions: (n+1) rows × (capacity+1) columns
    dp = [[0 for w in range(capacity + 1)] for i in range(n + 1)]

    print("\n----- Building DP Table -----")
    print(f"Table dimensions: {n+1} items × {capacity+1} capacities")

    # Step 2: Fill DP table bottom-up
    for item in range(1, n + 1):
        for weight in range(1, capacity + 1):
            # Current item index in original arrays (0-indexed)
            current_item_idx = item - 1
            current_value = values[current_item_idx]
            current_weight = weights[current_item_idx]

            # Check if current item can fit in current capacity
            if current_weight <= weight:
                # Case 1: Item fits — choose better option

                # Option A: Don't include current item
                # Value = best value with previous items at same capacity
                exclude_value = dp[item - 1][weight]

                # Option B: Include current item
                # Value = current item value + best value with remaining capacity
                include_value = dp[item - 1][weight - current_weight] + current_value

                # Take maximum of both options (optimal substructure)
                dp[item][weight] = max(include_value, exclude_value)

            else:
                # Case 2: Item too heavy for current capacity
                # Can't include it, carry forward previous best value
                dp[item][weight] = dp[item - 1][weight]

    # Step 3: Display DP table for visualization
    print_dp_table(dp, weights, values, capacity, n)

    # Step 4: Backtrack to find which items were selected
    selected_items = backtrack(dp, weights, values, capacity, n)

    # The bottom-right cell contains the final answer
    return dp[n][capacity], selected_items

def print_dp_table(dp, weights, values, capacity, n):
    """
    Print the DP table in a formatted manner for visualization.
    Shows how optimal values are built up step by step.
    """
    print("\n----- DP Table (Rows=Items, Cols=Capacity) -----")

    # Print header row (capacities)
    print(f"{'Item':<10}", end="")
    for w in range(capacity + 1):
        print(f"{w:>5}", end="")
    print()
    print("-" * (10 + 5 * (capacity + 1)))

    # Print each row
    for i in range(n + 1):
        if i == 0:
            label = "None"
        else:
            label = f"{i} (v={values[i-1]}, w={weights[i-1]})"

        print(f"{label:<10}", end="")
        for w in range(capacity + 1):
            print(f"{dp[i][w]:>5}", end="")
        print()

    print()

def backtrack(dp, weights, values, capacity, n):
    """
    Backtrack through DP table to find which items were selected.

    Algorithm:
        Start from dp[n][capacity] (bottom-right)
        If dp[i][w] != dp[i-1][w], item i was included
        Move to dp[i-1][w - weight[i-1]] when item included
        Move to dp[i-1][w] when item excluded

    Returns:
        List of selected item indices (1-indexed)
    """
    print("----- Backtracking to Find Selected Items -----")

    selected = []
    w = capacity

    for i in range(n, 0, -1):
        # Check if value changed from previous row
        # If yes, item i was included
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i)
            print(f"Item {i} included: value={values[i-1]}, weight={weights[i-1]}")
            # Reduce capacity by weight of selected item
            w -= weights[i - 1]
        else:
            print(f"Item {i} excluded")

    selected.reverse()  # Reverse to get items in order
    return selected

# ── Main Program ──────────────────────────────────────────────
def main():
    print("=" * 60)
    print("   0/1 KNAPSACK PROBLEM - DYNAMIC PROGRAMMING")
    print("=" * 60)

    while True:
        try:
            # Input number of items
            n = int(input("\nEnter number of items: "))

            # Input values and weights
            values = [int(i) for i in input("Enter values of items (space-separated): ").split()]
            weights = [int(i) for i in input("Enter weights of items (space-separated): ").split()]

            # Validate input lengths
            if len(values) != n or len(weights) != n:
                print(f"Error: Expected {n} items, but got {len(values)} values and {len(weights)} weights")
                continue

            # Input knapsack capacity
            capacity = int(input("Enter maximum weight capacity: "))

            # Display input summary
            print("\n----- Input Summary -----")
            print(f"Number of items: {n}")
            print(f"Knapsack capacity: {capacity}")
            print(f"\n{'Item':<8} {'Value':<10} {'Weight':<10} {'V/W Ratio':<10}")
            print("-" * 40)
            for i in range(n):
                ratio = values[i] / weights[i] if weights[i] > 0 else 0
                print(f"Item {i+1:<3} {values[i]:<10} {weights[i]:<10} {ratio:<10.2f}")

            # Solve using DP
            maximum_value, selected_items = knapsack(values, weights, capacity)

            # Display results
            print("\n" + "=" * 60)
            print("RESULT:")
            print("=" * 60)
            print(f"Maximum value achievable: {maximum_value}")
            print(f"Selected items: {selected_items}")

            # Calculate total weight of selected items
            total_weight = sum(weights[i-1] for i in selected_items)
            total_value = sum(values[i-1] for i in selected_items)

            print(f"\nTotal weight used: {total_weight}/{capacity}")
            print(f"Total value: {total_value}")

            print("\nSelected items details:")
            for item_num in selected_items:
                idx = item_num - 1
                print(f"  Item {item_num}: value={values[idx]}, weight={weights[idx]}")

            print("=" * 60)

            # Ask if user wants to continue
            choice = input("\nDo you want to solve another problem? (y/n): ").strip().lower()
            if choice != 'y':
                print("Thank you for using the program!")
                break

        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            break
        except ValueError:
            print("Error: Please enter valid integers.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

"""
===============================================================================
                         PRACTICAL EXAM EXPLANATION
===============================================================================

PROBLEM STATEMENT:
------------------
Given n items, each with a value and weight, and a knapsack with capacity W,
find the maximum value that can be achieved by selecting items such that:
1. Total weight ≤ W (capacity constraint)
2. Each item is either taken completely or not taken at all (0/1 choice)

DIFFERENCE FROM FRACTIONAL KNAPSACK:
-------------------------------------
0/1 KNAPSACK:
- Items CANNOT be broken (binary choice: take or leave)
- Requires DYNAMIC PROGRAMMING
- Time: O(n × W)
- Greedy approach does NOT work

FRACTIONAL KNAPSACK:
- Items CAN be broken into fractions
- Solved using GREEDY approach (sort by value/weight ratio)
- Time: O(n log n)
- Always optimal with greedy

WHY GREEDY FAILS FOR 0/1 KNAPSACK:
-----------------------------------
Example:
  Item 1: value=10, weight=5  (ratio=2.0)
  Item 2: value=15, weight=10 (ratio=1.5)
  Item 3: value=20, weight=15 (ratio=1.33)
  Capacity = 20

Greedy (by ratio): Take Item1 (w=5, v=10) + Item2 (w=10, v=15) = Total: 25
Optimal Solution: Take Item2 (w=10, v=15) + Item3 (w=15, v=20) = Total: 35

Greedy gives suboptimal result because past choices affect future options!

DYNAMIC PROGRAMMING APPROACH:
------------------------------
Key Concepts:
1. Optimal Substructure:
   Optimal solution contains optimal solutions to subproblems

2. Overlapping Subproblems:
   Same subproblems are solved multiple times

3. Bottom-Up Construction:
   Build solution from smaller subproblems to larger ones

DP STATE DEFINITION:
--------------------
dp[i][w] = maximum value achievable using first i items
           with knapsack capacity w

Dimensions:
- Rows: 0 to n (number of items + 1 for base case)
- Columns: 0 to W (capacity values from 0 to W)

RECURRENCE RELATION:
--------------------
For each item i and capacity w:

Base Cases:
  dp[0][w] = 0  (no items → 0 value)
  dp[i][0] = 0  (0 capacity → 0 value)

Recursive Case:
  If weights[i-1] <= w:  (item can fit)
    dp[i][w] = max(
        dp[i-1][w],                              # Option 1: Don't take item
        dp[i-1][w - weights[i-1]] + values[i-1]  # Option 2: Take item
    )
  Else:  (item too heavy)
    dp[i][w] = dp[i-1][w]  # Can't take, carry forward previous best

ALGORITHM STEPS:
----------------
1. Create (n+1) × (W+1) DP table, initialize with 0
2. For each item i from 1 to n:
     For each capacity w from 1 to W:
       If item i fits (weights[i-1] <= w):
         Choose max of:
           - Exclude item: dp[i-1][w]
           - Include item: dp[i-1][w - weights[i-1]] + values[i-1]
       Else:
         Can't include: dp[i-1][w]
3. Answer is dp[n][W] (all items, full capacity)
4. Backtrack to find selected items

BACKTRACKING TO FIND ITEMS:
----------------------------
Start from dp[n][W]:
  For i = n down to 1:
    If dp[i][w] != dp[i-1][w]:
      Item i was included
      w = w - weights[i-1]  (reduce capacity)
    Else:
      Item i was excluded

TIME COMPLEXITY ANALYSIS:
-------------------------
1. Creating DP table: O(n × W)
2. Filling DP table: O(n × W) — nested loops
3. Backtracking: O(n)

Overall: O(n × W)

Note: This is pseudo-polynomial time
- Polynomial in input size (n) and magnitude of W
- Not polynomial if W is very large (exponential in bits of W)

SPACE COMPLEXITY:
-----------------
O(n × W) — for DP table

Space Optimization:
- Can reduce to O(W) by keeping only current and previous row
- Trade-off: can't backtrack to find selected items easily

WORKED EXAMPLE:
---------------
Items:
  Item 1: value=60,  weight=10
  Item 2: value=100, weight=20
  Item 3: value=120, weight=30

Capacity W = 50

DP Table Construction:

      Capacity →
      0   10  20  30  40  50
    ┌──────────────────────────
  0 │ 0   0   0   0   0   0     (no items)
  1 │ 0   60  60  60  60  60    (item1: v=60, w=10)
  2 │ 0   60  100 160 160 160   (item1+2)
  3 │ 0   60  100 160 180 220   (item1+2+3)

Final Answer: 220

Backtrack:
  dp[3][50] = 220 ≠ dp[2][50] = 160  → Item 3 included, w = 50-30 = 20
  dp[2][20] = 100 ≠ dp[1][20] = 60   → Item 2 included, w = 20-20 = 0
  dp[1][0] = 0 = dp[0][0] = 0        → Item 1 not included

Selected: Item 2 + Item 3
Total: 100 + 120 = 220, Weight: 20 + 30 = 50

KEY POINTS TO MENTION DURING VIVA:
-----------------------------------
1. Why use Dynamic Programming instead of Greedy?
   → 0/1 constraint creates dependencies between choices
   → Greedy's local optimum doesn't guarantee global optimum
   → DP systematically explores all valid combinations efficiently

2. What is the meaning of dp[i][w]?
   → Maximum value achievable with first i items and capacity w
   → Represents optimal solution to subproblem

3. Explain the two choices at each step?
   → Include item: get its value + best value with remaining capacity
   → Exclude item: keep best value without using this item
   → Take maximum of both (optimal substructure)

4. What are base cases?
   → No items (i=0): value = 0 regardless of capacity
   → No capacity (w=0): value = 0 regardless of items
   → These initialize the DP table boundaries

5. How to optimize space?
   → Keep only two rows (current and previous)
   → Or use 1D array and iterate backwards
   → Reduces space to O(W)

6. Time complexity — polynomial or exponential?
   → Pseudo-polynomial: O(n × W)
   → Polynomial in n, but exponential in bit-length of W
   → If W = 2^k bits, complexity is exponential in k

7. Can we solve with recursion + memoization?
   → Yes, top-down DP approach
   → Same time/space complexity
   → Bottom-up (tabulation) is usually more efficient

8. Real-world applications?
   → Budget allocation (projects with costs and benefits)
   → Cargo loading (containers with values and weights)
   → Resource allocation in computing (CPU, memory)
   → Investment portfolio selection

COMPARISON: KNAPSACK VARIATIONS:
--------------------------------
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Type         │ Item Choice  │ Approach     │ Complexity   │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ 0/1          │ Take or      │ DP           │ O(nW)        │
│ Knapsack     │ leave        │              │              │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ Fractional   │ Can split    │ Greedy       │ O(n log n)   │
│ Knapsack     │              │              │              │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ Unbounded    │ Unlimited    │ DP           │ O(nW)        │
│ Knapsack     │ copies       │              │              │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ Bounded      │ Limited      │ DP           │ O(nWK)       │
│ Knapsack     │ copies       │              │ K=max copies │
└──────────────┴──────────────┴──────────────┴──────────────┘

SAMPLE OUTPUT:
--------------
============================================================
   0/1 KNAPSACK PROBLEM - DYNAMIC PROGRAMMING
============================================================

Enter number of items: 3
Enter values of items (space-separated): 60 100 120
Enter weights of items (space-separated): 10 20 30
Enter maximum weight capacity: 50

----- Input Summary -----
Number of items: 3
Knapsack capacity: 50

Item     Value      Weight     V/W Ratio
----------------------------------------
Item 1   60         10         6.00
Item 2   100        20         5.00
Item 3   120        30         4.00

----- Building DP Table -----
Table dimensions: 4 items × 51 capacities

----- DP Table (Rows=Items, Cols=Capacity) -----
Item          0   10   20   30   40   50
--------------------------------------------
None          0    0    0    0    0    0
1 (v=60, w=10)0   60   60   60   60   60
2 (v=100,w=20)0   60  100  160  160  160
3 (v=120,w=30)0   60  100  160  180  220

----- Backtracking to Find Selected Items -----
Item 3 included: value=120, weight=30
Item 2 included: value=100, weight=20
Item 1 excluded

============================================================
RESULT:
============================================================
Maximum value achievable: 220
Selected items: [2, 3]

Total weight used: 50/50
Total value: 220

Selected items details:
  Item 2: value=100, weight=20
  Item 3: value=120, weight=30
============================================================

PRACTICAL EXAM TIPS:
--------------------
✓ Clearly explain why greedy doesn't work (with counterexample)
✓ Define DP state and recurrence relation precisely
✓ Draw the DP table for small example (3 items, capacity ~30)
✓ Show both choices (include/exclude) at each cell
✓ Demonstrate backtracking process to find items
✓ Mention space optimization (from O(nW) to O(W))
✓ Compare with Fractional Knapsack
✓ Know time complexity is pseudo-polynomial
✓ Explain optimal substructure and overlapping subproblems

ADVANTAGES:
-----------
+ Guarantees optimal solution
+ Handles discrete (0/1) choices correctly
+ Can be extended to many variations
+ Relatively efficient for moderate W

DISADVANTAGES:
--------------
- Space: O(nW) can be large for big W
- Pseudo-polynomial time (exponential in bits of W)
- Not suitable for very large capacity values
- More complex than greedy approach

===============================================================================
"""
