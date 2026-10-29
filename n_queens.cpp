// ============================================================
// N-Queens Problem - Backtracking with First Queen Pre-placed
// ============================================================
// Problem Statement: Design 8-Queens matrix having first Queen
// placed. Use backtracking to place remaining Queens to generate
// the final 8-queen's matrix.
// ============================================================

#include <iostream>
#include <vector>
#include <set>
using namespace std;

// Global variables
int n = 8;  // Board size (8x8 for standard 8-Queens problem)

// 2D vector representing the chessboard ('Q' for queen, '.' for empty)
vector<vector<char>> board;

// Sets to track attacked positions (for O(1) lookup)
set<int> col;       // Columns that have queens (blocks entire column)
set<int> posDiag;   // Positive diagonals (r+c constant for each diagonal)
set<int> negDiag;   // Negative diagonals (r-c constant for each diagonal)

// Function to print the current board configuration
/**
 * Displays the 8x8 chessboard
 * 'Q' represents a queen, '.' represents an empty cell
 */
void printBoard() {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << board[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;
}

// Backtracking function to place queens
/**
 * Recursively places queens row by row using backtracking
 *
 * @param r: Current row being processed
 * @param first_row: Row where first queen is pre-placed (skip this row)
 * @return: true if solution found, false otherwise
 *
 * Algorithm:
 * 1. Try placing queen in each column of current row
 * 2. Check if position is safe (not attacked)
 * 3. If safe, place queen and recurse to next row
 * 4. If recursion fails, backtrack (remove queen, try next column)
 * 5. If all rows filled successfully, solution found
 */
bool backtrack(int r, int first_row) {
    // Base case: All rows processed successfully
    if (r == n) {
        printBoard();  // Display solution
        return true;   // Solution found
    }

    // Skip the row where first queen is already placed
    if (r == first_row) {
        return backtrack(r + 1, first_row);
    }

    // Try placing queen in each column of current row
    for (int c = 0; c < n; c++) {
        // Check if position (r, c) is under attack
        // A position is attacked if:
        // - Same column has a queen: col contains c
        // - Same positive diagonal has a queen: posDiag contains (r+c)
        // - Same negative diagonal has a queen: negDiag contains (r-c)
        if (col.count(c) || posDiag.count(r + c) || negDiag.count(r - c)) {
            continue;  // Position is attacked, try next column
        }

        // Position is safe! Place queen and mark attacked positions
        col.insert(c);              // Mark column as occupied
        posDiag.insert(r + c);      // Mark positive diagonal as occupied
        negDiag.insert(r - c);      // Mark negative diagonal as occupied
        board[r][c] = 'Q';          // Place queen on board

        // Recursively try to place queens in remaining rows
        if (backtrack(r + 1, first_row)) {
            return true;  // Solution found in deeper recursion
        }

        // Backtrack: Remove queen and unmark positions
        // This happens when placing queen at (r,c) didn't lead to solution
        col.erase(c);           // Unmark column
        posDiag.erase(r + c);   // Unmark positive diagonal
        negDiag.erase(r - c);   // Unmark negative diagonal
        board[r][c] = '.';      // Remove queen from board
    }

    // No valid column found in this row - backtrack to previous row
    return false;
}

// Main function
int main() {
    int first_row, first_col;

    // Input: Position for the first queen
    cout << "Enter row for first queen (0-" << n - 1 << "): ";
    cin >> first_row;
    cout << "Enter column for first queen (0-" << n - 1 << "): ";
    cin >> first_col;

    // Initialize board with all empty cells ('.')
    board = vector<vector<char>>(n, vector<char>(n, '.'));

    // Place first queen at specified position
    board[first_row][first_col] = 'Q';

    // Mark positions attacked by first queen
    col.insert(first_col);                      // Block column
    posDiag.insert(first_row + first_col);      // Block positive diagonal
    negDiag.insert(first_row - first_col);      // Block negative diagonal

    cout << "\nFirst queen placed at (" << first_row << ", " << first_col << ")\n\n";

    // Start backtracking from row 0
    // Backtrack will skip first_row (already has queen)
    if (backtrack(0, first_row)) {
        cout << "Solution found!" << endl;
    } else {
        cout << "No solution with first queen at (" << first_row << ", " << first_col << ")" << endl;
    }

    return 0;
}

/*
============================================================
EXAMPLE OUTPUT:
============================================================
Enter row for first queen (0-7): 0
Enter column for first queen (0-7): 0

First queen placed at (0, 0)

Q . . . . . . .
. . . . Q . . .
. . . . . . . Q
. . . . . Q . .
. . Q . . . . .
. . . . . . Q .
. Q . . . . . .
. . . Q . . . .

Solution found!

============================================================
HOW IT WORKS:
============================================================
1. Pre-place first queen at user-specified position
2. Mark column and diagonals attacked by first queen
3. Use backtracking to place remaining 7 queens
4. For each row, try all columns
5. Place queen only if position is not attacked
6. If placement fails, backtrack and try next position
7. Continue until all queens placed or no solution found

============================================================
ATTACK PATTERNS:
============================================================
Queens attack in 3 ways:
1. COLUMN: All cells in same column
   - Tracked using: col set (stores column indices)

2. POSITIVE DIAGONAL: Cells where (row + col) is constant
   - Example: (0,2), (1,3), (2,4) all have sum = row+col
   - Tracked using: posDiag set

3. NEGATIVE DIAGONAL: Cells where (row - col) is constant
   - Example: (0,2), (1,1), (2,0) all have diff = -2
   - Tracked using: negDiag set

============================================================
TIME AND SPACE COMPLEXITY:
============================================================
Time Complexity: O(n!) in worst case
- For each row, try n columns
- But pruning reduces actual explorations significantly

Space Complexity: O(n)
- Board: O(n²)
- Sets: O(n) each
- Recursion stack: O(n) depth
*/

// ============================================================
// PRACTICAL EXAM EXPLANATION
// ============================================================

/*
📚 N-QUEENS PROBLEM CONCEPT:
----------------------------
Classic backtracking problem in computer science

Goal: Place N queens on N×N chessboard such that:
- No two queens attack each other
- Queens attack horizontally, vertically, and diagonally

Problem Variant (This Code):
- First queen is pre-placed by user
- Find valid placement for remaining N-1 queens

Historical Context:
- Proposed by chess player Max Bezzel (1848)
- First solution by Franz Nauck (1850)
- Classic example of constraint satisfaction problem

🎯 BACKTRACKING STRATEGY:
-------------------------
Backtracking is a systematic trial-and-error approach:

1. CHOOSE: Try placing queen in a position
2. CONSTRAIN: Check if position is valid (not attacked)
3. EXPLORE: If valid, recursively solve for next row
4. BACKTRACK: If fails, undo choice and try next position

Key Insight:
- Place queens ROW BY ROW (one queen per row)
- For each row, try all columns
- Skip columns that are under attack
- This reduces search space from O(n^n) to O(n!)

🔧 ALGORITHM EXPLANATION:
-------------------------
PHASE 1: INITIALIZATION
Step 1: Create empty n×n board
Step 2: Place first queen at user-specified position
Step 3: Mark attacked columns and diagonals

PHASE 2: BACKTRACKING
Step 4: Start from row 0, process row by row
Step 5: For current row r:
        - If r == n: All queens placed! Print solution
        - If r == first_row: Skip (queen already there)
        - For each column c in row r:
            * Check if (r, c) is safe
            * If safe:
                - Place queen
                - Mark attacked positions
                - Recursively solve for row r+1
                - If successful: return true
                - Else: Remove queen (backtrack)
        - If no column works: return false

PHASE 3: TERMINATION
- Solution found: Print board and success message
- No solution: Print failure message

📊 DETAILED EXAMPLE WALKTHROUGH:
--------------------------------
Example: First queen at (0, 0) for 4×4 board

Initial State:
Q . . .    col={0}, posDiag={0}, negDiag={0}
. . . .
. . . .
. . . .

Step 1: Process Row 1
- Try (1,0): 0 in col? YES → Skip
- Try (1,1): 1 in col? NO, 2 in posDiag? YES → Skip
- Try (1,2): 2 in col? NO, 3 in posDiag? NO, 1 in negDiag? NO → PLACE!

Q . . .    col={0,2}, posDiag={0,3}, negDiag={0,1}
. . Q .
. . . .
. . . .

Step 2: Process Row 2
- Try (2,0): 0 in col? YES → Skip
- Try (2,1): 1 in col? NO, 3 in posDiag? YES → Skip
- Try (2,2): 2 in col? YES → Skip
- Try (2,3): 3 in col? NO, 5 in posDiag? NO, -1 in negDiag? NO → PLACE!

Q . . .    col={0,2,3}, posDiag={0,3,5}, negDiag={0,1,-1}
. . Q .
. . . Q
. . . .

Step 3: Process Row 3
- Try (3,0): 0 in col? YES → Skip
- Try (3,1): 1 in col? NO, 4 in posDiag? NO, 2 in negDiag? NO → PLACE!

Q . . .    SOLUTION FOUND!
. . Q .
. . . Q
. Q . .

If placement failed at any step, backtrack and try next column.

💡 WHY BACKTRACKING WORKS:
--------------------------
1. SYSTEMATIC EXPLORATION:
   - Explores all possible configurations
   - Guarantees finding solution if one exists

2. EARLY PRUNING:
   - Stops exploring as soon as constraint violated
   - Doesn't waste time on invalid paths

3. STATE RESTORATION:
   - Backtracking undoes changes
   - Allows exploring alternative paths

4. CONSTRAINT PROPAGATION:
   - Marking attacked positions immediately
   - Reduces search space early

🔑 ATTACK CHECKING OPTIMIZATION:
--------------------------------
Instead of checking every queen's position (O(n) per check),
use sets for O(1) checking:

Column Check:
- All cells in same column share column index
- Store occupied columns in set

Positive Diagonal Check:
- Cells on same diagonal have constant (row + col)
- Example: (0,3), (1,4), (2,5) → sum = 3, 5, 7
  Wait, (0,3)=3, (1,4)=5, (2,5)=7 - different!
- Actually: (0,2), (1,3), (2,4) → all sum to row+col = 2,4,6
  Still different. Let me correct:
- (0,2): 0+2=2, (1,3): 1+3=4 - WRONG!
- Correct: (0,0), (1,1), (2,2) → 0,2,4 - still different!
- Actually correct: same diagonal = same (r+c) value
  Example: diagonal from (0,2) includes (1,3), (2,4)
  But 0+2=2, 1+3=4, 2+4=6 - all different!

Let me reconsider: For positive diagonal:
- Move: right-down (r+1, c+1)
- (0,0), (1,1), (2,2) → r-c = 0, 0, 0 ✓
- That's NEGATIVE diagonal!

Correct understanding:
POSITIVE Diagonal (slope = -1, going ↘):
- Move: (r+1, c+1)
- Constant: r - c
- Example: (0,3), (1,4), (2,5) → 0-3=-3, 1-4=-3, 2-5=-3 ✓

NEGATIVE Diagonal (slope = 1, going ↙):
- Move: (r+1, c-1)
- Constant: r + c
- Example: (0,3), (1,2), (2,1) → 0+3=3, 1+2=3, 2+1=3 ✓

Wait, let me verify with code:
Code uses: posDiag stores (r+c), negDiag stores (r-c)

For diagonal ↘ (like \): (0,0), (1,1), (2,2)
- r+c: 0, 2, 4 (different) ✗
- r-c: 0, 0, 0 (same) ✓ → This is negDiag in code

For diagonal ↙ (like /): (2,0), (1,1), (0,2)
- r+c: 2, 2, 2 (same) ✓ → This is posDiag in code
- r-c: 2, 0, -2 (different) ✗

So the code naming is:
- posDiag (r+c): for / diagonals (bottom-left to top-right)
- negDiag (r-c): for \ diagonals (top-left to bottom-right)

⏱️ COMPLEXITY ANALYSIS:
-----------------------
Time Complexity: O(n!)
- First row: n choices
- Second row: at most (n-2) choices (after constraints)
- Third row: fewer choices
- Total: roughly n! configurations
- But pruning makes it much faster in practice

Space Complexity: O(n)
- Board: O(n²) for storage
- Sets: 3 × O(n) = O(n)
- Recursion stack: O(n) depth
- Total: O(n²) dominated by board

Actual Performance:
- 8-Queens: ~92 solutions exist
- With pruning: finds solution in milliseconds
- Without pruning: would take much longer

🎓 EXAM TIPS:
-------------
1. START with problem definition
   - N queens on N×N board
   - No two queens attack each other

2. EXPLAIN three attack directions
   - Horizontal (same row)
   - Vertical (same column)
   - Diagonal (two types)

3. SHOW diagonal formulas
   - Positive diagonal: r + c = constant
   - Negative diagonal: r - c = constant

4. DRAW small example (4×4)
   - Show step-by-step placement
   - Mark attacked cells
   - Show backtracking when stuck

5. EXPLAIN backtracking clearly
   - Try, check, recurse, backtrack

6. MENTION optimization
   - Sets for O(1) attack checking
   - Row-by-row placement

7. STATE complexity
   - Time: O(n!) with pruning
   - Space: O(n²)

❓ COMMON EXAM QUESTIONS:
-------------------------
Q1: What is backtracking?
A: Algorithmic technique for solving constraint satisfaction problems
   by trying possibilities and backtracking when constraints violated.

Q2: Why place queens row by row?
A: Ensures exactly one queen per row. Reduces search space from
   O(n^n) to O(n!) since we try n positions in row 1, then n-1, etc.

Q3: How to check if position is attacked?
A: Check three sets:
   - col: if column is occupied
   - posDiag: if r+c value exists
   - negDiag: if r-c value exists

Q4: What is the diagonal formula?
A: Positive diagonal (↗): r + c is constant
   Negative diagonal (↘): r - c is constant

Q5: Time complexity?
A: O(n!) - factorial due to decreasing choices per row.
   With pruning, actual time is much better.

Q6: How many solutions for 8-Queens?
A: 92 distinct solutions (12 fundamental, 80 by rotation/reflection).

Q7: What if no solution exists for given first queen position?
A: Some starting positions have no solution. Algorithm returns false
   after trying all possibilities.

Q8: Why use sets instead of arrays for tracking?
A: Sets provide O(1) lookup, insert, and delete operations.
   Array checking would be O(n) each time.

Q9: Can we use iteration instead of recursion?
A: Yes, but recursion is more natural for backtracking.
   Iteration requires explicit stack management.

Q10: Space optimization possible?
A: Yes! Instead of 2D board, can use 1D array storing column index
   for each row's queen. Space becomes O(n) instead of O(n²).

🎯 WHAT TO WRITE IN EXAM:
--------------------------
1. Problem statement (N queens, no attacks)
2. Backtracking concept
3. Attack patterns (3 types)
4. Diagonal formulas (r+c, r-c)
5. Algorithm steps (try, check, recurse, backtrack)
6. Complete code with comments
7. Small example (4×4) with step-by-step
8. Show backtracking scenario
9. Complexity: Time O(n!), Space O(n²)
10. Optimizations (sets for O(1) checking)

💻 CODE WALKTHROUGH FOR EXAM:
------------------------------
1. Global variables:
   - board: 2D grid
   - col, posDiag, negDiag: sets for attack tracking

2. printBoard():
   - Display current board state

3. backtrack(r, first_row):
   - Base case: r == n (all rows done)
   - Skip first_row (pre-placed queen)
   - Try each column c:
     * Check if safe (not in any set)
     * Place queen, update sets
     * Recurse to next row
     * Backtrack if failed

4. main():
   - Input first queen position
   - Initialize board and sets
   - Call backtrack(0, first_row)
   - Display result

🌟 KEY INSIGHTS FOR EXAM:
--------------------------
• Backtracking explores solution space systematically
• Constraint checking happens before recursion (pruning)
• Sets enable O(1) attack checking (optimization)
• Row-by-row placement reduces search space
• Undoing changes (backtracking) allows trying alternatives
• Pre-placing first queen adds constraint, may have no solution
• Solution guaranteed to be found if one exists
*/
