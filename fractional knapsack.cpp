// ============================================================
// Fractional Knapsack - Greedy Algorithm
// ============================================================
// Problem Statement: Given a set of N items each having value V with weight W
// and the total capacity of a knapsack. The task is to find the maximal value
// of fractions of items that can fit into the knapsack.
// ============================================================

#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
using namespace std;

// Structure to represent an item
struct Item {
    int profit;     // Value/Profit of the item
    int weight;     // Weight of the item
    double ratio;   // Profit per unit weight (profit/weight ratio)

    // Constructor to initialize an item
    Item(int p, int w) {
        profit = p;
        weight = w;
        ratio = (double)p / w;  // Calculate profit-to-weight ratio
    }
};

// Comparator function to sort by profit/weight ratio (highest first)
// Used by sort() to arrange items in descending order of ratio
bool compare(Item a, Item b) {
    return a.ratio > b.ratio;  // Higher ratio comes first
}

// Fractional Knapsack - Greedy Method
/**
 * Greedy Strategy: Always pick the item with highest profit/weight ratio
 *
 * @param capacity: Maximum weight the knapsack can hold
 * @param items: Vector of items with profit, weight, and ratio
 * @return: Maximum profit achievable
 *
 * Process:
 * 1. Sort items by profit/weight ratio (descending)
 * 2. Pick items with highest ratio first
 * 3. If item fits completely, take it fully
 * 4. If item doesn't fit, take fraction that fits
 * 5. Stop when knapsack is full
 */
double fractionalKnapsack(int capacity, vector<Item>& items) {
    // Sort by profit/weight ratio (highest first) - GREEDY CHOICE
    // Items with better ratio give more profit per unit weight
    sort(items.begin(), items.end(), compare);

    double total_value = 0.0;  // Accumulated profit

    // Iterate through sorted items (highest ratio first)
    for (int i = 0; i < items.size(); i++) {
        if (capacity >= items[i].weight) {
            // Case 1: Item fits completely in remaining capacity
            // Take the whole item
            total_value += items[i].profit;
            capacity -= items[i].weight;  // Reduce remaining capacity
        } else {
            // Case 2: Item doesn't fit completely
            // Take fraction of the item that fits
            // Fraction = remaining_capacity / item_weight
            // Profit from fraction = profit × fraction
            total_value += items[i].profit * ((double)capacity / items[i].weight);
            break;  // Knapsack is now full, stop
        }
    }

    return total_value;
}

// ── Main ───────────────────────────────────────────────────
int main() {
    int n;
    cout << "Enter number of items: ";
    cin >> n;

    vector<Item> items;  // Vector to store all items

    // Input: Take profit and weight for each item
    for (int i = 0; i < n; i++) {
        int profit, weight;
        cout << "Item " << (i + 1) << " profit: ";
        cin >> profit;
        cout << "Item " << (i + 1) << " weight: ";
        cin >> weight;
        items.push_back(Item(profit, weight));  // Create item and add to vector
    }

    int capacity;
    cout << "Enter knapsack capacity: ";
    cin >> capacity;

    // Calculate maximum value using fractional knapsack
    double max_value = fractionalKnapsack(capacity, items);

    // Display result with 2 decimal places
    cout << fixed << setprecision(2);
    cout << "\nMaximum value: " << max_value << endl;

    return 0;
}

/*
============================================================
EXAMPLE OUTPUT:
============================================================
Enter number of items: 3
Item 1 profit: 60
Item 1 weight: 10
Item 2 profit: 100
Item 2 weight: 20
Item 3 profit: 120
Item 3 weight: 30
Enter knapsack capacity: 50

Maximum value: 240.00

============================================================
COMPLEXITY ANALYSIS:
============================================================
Time Complexity: O(n log n) due to sorting
- Sorting: O(n log n)
- Single pass through items: O(n)
- Total: O(n log n) [dominated by sorting]

Space Complexity: O(n) for storing items
- Vector of n items
- No additional data structures needed

============================================================
GREEDY STRATEGY:
============================================================
1. Calculate profit/weight ratio for each item
2. Sort items by ratio in descending order (highest first)
3. Take items with highest ratio first (greedy choice)
4. If an item doesn't fit completely, take its fraction
5. This ensures maximum profit per unit weight used
*/

// ============================================================
// PRACTICAL EXAM EXPLANATION
// ============================================================

/*
📚 FRACTIONAL KNAPSACK CONCEPT:
--------------------------------
Given:
- N items, each with profit P[i] and weight W[i]
- Knapsack with capacity C
- Can take FRACTIONS of items (key difference from 0-1 knapsack)

Goal:
- Maximize total profit while staying within capacity
- Can take 0 ≤ fraction ≤ 1 of each item

Real-world examples:
- Loading cargo (can break items)
- Filling containers with liquids/grains
- Resource allocation with divisible resources

🎯 GREEDY STRATEGY:
-------------------
Key Insight: Items with higher profit/weight ratio give more value!

Greedy Choice:
- Always pick item with HIGHEST profit/weight ratio first
- If it fits completely, take all of it
- If it doesn't fit, take fraction that fits
- Continue until knapsack is full

Why Greedy Works:
- Each unit of weight should contribute maximum profit
- Ratio = profit per unit weight
- Taking highest ratio first maximizes total profit

🔧 ALGORITHM STEPS:
-------------------
Step 1: For each item i, calculate ratio[i] = profit[i] / weight[i]

Step 2: Sort items by ratio in DESCENDING order
        → Item with highest ratio comes first

Step 3: Initialize total_value = 0, remaining_capacity = C

Step 4: For each item (in sorted order):
        IF item.weight ≤ remaining_capacity:
           - Take WHOLE item
           - total_value += item.profit
           - remaining_capacity -= item.weight
        ELSE:
           - Take FRACTION of item
           - fraction = remaining_capacity / item.weight
           - total_value += item.profit × fraction
           - BREAK (knapsack is full)

Step 5: Return total_value

📊 DETAILED EXAMPLE WALKTHROUGH:
--------------------------------
Input:
Items:
  Item 1: profit=60, weight=10
  Item 2: profit=100, weight=20
  Item 3: profit=120, weight=30
Capacity: 50

Step 1: Calculate ratios
  Item 1: ratio = 60/10 = 6.0
  Item 2: ratio = 100/20 = 5.0
  Item 3: ratio = 120/30 = 4.0

Step 2: Sort by ratio (descending)
  Sorted: Item1(6.0), Item2(5.0), Item3(4.0)

Step 3: Fill knapsack greedily

  Iteration 1 - Item 1 (profit=60, weight=10, ratio=6.0):
    - Remaining capacity = 50
    - Item weight = 10
    - 10 ≤ 50? YES → Take WHOLE item
    - total_value = 0 + 60 = 60
    - remaining_capacity = 50 - 10 = 40

  Iteration 2 - Item 2 (profit=100, weight=20, ratio=5.0):
    - Remaining capacity = 40
    - Item weight = 20
    - 20 ≤ 40? YES → Take WHOLE item
    - total_value = 60 + 100 = 160
    - remaining_capacity = 40 - 20 = 20

  Iteration 3 - Item 3 (profit=120, weight=30, ratio=4.0):
    - Remaining capacity = 20
    - Item weight = 30
    - 30 ≤ 20? NO → Take FRACTION
    - fraction = 20/30 = 0.667 (2/3 of item)
    - profit from fraction = 120 × (20/30) = 80
    - total_value = 160 + 80 = 240
    - remaining_capacity = 0
    - STOP (knapsack full)

Final Answer: Maximum value = 240.00

Summary:
- Took 100% of Item 1 (profit 60)
- Took 100% of Item 2 (profit 100)
- Took 66.7% of Item 3 (profit 80)
- Total weight used = 10 + 20 + 20 = 50 ✓
- Total profit = 240 ✓

💡 WHY GREEDY IS OPTIMAL:
-------------------------
Proof Intuition:
1. Every unit of weight should give maximum possible profit
2. Ratio = profit per unit weight
3. Taking highest ratio first maximizes profit per unit
4. If we swap any item with lower ratio item, profit decreases
5. Therefore, greedy choice is optimal

Exchange Argument:
- Suppose optimal solution doesn't follow greedy order
- Swap items to match greedy order
- This increases (or maintains) total profit
- Contradiction! Therefore greedy is optimal

🔑 KEY DIFFERENCES: FRACTIONAL vs 0-1 KNAPSACK:
------------------------------------------------
Fractional Knapsack:
✓ Can take fractions of items
✓ GREEDY approach works
✓ Time: O(n log n)
✓ Always gets optimal solution
✓ Easier problem

0-1 Knapsack:
✗ Cannot take fractions (all or nothing)
✗ Greedy DOESN'T work
✓ Needs Dynamic Programming
✓ Time: O(n × capacity)
✗ NP-hard problem

⏱️ STEP-BY-STEP COMPLEXITY:
---------------------------
1. Input n items: O(n)
2. Calculate ratios: O(n) [done in constructor]
3. Sort by ratio: O(n log n) [merge sort/quick sort]
4. Iterate through items: O(n)
5. Total: O(n) + O(n log n) + O(n) = O(n log n)

Dominant term: Sorting O(n log n)

🎓 EXAM TIPS:
-------------
1. START by explaining greedy strategy
   - "Always pick highest profit/weight ratio first"

2. CALCULATE ratios clearly
   - Show ratio = profit/weight for each item

3. SORT items by ratio (show sorted order)

4. ITERATE through sorted items
   - Show capacity remaining at each step
   - Indicate when taking whole vs fraction

5. DRAW a table showing the process

6. MENTION time complexity: O(n log n)

7. COMPARE with 0-1 knapsack briefly

📋 EXAM TABLE FORMAT:
---------------------
Item | Profit | Weight | Ratio | Action        | Profit Gained | Capacity Left
-----|--------|--------|-------|---------------|---------------|---------------
1    | 60     | 10     | 6.0   | Take all      | 60            | 40
2    | 100    | 20     | 5.0   | Take all      | 100           | 20
3    | 120    | 30     | 4.0   | Take 20/30    | 80            | 0
-----|--------|--------|-------|---------------|---------------|---------------
                                Total Profit:    240

❓ COMMON EXAM QUESTIONS:
-------------------------
Q1: Why is greedy approach optimal for fractional knapsack?
A: Because we can take fractions. Always taking highest ratio maximizes
   profit per unit weight. This greedy choice leads to global optimum.

Q2: Does greedy work for 0-1 knapsack?
A: NO! When we can't take fractions, greedy may not be optimal.
   Example: capacity=50, items: (60,10), (100,50), (120,50)
   Greedy picks first item, gets 60. Optimal is picking second, gets 100.

Q3: Time complexity?
A: O(n log n) due to sorting. If items were pre-sorted, O(n).

Q4: What if two items have same ratio?
A: Doesn't matter which is picked first - both give same value per unit.
   Either order produces same optimal result.

Q5: Can we use other sorting algorithms?
A: Yes! Any O(n log n) algorithm works: merge sort, heap sort, quick sort.

Q6: What if capacity is 0?
A: Maximum value = 0 (can't take any items).

Q7: What if all items fit completely?
A: Take all items, no fractions needed. Total profit = sum of all profits.

Q8: Space complexity?
A: O(n) for storing n items in vector.

Q9: Is this problem NP-hard?
A: NO! Fractional knapsack is polynomial time O(n log n).
   Only 0-1 knapsack is NP-hard.

Q10: Real-world applications?
A: Loading cargo ships, resource allocation, investment portfolios,
   bandwidth allocation, any scenario with divisible resources.

🎯 WHAT TO WRITE IN EXAM:
--------------------------
1. Problem statement (copy from question)
2. Concept: Fractional knapsack with greedy approach
3. Greedy strategy explanation
4. Algorithm steps (numbered clearly)
5. Complete code with comments
6. Example walkthrough (use table format)
7. Why greedy is optimal (brief proof)
8. Time & space complexity
9. Difference from 0-1 knapsack
10. Conclusion

💻 CODE EXPLANATION FOR EXAM:
------------------------------
1. Item struct: Stores profit, weight, and calculates ratio

2. compare(): Comparator for sorting by ratio (descending)

3. fractionalKnapsack():
   - Sort items by ratio (greedy choice)
   - Loop through items
   - Take whole item if fits, else take fraction
   - Return total value

4. Main:
   - Input items and capacity
   - Call fractionalKnapsack()
   - Display result

Key insight: One-pass greedy selection after sorting

🌟 EXAM PRESENTATION STRATEGY:
------------------------------
• Start with clear problem statement
• Explain greedy intuition first
• Show ratio calculation
• Draw table for example
• Write clean, commented code
• Analyze complexity
• Compare with 0-1 knapsack
• Conclude with optimality

✅ CHECKLIST FOR EXAM:
----------------------
□ Define problem clearly
□ Explain greedy strategy
□ Show ratio calculation formula
□ Sort items by ratio
□ Work through complete example with table
□ Write well-commented code
□ Mention time: O(n log n)
□ Mention space: O(n)
□ Explain why greedy works
□ Compare with 0-1 knapsack
□ State real-world applications
*/
