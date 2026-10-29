// ============================================================
// Fibonacci Sequence - Recursive vs Non-Recursive
// ============================================================
// Problem Statement: Write a program to display the Fibonacci
// sequence (Recursive and Non-Recursive)
// ============================================================

#include <iostream>
using namespace std;

// Global variable for recursive step counting
// Tracks how many times recursive function is called
int step_count = 0;

// ── Recursive Fibonacci ────────────────────────────────────
/**
 * Calculates nth Fibonacci number using recursion
 *
 * @param n: Position in Fibonacci sequence (0-indexed)
 * @return: nth Fibonacci number
 *
 * Working:
 * - F(0) = 0, F(1) = 1 (base cases)
 * - F(n) = F(n-1) + F(n-2) (recursive relation)
 * - Each call branches into two more calls (binary recursion tree)
 */
int recursive_fibonacci(int n) {
    step_count++;  // Count each function call for analysis

    // Base cases: F(0) = 0, F(1) = 1
    if (n <= 1) {
        return n;
    } else {
        // Recursive case: F(n) = F(n-1) + F(n-2)
        // This creates exponential number of function calls
        return recursive_fibonacci(n - 1) + recursive_fibonacci(n - 2);
    }
}

// ── Non-Recursive Fibonacci ────────────────────────────────
/**
 * Calculates nth Fibonacci number using iteration
 *
 * @param n: Position in Fibonacci sequence
 * @param steps: Reference parameter to count iterations
 * @return: nth Fibonacci number
 *
 * Working:
 * - Start with F(0)=0 and F(1)=1
 * - Iteratively calculate next number = previous two numbers
 * - Only stores last two values (space efficient)
 */
int non_recursive_fibonacci(int n, int &steps) {
    steps = 0;  // Initialize step counter

    // Base cases: F(0) = 0, F(1) = 1
    if (n <= 1) {
        return n;
    }

    // Initialize first two Fibonacci numbers
    int first = 0;   // F(0)
    int second = 1;  // F(1)
    steps++;         // Count initialization as one step

    // Calculate Fibonacci numbers iteratively from F(2) to F(n)
    for (int i = 2; i <= n; i++) {
        int third = first + second;  // F(i) = F(i-1) + F(i-2)
        first = second;              // Slide window: update F(i-2)
        second = third;              // Slide window: update F(i-1)
        steps++;                     // Count one step per iteration
    }

    return second;  // second now holds F(n)
}

// ── Main ───────────────────────────────────────────────────
int main() {
    int n;
    cout << "Enter n: ";
    cin >> n;

    // ── Test Non-Recursive Approach ──
    int steps_iter = 0;  // Variable to store iteration count
    int fib_iter = non_recursive_fibonacci(n, steps_iter);
    cout << "\nNon-Recursive: F(" << n << ") = " << fib_iter
         << ", Steps = " << steps_iter << endl;

    // ── Test Recursive Approach ──
    step_count = 0;  // Reset global counter before recursive call
    int fib_rec = recursive_fibonacci(n);
    cout << "Recursive: F(" << n << ") = " << fib_rec
         << ", Steps = " << step_count << endl;

    return 0;
}

/*
============================================================
TIME AND SPACE COMPLEXITY ANALYSIS:
============================================================

Recursive Fibonacci:
- Time Complexity: O(2^n) - exponential growth
  * Each call spawns 2 more calls → binary tree of calls
  * For F(n), approximately 2^n function calls are made
  * Example: F(5) makes 15 calls, F(10) makes 177 calls

- Space Complexity: O(n) - recursion stack depth
  * Maximum depth of recursion tree = n
  * At any point, call stack has at most n frames

Non-Recursive Fibonacci:
- Time Complexity: O(n) - linear growth
  * Single loop runs n-1 times
  * Each iteration does constant work

- Space Complexity: O(1) - constant space
  * Only uses 3 variables (first, second, third)
  * No recursion stack needed

COMPARISON:
Non-recursive is MUCH more efficient:
- For n=30: Recursive makes ~2 million calls vs 29 iterations
- For n=40: Recursive makes ~2 billion calls vs 39 iterations
*/

// ============================================================
// PRACTICAL EXAM EXPLANATION
// ============================================================

/*
📚 FIBONACCI SEQUENCE CONCEPT:
------------------------------
The Fibonacci sequence is: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

Mathematical Definition:
- F(0) = 0 (base case)
- F(1) = 1 (base case)
- F(n) = F(n-1) + F(n-2) for n ≥ 2 (recursive relation)

Real-world applications:
- Nature patterns (sunflower spirals, pinecones)
- Algorithm analysis
- Financial modeling
- Computer graphics

🔧 TWO APPROACHES:
------------------

1️⃣ RECURSIVE APPROACH:
   ✓ Simple and elegant code
   ✓ Directly mirrors mathematical definition
   ✗ Extremely inefficient (exponential time)
   ✗ Repeated calculations (overlapping subproblems)
   ✗ Stack overflow risk for large n

2️⃣ NON-RECURSIVE (ITERATIVE) APPROACH:
   ✓ Very efficient (linear time)
   ✓ Constant space usage
   ✓ No stack overflow risk
   ✓ Can handle large values of n
   ✗ Slightly more code than recursive

📊 EXAMPLE WALKTHROUGH FOR n=5:
-------------------------------

NON-RECURSIVE:
Step 1: Initialize first=0, second=1
Step 2: i=2 → third = 0+1 = 1, shift → first=1, second=1
Step 3: i=3 → third = 1+1 = 2, shift → first=1, second=2
Step 4: i=4 → third = 1+2 = 3, shift → first=2, second=3
Step 5: i=5 → third = 2+3 = 5, shift → first=3, second=5
Result: F(5) = 5, Steps = 5

RECURSIVE:
Call tree for F(5):
                    F(5)
                   /    \
               F(4)      F(3)
              /   \      /   \
          F(3)   F(2)  F(2) F(1)
         /  \    / \   / \
      F(2) F(1) F(1) F(0) F(1) F(0)
      / \
   F(1) F(0)

Total calls = 15 (Notice F(3) calculated twice, F(2) thrice!)
Result: F(5) = 5, Steps = 15

⏱️ PERFORMANCE COMPARISON:
--------------------------
n    | Recursive Calls | Iterative Steps | Ratio
-----|-----------------|-----------------|--------
5    |       15        |        5        |  3.0x
10   |      177        |       10        | 17.7x
20   |    21,891       |       20        | 1094x
30   | 2,692,537       |       30        | 89,751x

Observation: As n increases, recursive becomes EXTREMELY slow!

💡 WHY RECURSIVE IS SLOW:
-------------------------
Problem: OVERLAPPING SUBPROBLEMS
- F(5) needs F(4) and F(3)
- F(4) needs F(3) and F(2)
- F(3) is calculated TWICE
- F(2) is calculated THREE times
- Exponential redundant calculations!

Solution: Use iterative approach OR memoization/dynamic programming

🎓 EXAM TIPS:
-------------
1. Start with Fibonacci definition: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)

2. For Recursive:
   - Draw call tree for small n (like n=4 or n=5)
   - Show overlapping subproblems
   - Explain exponential time O(2^n)

3. For Non-Recursive:
   - Show sliding window technique (3 variables)
   - Trace through 3-4 iterations
   - Explain linear time O(n) and constant space O(1)

4. Comparison:
   - Show step counts for same n
   - Highlight efficiency difference
   - Mention when to use each approach

🔑 KEY POINTS TO REMEMBER:
--------------------------
✓ Recursive: Simple code BUT exponentially slow
✓ Iterative: Slightly complex BUT extremely fast
✓ Recursive makes redundant calculations
✓ Iterative uses sliding window (3 variables)
✓ For large n (>30), only iterative is practical
✓ Step count clearly shows efficiency difference

❓ COMMON EXAM QUESTIONS:
-------------------------
Q1: Which is better - recursive or iterative?
A: Iterative is MUCH better for efficiency. Recursive is only good
   for understanding the mathematical concept.

Q2: Why is recursive Fibonacci so slow?
A: Because of overlapping subproblems - it recalculates the same
   values multiple times (exponential redundancy).

Q3: Can we improve recursive approach?
A: Yes! Use memoization (store calculated values) or convert to
   dynamic programming - reduces time to O(n).

Q4: What is time complexity of recursive Fibonacci?
A: O(2^n) - exponential. Each call spawns 2 more calls.

Q5: What is space complexity of iterative Fibonacci?
A: O(1) - constant space. Only uses 3 variables regardless of n.

Q6: For n=40, which approach should you use?
A: ONLY iterative! Recursive would take hours/days to complete.

Q7: What is the space complexity of recursive approach?
A: O(n) due to recursion call stack depth.

📝 SAMPLE OUTPUT EXPLANATION:
------------------------------
Input: n = 10

Non-Recursive: F(10) = 55, Steps = 10
→ Iterates 10 times, calculates each number once

Recursive: F(10) = 55, Steps = 177
→ Makes 177 function calls due to redundant calculations

Both get correct answer (55) but recursive is 17.7x slower!

🎯 WHAT TO WRITE IN EXAM:
--------------------------
1. Problem statement
2. Mathematical definition of Fibonacci
3. Both code implementations with comments
4. Trace execution for small n (like n=5)
5. Time and space complexity analysis
6. Comparison table showing step counts
7. Conclusion: Iterative is more efficient
8. Mention: Recursive can be improved with memoization

*/
