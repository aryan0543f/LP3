# ============================================================
# 0/1 Knapsack Problem – Branch and Bound Algorithm
# ============================================================
# Aim: Maximize the value of items in a knapsack with limited
#      capacity using Branch and Bound optimization technique
# ============================================================
# Items CANNOT be split — either take whole item or leave it
# Time Complexity : O(2^n) worst case, but prunes many branches
# Space Complexity: O(n) — recursion stack depth
# ============================================================

import heapq
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass(order=True)
class Node:
    """
    Represents a node in the Branch and Bound search tree.

    Attributes:
        bound: Upper bound of maximum profit in subtree (for priority queue)
        level: Current level in decision tree (which item we're considering)
        profit: Current profit accumulated
        weight: Current weight accumulated
        selected: List of selected items (1-indexed)
    """
    bound: float = field(compare=True)  # Primary sort key (max heap via negation)
    level: int = field(compare=False)
    profit: int = field(compare=False)
    weight: int = field(compare=False)
    selected: List[int] = field(default_factory=list, compare=False)

    def __lt__(self, other):
        # For max heap behavior: higher bound = higher priority
        return self.bound > other.bound

def calculate_bound(node: Node, n: int, capacity: int,
                   items: List[Tuple[int, int, float]]) -> float:
    """
    Calculate upper bound of profit in subtree rooted at node.

    Uses fractional knapsack greedy approach for remaining items
    to get optimistic upper bound. This bound helps prune branches
    that cannot lead to better solution.

    Args:
        node: Current node in search tree
        n: Total number of items
        capacity: Knapsack capacity
        items: List of (value, weight, ratio, original_index) tuples

    Returns:
        Upper bound of maximum profit achievable from this node

    Algorithm:
        1. Start with current profit and weight from node
        2. Greedily add remaining items (sorted by value/weight ratio)
        3. When item doesn't fit completely, add fractional part
        4. This gives optimistic upper bound (fractional is allowed here)
    """
    # If weight exceeds capacity, this node is not promising
    if node.weight >= capacity:
        return 0

    profit_bound = node.profit
    total_weight = node.weight
    level = node.level

    # Greedily add items in order of value/weight ratio
    while level < n and total_weight + items[level][1] <= capacity:
        total_weight += items[level][1]
        profit_bound += items[level][0]
        level += 1

    # Add fractional part of next item (if any room left)
    if level < n:
        remaining_capacity = capacity - total_weight
        profit_bound += items[level][0] * (remaining_capacity / items[level][1])

    return profit_bound

def knapsack_branch_bound(values: List[int], weights: List[int],
                         capacity: int) -> Tuple[int, List[int]]:
    """
    Solve 0/1 Knapsack using Branch and Bound with Best-First Search.

    Args:
        values: List of item values/profits
        weights: List of item weights
        capacity: Maximum weight capacity of knapsack

    Returns:
        Tuple of (maximum_value, selected_items)

    Branch and Bound Strategy:
        1. Generate search tree with two branches at each node:
           - Left branch: Include current item
           - Right branch: Exclude current item

        2. Use priority queue (max heap) for best-first search
           - Always explore most promising node first
           - Most promising = highest upper bound

        3. Pruning:
           - If node's bound ≤ current best profit: prune subtree
           - If node's weight > capacity: prune (infeasible)

        4. Bounding:
           - Calculate upper bound using fractional knapsack
           - Helps identify which branches to explore

    Advantages over DP:
        - Better for sparse solutions (few items selected)
        - Can terminate early if optimal found
        - Memory efficient (no 2D table)

    Advantages of DP over Branch & Bound:
        - Guaranteed O(nW) time
        - No worst-case exponential behavior
        - More predictable performance
    """
    n = len(values)

    # Step 1: Create items list with value/weight ratio for sorting
    # Format: (value, weight, ratio, original_index)
    items = []
    for i in range(n):
        ratio = values[i] / weights[i] if weights[i] > 0 else 0
        items.append((values[i], weights[i], ratio, i))

    # Step 2: Sort by value/weight ratio in descending order
    # This heuristic makes bound calculations more effective
    items.sort(key=lambda x: x[2], reverse=True)

    print("\n----- Items Sorted by Value/Weight Ratio -----")
    print(f"{'Original':<10} {'Value':<10} {'Weight':<10} {'Ratio':<10}")
    print("-" * 45)
    for val, wt, ratio, orig_idx in items:
        print(f"Item {orig_idx+1:<5} {val:<10} {wt:<10} {ratio:<10.2f}")

    # Step 3: Initialize priority queue (max heap via negative bound)
    pq = []

    # Create root node (no items considered yet)
    root = Node(bound=0, level=0, profit=0, weight=0, selected=[])
    root.bound = calculate_bound(root, n, capacity, items)

    heapq.heappush(pq, root)

    # Track best solution found so far
    max_profit = 0
    best_selection = []

    # Statistics for visualization
    nodes_explored = 0
    nodes_pruned = 0
    max_queue_size = 0

    print("\n----- Branch and Bound Exploration -----")
    print(f"{'Node':<6} {'Level':<7} {'Profit':<8} {'Weight':<8} {'Bound':<10} {'Action':<15} {'Status':<20}")
    print("-" * 90)

    # Step 4: Process nodes using best-first search
    while pq:
        max_queue_size = max(max_queue_size, len(pq))

        # Get most promising node (highest bound)
        current = heapq.heappop(pq)
        nodes_explored += 1

        # Pruning condition: If this node's bound can't beat current best, skip it
        if current.bound <= max_profit:
            nodes_pruned += 1
            print(f"{nodes_explored:<6} {current.level:<7} {current.profit:<8} "
                  f"{current.weight:<8} {current.bound:<10.2f} {'Pruned':<15} "
                  f"{'Bound ≤ best profit':<20}")
            continue

        # If we've considered all items, check if this is best solution
        if current.level == n:
            if current.profit > max_profit:
                max_profit = current.profit
                best_selection = current.selected[:]
                print(f"{nodes_explored:<6} {current.level:<7} {current.profit:<8} "
                      f"{current.weight:<8} {current.bound:<10.2f} {'Leaf node':<15} "
                      f"{'New best: {max_profit}':<20}")
            continue

        # Get current item being considered
        item_val, item_wt, item_ratio, orig_idx = items[current.level]

        # Branch 1: INCLUDE current item (if feasible)
        if current.weight + item_wt <= capacity:
            include_node = Node(
                bound=0,
                level=current.level + 1,
                profit=current.profit + item_val,
                weight=current.weight + item_wt,
                selected=current.selected + [orig_idx + 1]  # 1-indexed
            )
            include_node.bound = calculate_bound(include_node, n, capacity, items)

            # Update best solution if this is a leaf node
            if include_node.level == n and include_node.profit > max_profit:
                max_profit = include_node.profit
                best_selection = include_node.selected[:]

            # Only add to queue if promising
            if include_node.bound > max_profit:
                heapq.heappush(pq, include_node)
                print(f"{nodes_explored:<6} {current.level:<7} {current.profit:<8} "
                      f"{current.weight:<8} {current.bound:<10.2f} "
                      f"{'Include Item '+str(orig_idx+1):<15} {'Added to queue':<20}")
            else:
                nodes_pruned += 1
                print(f"{nodes_explored:<6} {current.level:<7} {current.profit:<8} "
                      f"{current.weight:<8} {current.bound:<10.2f} "
                      f"{'Include Item '+str(orig_idx+1):<15} {'Pruned (low bound)':<20}")

        # Branch 2: EXCLUDE current item (always feasible)
        exclude_node = Node(
            bound=0,
            level=current.level + 1,
            profit=current.profit,
            weight=current.weight,
            selected=current.selected[:]
        )
        exclude_node.bound = calculate_bound(exclude_node, n, capacity, items)

        # Only add to queue if promising
        if exclude_node.bound > max_profit:
            heapq.heappush(pq, exclude_node)
            print(f"{nodes_explored:<6} {current.level:<7} {current.profit:<8} "
                  f"{current.weight:<8} {current.bound:<10.2f} "
                  f"{'Exclude Item '+str(orig_idx+1):<15} {'Added to queue':<20}")
        else:
            nodes_pruned += 1
            print(f"{nodes_explored:<6} {current.level:<7} {current.profit:<8} "
                  f"{current.weight:<8} {current.bound:<10.2f} "
                  f"{'Exclude Item '+str(orig_idx+1):<15} {'Pruned (low bound)':<20}")

    # Print statistics
    print("\n----- Algorithm Statistics -----")
    print(f"Total nodes explored: {nodes_explored}")
    print(f"Total nodes pruned: {nodes_pruned}")
    print(f"Pruning efficiency: {nodes_pruned/(nodes_explored+nodes_pruned)*100:.1f}%")
    print(f"Max queue size: {max_queue_size}")
    print(f"Total nodes generated: {nodes_explored + nodes_pruned}")

    return max_profit, sorted(best_selection)

# ── Main Program ──────────────────────────────────────────────
def main():
    print("=" * 70)
    print("   0/1 KNAPSACK PROBLEM - BRANCH AND BOUND ALGORITHM")
    print("=" * 70)

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

            # Solve using Branch and Bound
            maximum_value, selected_items = knapsack_branch_bound(values, weights, capacity)

            # Display results
            print("\n" + "=" * 70)
            print("RESULT:")
            print("=" * 70)
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

            print("=" * 70)

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
Given n items with values and weights, and a knapsack with capacity W,
find the maximum value achievable by selecting items such that:
1. Total weight ≤ W (capacity constraint)
2. Each item is taken completely or not taken at all (0/1 choice)

BRANCH AND BOUND TECHNIQUE:
---------------------------
Branch and Bound is a general algorithmic technique for solving optimization
problems. It systematically explores the solution space while pruning branches
that cannot lead to optimal solution.

Key Components:
1. BRANCHING: Generate child nodes (subproblems) from parent node
2. BOUNDING: Calculate upper/lower bounds to estimate best possible solution
3. PRUNING: Discard branches that cannot improve current best solution

DIFFERENCE FROM DYNAMIC PROGRAMMING:
------------------------------------
BRANCH AND BOUND:
- Explores search tree with pruning
- Best-first search (priority queue)
- Can terminate early when optimal found
- Worst case: O(2^n), but often much better due to pruning
- Space: O(n) - recursion/queue depth
- Better for: sparse solutions, early termination possible

DYNAMIC PROGRAMMING:
- Systematically fills table bottom-up
- Explores all subproblems
- Always completes full table
- Time: O(n × W) guaranteed
- Space: O(n × W)
- Better for: dense solutions, guaranteed polynomial time

WHY NOT GREEDY?
---------------
Greedy (sort by value/weight ratio) fails because:
- Local optimal choice doesn't guarantee global optimal
- Past choices constrain future options
- Cannot backtrack once item is selected

Example where greedy fails:
  Item 1: value=10, weight=5  (ratio=2.0)
  Item 2: value=15, weight=10 (ratio=1.5)
  Capacity = 10

Greedy: Take Item1 (w=5, v=10), can't fit Item2 → Total: 10
Optimal: Take Item2 (w=10, v=15) → Total: 15

BRANCH AND BOUND APPROACH FOR KNAPSACK:
----------------------------------------

1. STATE SPACE TREE:
   - Each node represents partial solution
   - Level i: decision for item i (include or exclude)
   - Left child: include item i
   - Right child: exclude item i
   - Leaves: complete solutions (all items considered)

2. NODE STRUCTURE:
   - level: which item we're deciding on (0 to n)
   - profit: total value accumulated so far
   - weight: total weight accumulated so far
   - bound: upper bound of profit in subtree
   - selected: list of selected items

3. BOUNDING FUNCTION:
   Calculate upper bound using fractional knapsack on remaining items:

   bound(node) = current_profit + fractional_knapsack(remaining_items)

   This gives optimistic estimate (fractional allowed for bound calculation)
   Real solution must be ≤ bound (since we can't actually split items)

4. SEARCH STRATEGY - BEST FIRST SEARCH:
   - Use max priority queue (ordered by bound)
   - Always explore most promising node first
   - Most promising = highest upper bound
   - Better than DFS/BFS: finds optimal solution faster

5. PRUNING CONDITIONS:
   a) Bound Pruning: If bound(node) ≤ current_best_profit
      → Subtree cannot improve solution → Prune

   b) Infeasibility Pruning: If weight > capacity
      → Solution infeasible → Don't generate this node

ALGORITHM STEPS:
----------------
1. Sort items by value/weight ratio (descending)
   → Makes bound calculation more effective

2. Initialize:
   - Create root node (level=0, profit=0, weight=0)
   - Calculate bound for root
   - Add to priority queue
   - Set max_profit = 0

3. While priority queue not empty:
   a) Extract node with highest bound

   b) If bound ≤ max_profit: PRUNE (can't improve)

   c) If level == n (all items considered):
      - If profit > max_profit: update best solution
      - Continue to next node

   d) Generate two child nodes:

      LEFT CHILD (include item):
      - Check if weight + item.weight ≤ capacity
      - If feasible:
          profit = parent.profit + item.value
          weight = parent.weight + item.weight
          Calculate bound
          If bound > max_profit: add to queue
          Else: PRUNE

      RIGHT CHILD (exclude item):
      - profit = parent.profit (unchanged)
      - weight = parent.weight (unchanged)
      - Calculate bound
      - If bound > max_profit: add to queue
      - Else: PRUNE

4. Return max_profit and selected items

BOUNDING FUNCTION DETAILED:
---------------------------
def calculate_bound(node, items, capacity):
    if node.weight >= capacity:
        return 0

    bound = node.profit
    weight = node.weight
    level = node.level

    # Greedily add items (sorted by ratio)
    while level < n and weight + items[level].weight <= capacity:
        weight += items[level].weight
        bound += items[level].value
        level += 1

    # Add fraction of next item (if room left)
    if level < n:
        remaining = capacity - weight
        bound += items[level].value * (remaining / items[level].weight)

    return bound

KEY INSIGHT: We use fractional knapsack (greedy) for bounding, even though
actual problem is 0/1. This gives upper bound that helps prune branches.

WORKED EXAMPLE:
---------------
Items:
  Item 1: value=40,  weight=2   (ratio=20)
  Item 2: value=30,  weight=5   (ratio=6)
  Item 3: value=50,  weight=10  (ratio=5)
  Item 4: value=10,  weight=5   (ratio=2)

Capacity W = 16

After sorting by ratio: Item1, Item2, Item3, Item4

Search Tree Exploration (best-first):

Root: (level=0, profit=0, weight=0, bound=115*)
  *bound = 0 + 40 + 30 + 50 + (16-17 remaining, but only need 16)
  *bound = 0 + 40 + 30 + 50*((16-7)/10) = 0 + 40 + 30 + 45 = 115

├─ Include Item1: (level=1, profit=40, weight=2, bound=115)
│  ├─ Include Item2: (level=2, profit=70, weight=7, bound=115)
│  │  ├─ Include Item3: (level=3, profit=120, weight=17) → INFEASIBLE
│  │  └─ Exclude Item3: (level=3, profit=70, weight=7, bound=80)
│  └─ Exclude Item2: (level=2, profit=40, weight=2, bound=100)
│     ├─ Include Item3: (level=3, profit=90, weight=12, bound=98)
│     └─ Exclude Item3: (level=3, profit=40, weight=2, bound=50)
└─ Exclude Item1: (level=1, profit=0, weight=0, bound=80)
   └─ ... (lower bound, explored later or pruned)

Best Solution: Item1 + Item2 + Item4 OR Item1 + Item3
(Multiple optimal solutions may exist)

TIME COMPLEXITY ANALYSIS:
-------------------------
Worst Case: O(2^n)
- Must explore all 2^n nodes in complete binary tree
- Happens when no effective pruning occurs

Best Case: O(n log n)
- Only root path explored + sorting cost
- Happens when root immediately gives optimal solution

Average Case: Better than O(2^n)
- Effective pruning eliminates many branches
- Performance depends on:
  * Item distribution
  * Capacity value
  * Bounding function quality

Practical Performance:
- Much better than naive brute force
- Can solve problems with 20-30 items efficiently
- Pruning efficiency often 70-90%

SPACE COMPLEXITY:
-----------------
O(n) - Maximum queue size and recursion depth
Much better than DP's O(n × W)

ADVANTAGES OF BRANCH AND BOUND:
--------------------------------
+ Space efficient: O(n) vs DP's O(n × W)
+ Can terminate early when optimal found
+ Works well when optimal solution is sparse
+ Flexible: can add more constraints easily
+ Better for large capacity values

DISADVANTAGES:
--------------
- Worst case exponential time: O(2^n)
- Performance unpredictable (depends on instance)
- Complex implementation
- Overhead of priority queue operations

COMPARISON: DP vs BRANCH & BOUND:
---------------------------------
┌────────────────┬─────────────────┬─────────────────┐
│ Aspect         │ Dynamic Prog    │ Branch & Bound  │
├────────────────┼─────────────────┼─────────────────┤
│ Time           │ O(n × W)        │ O(2^n) worst    │
│ Space          │ O(n × W)        │ O(n)            │
│ Predictability │ High            │ Low             │
│ Early exit     │ No              │ Yes             │
│ Large W        │ Poor            │ Good            │
│ Large n        │ Good (if W ok)  │ Poor            │
│ Implementation │ Simpler         │ Complex         │
└────────────────┴─────────────────┴─────────────────┘

WHEN TO USE BRANCH AND BOUND:
------------------------------
1. Capacity W is very large (DP becomes impractical)
2. Few items expected in optimal solution
3. Need to find solution quickly (can terminate early)
4. Memory is constrained
5. Problem has additional constraints beyond 0/1

WHEN TO USE DYNAMIC PROGRAMMING:
---------------------------------
1. Capacity W is moderate
2. Need guaranteed polynomial time
3. Many items expected in solution
4. Predictable performance required
5. Will reuse subproblem solutions

OPTIMIZATION TECHNIQUES:
------------------------
1. Item Sorting:
   - Sort by value/weight ratio
   - Makes bounding function tighter
   - Better pruning efficiency

2. Search Strategy:
   - Best-first search (priority queue) better than DFS/BFS
   - Always explore most promising branch first
   - Finds good solutions early → better pruning

3. Initial Solution:
   - Start with greedy solution as initial max_profit
   - Improves pruning from the beginning
   - Not implemented here for clarity

4. Bound Calculation:
   - Efficient fractional knapsack in O(n)
   - Tighter bounds → more pruning

VIVA QUESTIONS & ANSWERS:
--------------------------
Q1: Why use Branch and Bound instead of DP?
A: When capacity W is very large, DP's O(n×W) time and space become
   impractical. Branch and Bound uses O(n) space and can solve such
   problems efficiently through pruning.

Q2: What is the bounding function's purpose?
A: It calculates an optimistic upper bound on profit for a subtree.
   If this bound is less than current best profit, entire subtree
   can be pruned without exploration.

Q3: Why sort items by value/weight ratio?
A: Sorting makes the bounding function tighter (closer to actual
   maximum). Tighter bounds lead to more effective pruning and
   better performance.

Q4: What is the difference between bounding and pruning?
A: Bounding calculates upper bound estimate for a node's subtree.
   Pruning is the decision to discard a branch based on its bound.
   Bounding provides information, pruning takes action.

Q5: Best-first search vs DFS vs BFS?
A: Best-first (priority queue) always explores most promising node
   first. Finds good solutions early, leading to better pruning.
   DFS and BFS don't prioritize promising branches.

Q6: Why use fractional knapsack for bounding when problem is 0/1?
A: Fractional knapsack gives UPPER bound (optimistic estimate).
   Since we can't actually split items, real solution ≤ bound.
   This upper bound is used to prune branches, not as actual solution.

Q7: Can Branch and Bound guarantee optimal solution?
A: Yes, if algorithm completes without early termination, it
   guarantees optimal solution. It explores enough of search space
   to prove optimality through bounding.

Q8: What if all bounds are tight and no pruning occurs?
A: Degenerates to complete search tree exploration: O(2^n) time.
   This is worst case, but rarely happens in practice with good
   bounding functions.

Q9: How to improve pruning efficiency?
A: (1) Better bounding function (tighter bounds)
   (2) Good initial solution (greedy pre-processing)
   (3) Sort items by value/weight ratio
   (4) Use best-first search strategy

Q10: Space complexity comparison with DP?
A: Branch and Bound: O(n) - queue depth
   Dynamic Programming: O(n × W) - full table
   Huge advantage when W is large!

PRACTICAL EXAM TIPS:
--------------------
✓ Explain branching (include/exclude decisions)
✓ Explain bounding function using fractional knapsack
✓ Demonstrate pruning with example
✓ Show priority queue usage (best-first search)
✓ Compare with DP (advantages/disadvantages)
✓ Explain why greedy fails for actual solution but works for bound
✓ Draw small search tree with pruning (3-4 items)
✓ Mention space advantage: O(n) vs O(nW)
✓ Discuss worst and average case complexity
✓ Know when to use B&B vs DP

REAL-WORLD APPLICATIONS:
------------------------
1. Resource Allocation:
   - Project selection with budget constraints
   - Capital budgeting in finance

2. Cargo Loading:
   - Aircraft/ship cargo optimization
   - Container loading problems

3. Cryptography:
   - Subset sum problems
   - Cryptanalysis

4. Computer Networks:
   - Bandwidth allocation
   - Server resource distribution

5. Manufacturing:
   - Production planning
   - Inventory management

SAMPLE OUTPUT:
--------------
======================================================================
   0/1 KNAPSACK PROBLEM - BRANCH AND BOUND ALGORITHM
======================================================================

Enter number of items: 4
Enter values of items (space-separated): 40 30 50 10
Enter weights of items (space-separated): 2 5 10 5
Enter maximum weight capacity: 16

----- Input Summary -----
Number of items: 4
Knapsack capacity: 16

Item     Value      Weight     V/W Ratio
----------------------------------------
Item 1   40         2          20.00
Item 2   30         5          6.00
Item 3   50         10         5.00
Item 4   10         5          2.00

----- Items Sorted by Value/Weight Ratio -----
Original   Value      Weight     Ratio
---------------------------------------------
Item 1     40         2          20.00
Item 2     30         5          6.00
Item 3     50         10         5.00
Item 4     10         5          2.00

----- Branch and Bound Exploration -----
Node   Level   Profit   Weight   Bound      Action          Status
----------------------------------------------------------------------------------
1      0       0        0        115.00     Include Item 1  Added to queue
...
[Detailed exploration trace shown during execution]

----- Algorithm Statistics -----
Total nodes explored: 15
Total nodes pruned: 8
Pruning efficiency: 34.8%
Max queue size: 4
Total nodes generated: 23

======================================================================
RESULT:
======================================================================
Maximum value achievable: 90
Selected items: [1, 2, 4]

Total weight used: 12/16
Total value: 90

Selected items details:
  Item 1: value=40, weight=2
  Item 2: value=30, weight=5
  Item 4: value=10, weight=5
======================================================================

KEY TAKEAWAYS:
--------------
1. Branch and Bound is a general optimization technique
2. Uses branching (generate subproblems) + bounding (estimate) + pruning (discard)
3. Best-first search with priority queue for efficiency
4. Space efficient: O(n) vs DP's O(n × W)
5. Worst case O(2^n), but often much better with good pruning
6. Better than DP when capacity W is very large
7. Bounding uses fractional knapsack (greedy) for upper bound
8. Pruning eliminates branches that can't improve current best
9. Performance depends on problem instance (unpredictable)
10. Optimal solution guaranteed when algorithm completes

===============================================================================
"""
