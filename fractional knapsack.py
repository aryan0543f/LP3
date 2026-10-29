# ============================================================
# Fractional Knapsack Problem – Greedy Method
# ============================================================
# Aim: Maximize the value of items in a knapsack with limited
#      capacity, where items CAN be broken into fractions
# ============================================================
# Items CAN be broken into fractions
# Greedy choice: sort by profit/weight ratio (highest first)
# Time Complexity : O(n log n) — dominated by sorting
# Space Complexity: O(n)
# ============================================================

class Item:
    """
    Represents an item with profit (value) and weight.

    Attributes:
        profit: Value/profit of the item
        weight: Weight of the item
    """
    def __init__(self, profit, weight):
        self.profit = profit  # Value/profit of the item
        self.weight = weight  # Weight of the item

def fractionalKnapsack(w, arr):
    """
    Calculate maximum value achievable in fractional knapsack using greedy approach.

    Args:
        w: Maximum capacity of knapsack
        arr: List of Item objects

    Returns:
        float: Maximum total profit achievable

    Greedy Strategy:
        1. Calculate profit/weight ratio for each item
        2. Sort items by this ratio in descending order
        3. Pick items with highest ratio first
        4. Take whole item if it fits, else take fraction

    Time Complexity: O(n log n) - sorting dominates
    Space Complexity: O(1) - in-place sorting, only scalar variables used
    """

    # Step 1: Sort items by profit/weight ratio in descending order
    # This is the GREEDY CHOICE - always pick highest value-per-weight first
    # Lambda function calculates ratio for each item during comparison
    # reverse=True ensures highest ratio comes first
    arr.sort(key=lambda x: x.profit / x.weight, reverse=True)

    # Initialize final value (total profit accumulated)
    finalValue = 0.0

    # Step 2: Iterate through sorted items and pick greedily
    for item in arr:
        # Check if current item can fit completely in remaining capacity
        if w >= item.weight:
            # Case 1: Item fits completely - take the whole item
            # Add full profit of this item to final value
            finalValue += item.profit

            # Reduce remaining capacity by weight of this item
            w -= item.weight

        else:
            # Case 2: Item doesn't fit completely - take only a fraction
            # Calculate fraction that fits: remaining_capacity / item_weight
            # Add proportional profit: item_profit × (remaining_capacity / item_weight)
            finalValue += item.profit * (w / item.weight)

            # Knapsack is now full, no point continuing the loop
            break

    # Return the maximum value achieved
    return finalValue

# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # Input: number of items
    n = int(input("Enter number of items-\n"))

    # Create list to store Item objects
    arr = []

    # Input: profit and weight for each item
    for i in range(n):
        profit = int(input(f"Enter profit of item {i + 1}-\n"))
        weight = int(input(f"Enter weight of item {i + 1}-\n"))
        # Create Item object and add to list
        arr.append(Item(profit, weight))

    # Input: maximum capacity of knapsack
    w = int(input("Enter capacity of knapsack-\n"))

    # Call fractionalKnapsack function and display result
    print("Maximum value in knapsack: ", fractionalKnapsack(w, arr))

# ── Example ───────────────────────────────────────────────────
# Items: (profit=60, weight=10), (profit=100, weight=20), (profit=120, weight=30)
# Capacity = 50
# Ratios:  60/10=6.0,  100/20=5.0,  120/30=4.0
# Take item1 fully (10kg, +60), item2 fully (20kg, +100), item3 20/30 fraction (+80)
# Maximum value = 240.0

"""
===============================================================================
                         PRACTICAL EXAM EXPLANATION
===============================================================================

PROBLEM STATEMENT:
------------------
Given n items with their profits (values) and weights, and a knapsack with
capacity W, find the maximum profit that can be obtained by selecting items
(or fractions of items) such that:
1. Total weight does not exceed W (capacity constraint)
2. Items CAN be broken into fractions (any fraction from 0 to 1)
3. Goal: Maximize total profit

DIFFERENCE FROM 0/1 KNAPSACK:
------------------------------
┌──────────────────┬─────────────────┬─────────────────────┐
│ Feature          │ Fractional      │ 0/1 Knapsack        │
├──────────────────┼─────────────────┼─────────────────────┤
│ Item Division    │ ALLOWED         │ NOT allowed         │
│ Choice           │ Take any        │ Take all or nothing │
│                  │ fraction [0,1]  │ (binary choice)     │
├──────────────────┼─────────────────┼─────────────────────┤
│ Approach         │ GREEDY          │ Dynamic Programming │
│                  │ Algorithm       │                     │
├──────────────────┼─────────────────┼─────────────────────┤
│ Time Complexity  │ O(n log n)      │ O(n × W)            │
├──────────────────┼─────────────────┼─────────────────────┤
│ Space Complexity │ O(n) or O(1)    │ O(n × W)            │
├──────────────────┼─────────────────┼─────────────────────┤
│ Greedy Works?    │ YES ✓           │ NO ✗                │
│                  │ Optimal         │ Suboptimal          │
└──────────────────┴─────────────────┴─────────────────────┘

WHY GREEDY WORKS FOR FRACTIONAL KNAPSACK:
------------------------------------------
Key Insight: Since we can take fractions, there are no dependencies between
            choices. We can always adjust by taking partial items.

Greedy Choice Property:
- At each step, take as much as possible of the item with highest value density
- This local optimal choice leads to global optimal solution
- We can prove this using "exchange argument"

Proof Sketch (Exchange Argument):
1. Suppose greedy solution G is not optimal
2. Let O be an optimal solution that differs from G
3. Let item i be the first item where G and O differ
4. In G, we took item i (highest ratio remaining)
5. In O, some other item j with lower ratio was taken instead
6. Exchange: Replace portion of j in O with portion of i (same weight)
7. Since ratio(i) > ratio(j), this increases total profit
8. Contradiction: O was supposed to be optimal
9. Therefore, greedy solution must be optimal

GREEDY STRATEGY:
----------------
Greedy Choice: Always select item with MAXIMUM profit/weight ratio

Algorithm:
1. Calculate profit/weight ratio for each item (value density)
2. Sort items by ratio in descending order (highest first)
3. Iterate through sorted items:
   - If item fits completely: take it all
   - If item doesn't fit: take fraction that fills remaining capacity
4. Stop when knapsack is full

Why This Works:
- Maximizes value gained per unit weight consumed
- No dependencies - can always take partial items
- Locally optimal → Globally optimal

ALGORITHM STEPS:
----------------
Input: n items with (profit, weight), knapsack capacity W

Step 1: Calculate Ratios
  For each item i:
    ratio[i] = profit[i] / weight[i]

Step 2: Sort by Ratio
  Sort items by ratio in descending order (highest first)

Step 3: Greedy Selection
  Initialize: totalProfit = 0, remainingCapacity = W

  For each item in sorted order:
    If item.weight ≤ remainingCapacity:
      // Take whole item
      totalProfit += item.profit
      remainingCapacity -= item.weight
    Else:
      // Take fraction to fill remaining capacity
      fraction = remainingCapacity / item.weight
      totalProfit += item.profit × fraction
      Break  // Knapsack is full

Step 4: Return totalProfit

TIME COMPLEXITY ANALYSIS:
-------------------------
1. Calculating ratios: O(n) - one pass through items
2. Sorting by ratio: O(n log n) - comparison-based sorting
3. Selecting items: O(n) - one pass through sorted items

Overall: O(n log n)  ← Dominated by sorting step

This is better than 0/1 Knapsack which requires O(n × W) using DP.

SPACE COMPLEXITY:
-----------------
Method 1 (as in code): O(n)
  - Storing n items in array
  - In-place sorting (no extra array)
  - Few scalar variables (finalValue, w)

Method 2 (if using separate ratio array): O(n)
  - Additional O(n) for storing ratios
  - Still O(n) overall

WORKED EXAMPLE:
---------------
Items:
  Item 1: profit=60,  weight=10  → ratio = 60/10 = 6.0
  Item 2: profit=100, weight=20  → ratio = 100/20 = 5.0
  Item 3: profit=120, weight=30  → ratio = 120/30 = 4.0

Capacity W = 50

Step 1: Calculate Ratios
  Item 1: 6.0  ← Highest ratio
  Item 2: 5.0
  Item 3: 4.0  ← Lowest ratio

Step 2: Sort by Ratio (already sorted)
  Order: Item1, Item2, Item3

Step 3: Greedy Selection
  Remaining capacity = 50
  Total profit = 0

  Process Item 1 (profit=60, weight=10):
    10 ≤ 50? YES → Take whole item
    profit += 60 → profit = 60
    capacity -= 10 → capacity = 40

  Process Item 2 (profit=100, weight=20):
    20 ≤ 40? YES → Take whole item
    profit += 100 → profit = 160
    capacity -= 20 → capacity = 20

  Process Item 3 (profit=120, weight=30):
    30 ≤ 20? NO → Take fraction
    fraction = 20/30 = 2/3
    profit += 120 × (20/30) = 120 × 0.6667 = 80
    profit = 160 + 80 = 240
    capacity = 0 → FULL, stop

Step 4: Final Answer
  Maximum value = 240.0
  Items taken:
    - Item 1: 100% (10 kg, value 60)
    - Item 2: 100% (20 kg, value 100)
    - Item 3: 66.67% (20 kg, value 80)
  Total weight: 50 kg (full capacity used)

ANOTHER EXAMPLE:
----------------
Items:
  Item A: profit=10, weight=2   → ratio = 5.0
  Item B: profit=5,  weight=3   → ratio = 1.67
  Item C: profit=15, weight=5   → ratio = 3.0
  Item D: profit=7,  weight=7   → ratio = 1.0
  Item E: profit=6,  weight=1   → ratio = 6.0  ← Highest

Capacity = 15

After sorting by ratio:
  E(6.0), A(5.0), C(3.0), B(1.67), D(1.0)

Selection:
  1. Take E fully: 1 kg, +6 value, capacity=14
  2. Take A fully: 2 kg, +10 value, capacity=12
  3. Take C fully: 5 kg, +15 value, capacity=7
  4. Take B fully: 3 kg, +5 value, capacity=4
  5. Take D partially: 4/7 of D, +4 value, capacity=0

Maximum value = 6 + 10 + 15 + 5 + 4 = 40

KEY POINTS TO MENTION DURING VIVA:
-----------------------------------
1. Why does greedy work for Fractional but not 0/1 Knapsack?
   → Fractional allows partial items - no dependencies between choices
   → Can always adjust by taking fractions
   → 0/1 has discrete choices - past decisions affect future options
   → Fractional has "greedy choice property" and "optimal substructure"

2. What is the greedy choice here?
   → Always select item with MAXIMUM profit/weight ratio
   → This maximizes value gained per unit weight consumed
   → Local optimum = Global optimum for this problem

3. Why sort by profit/weight ratio, not by profit or weight alone?
   → Profit alone: might take heavy low-value items
   → Weight alone: might take light low-value items
   → Ratio balances both: maximum value per unit weight

4. What if two items have the same ratio?
   → Either order works - both give same total value
   → Can use secondary criteria (prefer lighter item first)
   → Doesn't affect optimality of solution

5. How to prove greedy gives optimal solution?
   → Use "exchange argument" (contradiction proof)
   → Assume optimal solution differs from greedy
   → Show we can improve it by exchanging to greedy choice
   → Contradiction proves greedy must be optimal

6. Can we use Dynamic Programming instead?
   → Yes, but unnecessary - greedy is simpler and faster
   → DP would be O(n × W) vs Greedy O(n log n)
   → When greedy works, prefer it over DP

7. What if items are already sorted by ratio?
   → Skip sorting step
   → Time complexity becomes O(n)
   → Just iterate and pick greedily

8. Real-world applications?
   → Resource allocation (CPU time, memory, bandwidth)
   → Investment portfolio with divisible assets
   → Cutting stock problems (lumber, fabric, paper)
   → Loading cargo with liquid/bulk materials
   → Network bandwidth allocation

PROOF OF CORRECTNESS (Detailed):
---------------------------------
Theorem: Greedy algorithm produces optimal solution for Fractional Knapsack.

Proof by Exchange Argument:

Let G = greedy solution (sorted by ratio, pick highest first)
Let O = some optimal solution

Assume G ≠ O (greedy is not optimal)

Let item i be the FIRST item where G and O differ.
- In G: we took x_i fraction of item i
- In O: we took y_i fraction of item i, where y_i < x_i

Since greedy picks highest ratio first:
- ratio(i) ≥ ratio(j) for all items j picked after i

In O, since we took less of item i, we must have taken more of some other
item j with lower ratio (to use the same total weight).

Exchange Operation:
- Decrease item j in O by weight δ
- Increase item i in O by weight δ
- This maintains total weight constraint

Change in value:
  ΔValue = ratio(i) × δ - ratio(j) × δ
         = (ratio(i) - ratio(j)) × δ
         > 0  (since ratio(i) > ratio(j))

This means we IMPROVED solution O, contradicting that O was optimal.

Therefore, our assumption G ≠ O must be false.
Hence, greedy solution G must be optimal. ∎

COMPARISON: KNAPSACK VARIANTS:
-------------------------------
┌────────────────┬──────────────┬──────────────┬──────────────┐
│ Variant        │ Constraint   │ Approach     │ Complexity   │
├────────────────┼──────────────┼──────────────┼──────────────┤
│ Fractional     │ Continuous   │ Greedy       │ O(n log n)   │
│ Knapsack       │ choice       │ (by ratio)   │              │
├────────────────┼──────────────┼──────────────┼──────────────┤
│ 0/1 Knapsack   │ Binary       │ Dynamic      │ O(n × W)     │
│                │ choice       │ Programming  │              │
├────────────────┼──────────────┼──────────────┼──────────────┤
│ Unbounded      │ Unlimited    │ Dynamic      │ O(n × W)     │
│ Knapsack       │ copies       │ Programming  │              │
├────────────────┼──────────────┼──────────────┼──────────────┤
│ Bounded        │ Limited      │ Dynamic      │ O(n × W × K) │
│ Knapsack       │ copies       │ Programming  │              │
└────────────────┴──────────────┴──────────────┴──────────────┘

SAMPLE OUTPUT:
--------------
Enter number of items-
3
Enter profit of item 1-
60
Enter weight of item 1-
10
Enter profit of item 2-
100
Enter weight of item 2-
20
Enter profit of item 3-
120
Enter weight of item 3-
30
Enter capacity of knapsack-
50
Maximum value in knapsack:  240.0

ANOTHER SAMPLE:
---------------
Enter number of items-
4
Enter profit of item 1-
10
Enter weight of item 1-
2
Enter profit of item 2-
5
Enter weight of item 2-
3
Enter profit of item 3-
15
Enter weight of item 3-
5
Enter profit of item 4-
7
Enter weight of item 4-
7
Enter capacity of knapsack-
10
Maximum value in knapsack:  30.0

Explanation:
  Ratios: 10/2=5.0, 5/3≈1.67, 15/5=3.0, 7/7=1.0
  Sorted: Item1(5.0), Item3(3.0), Item2(1.67), Item4(1.0)
  Take: Item1 fully (2kg, +10), Item3 fully (5kg, +15),
        Item2 fully (3kg, +5), capacity used = 10kg
  Total = 10 + 15 + 5 = 30.0

PRACTICAL EXAM TIPS:
--------------------
✓ Clearly explain the greedy choice (profit/weight ratio)
✓ Show step-by-step calculation of ratios for given items
✓ Demonstrate sorting (before and after)
✓ Trace through greedy selection with remaining capacity
✓ Show both full item and fractional item selection
✓ Mention why greedy works here but not for 0/1 knapsack
✓ Calculate final profit and show which items were selected
✓ Draw a diagram if time permits
✓ Mention time complexity (O(n log n)) and space complexity (O(n))
✓ Be ready to prove optimality using exchange argument
✓ Know real-world applications

COMMON MISTAKES TO AVOID:
--------------------------
✗ Sorting by profit alone (ignoring weight)
✗ Sorting by weight alone (ignoring profit)
✗ Forgetting to calculate profit/weight ratio
✗ Sorting in ascending order (should be descending)
✗ Not breaking loop after taking fraction (wastes iterations)
✗ Claiming greedy works for 0/1 knapsack (it doesn't!)
✗ Forgetting that items can be divided (not binary choice)

ADVANTAGES:
-----------
+ Simple and intuitive algorithm
+ Optimal solution guaranteed
+ Fast: O(n log n) time complexity
+ Low space complexity: O(n) or O(1)
+ Easy to implement
+ Better than DP for this problem variant

DISADVANTAGES:
--------------
- Only works when items are divisible
- Requires sorting (preprocessing step)
- Not applicable to 0/1 knapsack (discrete items)
- Assumes items can be broken arbitrarily (not always realistic)

WHEN TO USE FRACTIONAL VS 0/1:
-------------------------------
Use Fractional Knapsack when:
  → Items are liquids, powders, gases (naturally divisible)
  → Items are bulk materials (sand, grain, oil)
  → Abstract resources (time, bandwidth, money)
  → Problem explicitly allows fractions

Use 0/1 Knapsack when:
  → Items are discrete objects (laptops, books, jewels)
  → Items cannot be meaningfully divided
  → Problem requires whole items only
  → Real-world constraint: all-or-nothing

===============================================================================
"""
