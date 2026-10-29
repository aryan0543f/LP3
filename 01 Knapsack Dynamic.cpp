// ============================================================
// 0-1 Knapsack - Dynamic Programming (Tabulation)
// ============================================================
// Assignment 4: Write a program to solve a 0-1 Knapsack problem
// using dynamic programming
// ============================================================

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 0-1 Knapsack - Dynamic Programming (Tabulation)
/**
 * Solves 0-1 knapsack using bottom-up DP approach
 *
 * @param capacity: Maximum weight the knapsack can hold
 * @param weights: Vector of item weights
 * @param values: Vector of item values
 * @param n: Number of items
 * @return: Maximum value achievable
 *
 * DP State Definition:
 * dp[i][w] = maximum value using first i items with capacity w
 *
 * Recurrence Relation:
 * If weight[i-1] <= w:
 *     dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]],  // Include item
 *                    dp[i-1][w])                              // Exclude item
 * Else:
 *     dp[i][w] = dp[i-1][w]  // Can't include (too heavy)
 *
 * Base Case:
 * dp[0][w] = 0 for all w (no items, profit = 0)
 * dp[i][0] = 0 for all i (no capacity, profit = 0)
 */
int knapsack(int capacity, vector<int>& weights, vector<int>& values, int n) {
    // Create DP table: dp[i][w] = max value using first i items with capacity w
    // Dimensions: (n+1) x (capacity+1)
    // Extra row/column for base case (0 items or 0 capacity)
    vector<vector<int>> dp(n + 1, vector<int>(capacity + 1, 0));

    // Fill the DP table in bottom-up manner
    // i = number of items considered (1 to n)
    // w = capacity being considered (1 to capacity)
    for (int i = 1; i <= n; i++) {
        for (int w = 1; w <= capacity; w++) {
            // Check if current item can fit in current capacity
            if (weights[i - 1] <= w) {
                // Item fits! We have two choices:

                // Choice 1: INCLUDE current item
                // Value = value of current item + best value from remaining capacity
                // Remaining capacity = w - weight of current item
                // Use previous items (i-1) for remaining capacity
                int includeItem = values[i - 1] + dp[i - 1][w - weights[i - 1]];

                // Choice 2: EXCLUDE current item
                // Value = best value without using current item
                // Same capacity but only using first (i-1) items
                int excludeItem = dp[i - 1][w];

                // Take maximum of both choices (optimal substructure)
                dp[i][w] = max(includeItem, excludeItem);
            } else {
                // Item too heavy - cannot include it
                // Only option: exclude current item
                // Copy value from previous row (same capacity, one less item)
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    // Return maximum value achievable with n items and given capacity
    // Bottom-right cell contains the final answer
    return dp[n][capacity];
}

int main() {
    int n;
    cout << "Enter number of items: ";
    cin >> n;

    vector<int> values(n);   // Vector to store item values
    vector<int> weights(n);  // Vector to store item weights

    // Input: values of all items
    cout << "Enter values of items:\n";
    for (int i = 0; i < n; i++) {
        cout << "Item " << i + 1 << " value: ";
        cin >> values[i];
    }

    // Input: weights of all items
    cout << "Enter weights of items:\n";
    for (int i = 0; i < n; i++) {
        cout << "Item " << i + 1 << " weight: ";
        cin >> weights[i];
    }

    // Input: knapsack capacity
    int capacity;
    cout << "Enter knapsack capacity: ";
    cin >> capacity;

    // Solve using Dynamic Programming
    int maxProfit = knapsack(capacity, weights, values, n);

    // Display result
    cout << "\nMaximum Profit = " << maxProfit << endl;

    return 0;
}

/*
============================================================
EXAMPLE INPUT/OUTPUT:
============================================================
Enter number of items: 3
Enter values of items:
Item 1 value: 60
Item 2 value: 100
Item 3 value: 120
Enter weights of items:
Item 1 weight: 10
Item 2 weight: 20
Item 3 weight: 30
Enter knapsack capacity: 50

Maximum Profit = 220

Solution: Items 2 and 3 (weights: 20+30=50, values: 100+120=220)

============================================================
HOW DYNAMIC PROGRAMMING WORKS:
============================================================
- dp[i][w] = maximum value using first i items with capacity w
- For each item, we have two choices:
  1. Include it (if it fits): value[i] + dp[i-1][w-weight[i]]
  2. Exclude it: dp[i-1][w]
- Take the maximum of both choices

Key Principles:
1. Overlapping Subproblems: Same subproblems solved multiple times
2. Optimal Substructure: Optimal solution contains optimal solutions to subproblems
3. Memoization: Store results to avoid recomputation

============================================================
COMPLEXITY ANALYSIS:
============================================================
Time Complexity: O(n × capacity)
- Two nested loops: n items × capacity values
- Each cell computed in O(1) time

Space Complexity: O(n × capacity)
- 2D DP table of size (n+1) × (capacity+1)
- Can be optimized to O(capacity) using 1D array
*/

// ============================================================
// PRACTICAL EXAM EXPLANATION
// ============================================================

/*
📚 0-1 KNAPSACK - DYNAMIC PROGRAMMING CONCEPT:
----------------------------------------------
Problem Type: Optimization problem (NP-hard)

Given:
- N items, each with value V[i] and weight W[i]
- Knapsack with capacity C
- Each item can be taken ONCE (0 or 1 times)

Goal:
- Maximize total value
- Stay within capacity constraint
- Cannot take fractions of items

Why Dynamic Programming?
- Exhibits optimal substructure
- Has overlapping subproblems
- Can be solved efficiently using DP

🎯 KEY DP CONCEPTS:
-------------------
1. STATE DEFINITION:
   dp[i][w] = maximum value achievable using:
   - First i items (items 0 to i-1)
   - With knapsack capacity w

2. RECURRENCE RELATION:
   For item i with weight W[i] and value V[i]:

   If W[i] <= w:  (item can fit)
       dp[i][w] = max(
           V[i] + dp[i-1][w-W[i]],  // Include item i
           dp[i-1][w]                // Exclude item i
       )

   Else:  (item too heavy)
       dp[i][w] = dp[i-1][w]  // Must exclude item i

3. BASE CASES:
   dp[0][w] = 0 for all w  (no items → zero value)
   dp[i][0] = 0 for all i  (no capacity → zero value)

4. FINAL ANSWER:
   dp[n][capacity] = maximum value with all n items and full capacity

🔧 ALGORITHM EXPLANATION:
-------------------------
Step 1: Create DP table of size (n+1) × (capacity+1)
        Initialize all cells to 0 (base cases)

Step 2: Fill table row by row (item by item)
        For each item i (1 to n):
            For each capacity w (1 to capacity):
                If item i fits in capacity w:
                    Compare including vs excluding
                    Take maximum
                Else:
                    Must exclude (copy from previous row)

Step 3: Return dp[n][capacity] as final answer

📊 DETAILED EXAMPLE WALKTHROUGH:
--------------------------------
Input:
Item 1: value=60,  weight=10
Item 2: value=100, weight=20
Item 3: value=120, weight=30
Capacity: 50

DP Table Construction:

Capacity →  0    10   20   30   40   50
Items ↓
0 (none)    0    0    0    0    0    0
1 (I1)      0   60   60   60   60   60
2 (I1,I2)   0   60  100  160  160  160
3 (all)     0   60  100  160  180  220

Detailed Filling Process:

Row 0: Base case - no items, all values = 0

Row 1 (Item 1: w=10, v=60):
- dp[1][10] = max(60+dp[0][0], dp[0][10]) = max(60, 0) = 60
- dp[1][20] = max(60+dp[0][10], dp[0][20]) = max(60, 0) = 60
- dp[1][30] = max(60+dp[0][20], dp[0][30]) = max(60, 0) = 60
- ... all = 60 (only one item fits)

Row 2 (Item 2: w=20, v=100):
- dp[2][10] = dp[1][10] = 60 (Item 2 too heavy)
- dp[2][20] = max(100+dp[1][0], dp[1][20]) = max(100, 60) = 100
- dp[2][30] = max(100+dp[1][10], dp[1][30]) = max(160, 60) = 160
- dp[2][40] = max(100+dp[1][20], dp[1][40]) = max(160, 60) = 160
- dp[2][50] = max(100+dp[1][30], dp[1][50]) = max(160, 60) = 160

Row 3 (Item 3: w=30, v=120):
- dp[3][10] = dp[2][10] = 60 (Item 3 too heavy)
- dp[3][20] = dp[2][20] = 100 (Item 3 too heavy)
- dp[3][30] = max(120+dp[2][0], dp[2][30]) = max(120, 160) = 160
- dp[3][40] = max(120+dp[2][10], dp[2][40]) = max(180, 160) = 180
- dp[3][50] = max(120+dp[2][20], dp[2][50]) = max(220, 160) = 220 ✓

Final Answer: dp[3][50] = 220

Items Included: Item 2 (100) + Item 3 (120) = 220
Total Weight: 20 + 30 = 50 ≤ 50 ✓

💡 WHY DYNAMIC PROGRAMMING WORKS:
---------------------------------
1. OPTIMAL SUBSTRUCTURE:
   - Optimal solution to problem contains optimal solutions to subproblems
   - If items {i1, i2, ..., ik} are optimal for capacity C,
     then {i1, i2, ..., i(k-1)} are optimal for capacity C-W[ik]

2. OVERLAPPING SUBPROBLEMS:
   - Same subproblems appear multiple times in recursion tree
   - Example: dp[2][20] might be needed for dp[3][30] and dp[3][40]
   - Storing results avoids recomputation

3. BOTTOM-UP APPROACH:
   - Solve smaller subproblems first
   - Build up to larger problems using stored results
   - Guarantees all dependencies are computed before use

🔑 KEY POINTS TO REMEMBER:
--------------------------
✓ DP table: (n+1) × (capacity+1) dimensions
✓ State: dp[i][w] = max value with i items, capacity w
✓ Decision: Include or exclude each item
✓ Choice: Take maximum of both options
✓ Base case: Zero items or zero capacity = zero value
✓ Bottom-up: Fill table row by row
✓ Time: O(n × capacity), Space: O(n × capacity)
✓ Guaranteed optimal solution

⏱️ COMPLEXITY COMPARISON:
-------------------------
Approach          | Time           | Space      | Optimal?
------------------|----------------|------------|----------
Brute Force       | O(2^n)         | O(1)       | Yes
Branch & Bound    | O(2^n) best    | O(n)       | Yes
Dynamic Prog      | O(n × C)       | O(n × C)   | Yes
Greedy            | O(n log n)     | O(1)       | NO!

DP is best when:
- Capacity is reasonable (not too large)
- Need guaranteed optimal solution
- Can afford O(n × C) space

🎓 EXAM TIPS:
-------------
1. START with state definition
   - Clearly define what dp[i][w] represents

2. WRITE recurrence relation
   - Show both choices (include/exclude)
   - Explain max() selection

3. DRAW the DP table
   - Show at least a 4×4 example
   - Fill step by step

4. TRACE one cell calculation
   - Pick dp[2][30] or similar
   - Show both options computed
   - Show why max is chosen

5. MENTION base cases
   - dp[0][w] = 0 and dp[i][0] = 0

6. STATE complexity clearly
   - Time: O(n × capacity)
   - Space: O(n × capacity)

7. COMPARE with other approaches briefly

📋 EXAM TABLE FORMAT:
---------------------
        Capacity →
Items ↓   0   10   20   30   40   50
  0       0    0    0    0    0    0
  1       0   60   60   60   60   60
  2       0   60  100  160  160  160
  3       0   60  100  160  180  220

Trace for dp[3][50]:
- Include Item 3: 120 + dp[2][50-30] = 120 + dp[2][20] = 120 + 100 = 220 ✓
- Exclude Item 3: dp[2][50] = 160
- Maximum: max(220, 160) = 220

❓ COMMON EXAM QUESTIONS:
-------------------------
Q1: What is the state definition in 0-1 knapsack DP?
A: dp[i][w] = maximum value achievable using first i items with capacity w.

Q2: What is the recurrence relation?
A: If weight[i] ≤ w:
       dp[i][w] = max(value[i] + dp[i-1][w-weight[i]], dp[i-1][w])
   Else:
       dp[i][w] = dp[i-1][w]

Q3: Why is it called "0-1" knapsack?
A: Because each item can be taken 0 times or 1 time (not multiple times,
   not fractions). It's a binary choice for each item.

Q4: What are the base cases?
A: dp[0][w] = 0 for all w (no items)
   dp[i][0] = 0 for all i (no capacity)

Q5: Time complexity?
A: O(n × capacity) where n is number of items.
   Two nested loops, each cell computed in O(1).

Q6: Can we optimize space?
A: Yes! Can use 1D array of size (capacity+1), updating in reverse order.
   Space becomes O(capacity) instead of O(n × capacity).

Q7: How to find which items were selected?
A: Backtrack through DP table. If dp[i][w] != dp[i-1][w], item i was included.
   Move to dp[i-1][w-weight[i]] and repeat.

Q8: Difference from fractional knapsack?
A: 0-1: Cannot take fractions, needs DP, optimal substructure
   Fractional: Can take fractions, greedy works, simpler

Q9: Why not use greedy for 0-1 knapsack?
A: Greedy (by ratio) doesn't guarantee optimal for 0-1 knapsack.
   Example: capacity=50, items: (60,10), (100,50), (120,50)
   Greedy picks (60,10) first, misses optimal (100,50).

Q10: Is 0-1 knapsack NP-hard?
A: Yes, it's NP-hard. DP is pseudo-polynomial (depends on capacity value).
   For very large capacity, becomes exponential in input size.

🎯 WHAT TO WRITE IN EXAM:
--------------------------
1. Problem statement
2. DP approach explanation
3. State definition: dp[i][w]
4. Recurrence relation (with both cases)
5. Base cases
6. Complete code with comments
7. DP table example (fill 4×5 table)
8. Trace one cell calculation
9. Time complexity: O(n × C)
10. Space complexity: O(n × C)
11. Brief comparison with other approaches

💻 CODE WALKTHROUGH FOR EXAM:
------------------------------
1. Function knapsack():
   - Create 2D DP table (n+1) × (capacity+1)
   - Initialize all to 0 (base cases)
   - Fill table row by row, column by column
   - For each cell: check if item fits
   - If fits: max(include, exclude)
   - If doesn't fit: exclude (copy from above)
   - Return dp[n][capacity]

2. Main():
   - Input n items (values and weights)
   - Input capacity
   - Call knapsack()
   - Display maximum profit

Key insight: Build solution bottom-up using subproblem results

🌟 PRACTICAL APPLICATIONS:
--------------------------
• Resource allocation with constraints
• Budget optimization
• Cargo loading
• Investment portfolio selection
• Project selection
• Memory management
• Cutting stock problem
• Subset sum problems

✅ EXAM CHECKLIST:
------------------
□ Define dp[i][w] clearly
□ Write recurrence relation correctly
□ Show both cases (fits / doesn't fit)
□ Mention base cases
□ Draw DP table with example
□ Trace at least one cell
□ State time: O(n × C)
□ State space: O(n × C)
□ Explain why DP works (optimal substructure)
□ Compare briefly with greedy (doesn't work)
□ Write clean, commented code
*/
