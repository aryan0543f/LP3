# ============================================================
# 8-Queens Problem – Backtracking
# ============================================================
# Aim: Place 8 queens on an 8×8 chessboard so that no two
#      queens attack each other (no same row, column, or diagonal)
# ============================================================
# First queen position is taken as user input.
# Time Complexity : O(N!) — factorial due to backtracking
# Space Complexity: O(N²) — board matrix + O(N) recursion stack
# ============================================================

N = 8   # board size (8×8 chessboard)

def is_safe(board, row, col):
    """
    Check if placing a queen at position (row, col) is safe.

    A position is safe if no other queen can attack it:
    - No queen in same column (above current row)
    - No queen in upper-left diagonal
    - No queen in upper-right diagonal

    Note: We don't check same row because we place one queen per row.
          We only check above because we fill top-to-bottom.

    Args:
        board: 2D list representing chessboard (1 = queen, 0 = empty)
        row: Row index where we want to place queen
        col: Column index where we want to place queen

    Returns:
        bool: True if position is safe, False otherwise
    """

    # Check 1: Check same column above current row
    # We only need to check above because we haven't placed queens below yet
    for i in range(row):
        if board[i][col] == 1:  # Found a queen in same column
            return False

    # Check 2: Check upper-left diagonal (going up-left from current position)
    # Move diagonally: row decreases, column decreases
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:  # Stay within board boundaries
        if board[i][j] == 1:  # Found a queen on this diagonal
            return False
        i -= 1  # Move up
        j -= 1  # Move left

    # Check 3: Check upper-right diagonal (going up-right from current position)
    # Move diagonally: row decreases, column increases
    i, j = row - 1, col + 1
    while i >= 0 and j < N:  # Stay within board boundaries
        if board[i][j] == 1:  # Found a queen on this diagonal
            return False
        i -= 1  # Move up
        j += 1  # Move right

    # If all checks passed, position is safe
    return True

def solve(board, row):
    """
    Recursively place queens row by row using backtracking.

    Strategy:
    - Try to place a queen in each column of current row
    - If safe, place it and recurse to next row
    - If recursion succeeds, we found a solution
    - If recursion fails, backtrack (remove queen) and try next column
    - If no column works, return False (trigger backtracking in previous row)

    Args:
        board: Current state of chessboard
        row: Current row we're trying to place a queen in

    Returns:
        bool: True if solution found from this state, False otherwise
    """

    # Base case: All queens placed successfully
    # If we've placed queens in all N rows, we're done!
    if row == N:
        return True

    # Try placing queen in each column of current row
    for col in range(N):
        # Check if placing queen at (row, col) is safe
        if is_safe(board, row, col):
            # Place queen (make a choice)
            board[row][col] = 1

            # Recursively try to place queens in remaining rows
            # If successful, propagate success up the recursion chain
            if solve(board, row + 1):
                return True

            # If recursion failed, backtrack
            # Remove queen and try next column
            board[row][col] = 0

    # If no column worked in this row, return False
    # This triggers backtracking in the previous row
    return False

def print_board(board):
    """
    Print the chessboard in a readable format.
    Q = queen position, . = empty square
    Shows row and column indices for clarity.
    """
    # Print column numbers
    print("\n  " + "  ".join(str(c) for c in range(N)))
    print("  " + "-" * (N * 3))

    # Print each row with row number
    for r in range(N):
        # Create row string: Q for queen, . for empty
        row_str = " | ".join("Q" if board[r][c] == 1 else "." for c in range(N))
        print(f"{r} | {row_str}")
    print()

# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # Display problem description
    print("8-Queens Problem using Backtracking")
    print(f"Board size: {N}×{N}  (rows and columns are 0-indexed)\n")

    # Get first queen position from user
    first_row = int(input(f"Enter row for first queen (0 to {N-1}): "))
    first_col = int(input(f"Enter column for first queen (0 to {N-1}): "))

    # Initialise empty board (all zeros)
    # board[i][j] = 1 means queen at position (i, j)
    # board[i][j] = 0 means empty square
    board = [[0] * N for _ in range(N)]

    # Place first queen at user-specified position
    board[first_row][first_col] = 1

    print(f"\nFirst queen placed at ({first_row}, {first_col})")
    print("Solving with backtracking...\n")

    # Solve the puzzle in two phases:
    # Phase 1: Solve rows BEFORE first queen (if any)
    # Phase 2: Solve rows AFTER first queen

    solved = True

    # Phase 1: Fill rows 0 to (first_row - 1)
    for row in range(first_row):
        if not solve(board, row):
            solved = False  # No solution with this starting position
            break

    # Phase 2: Fill rows (first_row + 1) to N-1
    # Only attempt if Phase 1 succeeded
    if solved:
        solved = solve(board, first_row + 1)

    # Display result
    if solved:
        print("Solution found!")
        print_board(board)

        # Also print as matrix (for copying/verification)
        print("Final 8-Queens matrix:")
        for row in board:
            print(row)
    else:
        print(f"No solution exists with first queen at ({first_row}, {first_col}).")
        print("Try a different starting position.")

# ── Complexity ────────────────────────────────────────────────
# Time : O(N!)  — N choices for row 1, N-1 for row 2, …
#                 Worst case explores factorial branches
#                 In practice: pruning makes it much faster
# Space: O(N²)  — board matrix  +  O(N) recursion stack depth

"""
===============================================================================
                         PRACTICAL EXAM EXPLANATION
===============================================================================

PROBLEM STATEMENT:
------------------
Place N queens on an N×N chessboard such that no two queens attack each other.

Queens Attack Rules (Chess):
- Horizontal: Any square in same row
- Vertical: Any square in same column
- Diagonal: Any square on both diagonals (/ and \)

Constraints:
- Exactly N queens must be placed
- No two queens can attack each other
- Each row must have exactly one queen
- Each column must have exactly one queen
- No two queens on same diagonal

Goal: Find ANY valid configuration (or all configurations)

N-QUEENS VARIANTS:
------------------
1. Find ONE solution (this code)
2. Find ALL solutions (modify to collect instead of returning on first)
3. Count total solutions (count instead of print)
4. With first queen fixed (this code - user input)
5. Generalized N-Queens (works for any N, not just 8)

WHY BACKTRACKING?
-----------------
Brute Force Approach:
- Try all possible placements of N queens on N² squares
- Check each configuration if valid
- Total configurations: C(N², N) ≈ 64!/(8!×56!) for 8-queens
- Astronomically large! Not feasible

Backtracking Improvement:
- Build solution incrementally (one queen at a time)
- Check constraints at each step
- Abandon partial solutions that violate constraints
- Prune entire branches of search tree early
- Much more efficient than brute force

BACKTRACKING ALGORITHM PATTERN:
--------------------------------
General Template:

    def backtrack(state, choices):
        if is_complete(state):
            return state  # Found solution

        for choice in choices:
            if is_valid(state, choice):
                make_choice(state, choice)

                if backtrack(state, new_choices):
                    return True  # Solution found

                undo_choice(state, choice)  # Backtrack

        return False  # No solution in this branch

Applied to N-Queens:
- State: Current board configuration
- Choices: Columns in current row to try
- is_valid: is_safe() function
- make_choice: Place queen (board[row][col] = 1)
- undo_choice: Remove queen (board[row][col] = 0)

ALGORITHM STEPS (ROW-BY-ROW):
------------------------------
1. Start with empty board and row 0
2. For current row, try placing queen in each column (0 to N-1):
   a. Check if position is safe (is_safe function)
   b. If safe:
      - Place queen at this position
      - Recursively solve for next row
      - If recursion succeeds → solution found!
      - If recursion fails → remove queen (backtrack)
   c. If not safe, skip to next column
3. If no column works in current row → return False (backtrack)
4. Base case: If all rows filled → success!

IS_SAFE FUNCTION LOGIC:
-----------------------
To place queen at (row, col), check three directions:

1. Column Check (Vertical):
   - Look upward in same column
   - for i in range(row): check board[i][col]

2. Upper-Left Diagonal (\):
   - Move diagonally up-left: (row-1, col-1), (row-2, col-2), ...
   - While i >= 0 and j >= 0: check board[i][j]

3. Upper-Right Diagonal (/):
   - Move diagonally up-right: (row-1, col+1), (row-2, col+2), ...
   - While i >= 0 and j < N: check board[i][j]

Why only check ABOVE?
- We place queens row by row from top to bottom
- Rows below current row are still empty
- No need to check below, only above

Why not check same ROW?
- Our algorithm places one queen per row
- Current row has no queen yet (we're placing it now)
- Previous rows already have their queen placed

COMPLEXITY ANALYSIS:
--------------------
Time Complexity: O(N!)

Reasoning:
- Row 1: N choices (all columns available)
- Row 2: ≤ N-1 valid choices (some positions attacked)
- Row 3: ≤ N-2 valid choices
- ...
- Total: N × (N-1) × (N-2) × ... ≈ O(N!)

In practice:
- Pruning significantly reduces branches explored
- Many branches cut early by is_safe checks
- Actual time much better than theoretical worst case

Space Complexity: O(N²)

Components:
- Board: O(N²) for N×N matrix
- Recursion stack: O(N) depth (max N recursive calls)
- Total: O(N²) + O(N) = O(N²)

WORKED EXAMPLE (4-Queens for simplicity):
------------------------------------------
Board size: 4×4
Place 4 queens

Attempt 1: Start row 0, try col 0
  Place Q at (0,0)

  Row 1: Try col 0 → Not safe (same column)
         Try col 1 → Not safe (diagonal from (0,0))
         Try col 2 → Safe! Place Q at (1,2)

  Row 2: Try col 0 → Not safe (diagonal from (1,2))
         Try col 1 → Not safe (column from (0,0))
         Try col 2 → Not safe (column from (1,2))
         Try col 3 → Not safe (diagonal from (1,2))
         NO VALID POSITION → Backtrack to row 1

  Back to Row 1: Remove Q from (1,2)
                 Try col 3 → Safe! Place Q at (1,3)

  Row 2: Try col 0 → Not safe (diagonal)
         Try col 1 → Safe! Place Q at (2,1)

  Row 3: Try col 0 → Not safe (column)
         Try col 1 → Not safe (column)
         Try col 2 → Not safe (diagonal)
         Try col 3 → Not safe (column)
         NO VALID POSITION → Backtrack to row 2

  ... (continue backtracking and trying)

Eventually find solution:
  . Q . .     (0,1)
  . . . Q     (1,3)
  Q . . .     (2,0)
  . . Q .     (3,2)

Verification:
- No two queens in same row ✓
- No two queens in same column ✓
- No two queens on same diagonal ✓

8-QUEENS SPECIFIC:
------------------
Total Solutions: 92 distinct solutions for standard 8-Queens
Fundamental Solutions: 12 (others are rotations/reflections)

Example Solution:
  Row 0: Queen at column 0
  Row 1: Queen at column 4
  Row 2: Queen at column 7
  Row 3: Queen at column 5
  Row 4: Queen at column 2
  Row 5: Queen at column 6
  Row 6: Queen at column 1
  Row 7: Queen at column 3

Visual:
  Q . . . . . . .
  . . . . Q . . .
  . . . . . . . Q
  . . . . . Q . .
  . . Q . . . . .
  . . . . . . Q .
  . Q . . . . . .
  . . . Q . . . .

KEY POINTS TO MENTION DURING VIVA:
-----------------------------------
1. What is Backtracking?
   → Algorithmic technique for solving constraint satisfaction problems
   → Build solution incrementally, abandoning paths that violate constraints
   → "Try, and if it fails, undo and try another way"

2. Why is N-Queens a backtracking problem?
   → Large search space (brute force infeasible)
   → Constraints can be checked incrementally
   → Many branches can be pruned early
   → No better algorithm known (NP-hard for general case)

3. How does backtracking differ from brute force?
   → Brute force: Try all possibilities, check at end
   → Backtracking: Check constraints at each step, prune early
   → Backtracking is intelligent exhaustive search

4. What is the base case in recursion?
   → When row == N (all rows filled with queens)
   → Means we successfully placed N queens
   → Return True to propagate success

5. What triggers backtracking?
   → When is_safe returns False for all columns in a row
   → solve() returns False
   → Previous recursion level removes its queen and tries next column

6. Why check only above in is_safe?
   → We fill top-to-bottom, row by row
   → Rows below current row are still empty
   → No queens below to conflict with

7. Can we optimize further?
   → Yes! Use arrays to track attacked columns and diagonals
   → O(1) conflict checking instead of O(N)
   → Space-time tradeoff

8. How many solutions exist for N-Queens?
   → N=1: 1 solution
   → N=4: 2 solutions
   → N=8: 92 solutions
   → N=10: 724 solutions
   → No closed-form formula; grows exponentially

OPTIMIZATION TECHNIQUES:
------------------------
1. Bitmasking:
   - Use bits to represent attacked positions
   - Faster conflict checking

2. Column/Diagonal Arrays:
   - Track attacked columns: col_used[N]
   - Track attacked diagonals: diag1[2N-1], diag2[2N-1]
   - O(1) checking instead of O(N)

3. Symmetry Breaking:
   - For first queen, only try first N/2 positions
   - Generate symmetric solutions by mirroring

4. Heuristics:
   - Most constrained variable: pick row with fewest options
   - Least constraining value: pick column that blocks fewest future options

REAL-WORLD APPLICATIONS:
------------------------
1. Scheduling Problems:
   - Assign tasks to time slots without conflicts
   - Constraint: No resource conflicts

2. Graph Coloring:
   - Color graph nodes so adjacent nodes have different colors
   - Map coloring, register allocation

3. Sudoku Solver:
   - Fill grid respecting row/column/box constraints
   - Classic backtracking problem

4. Constraint Satisfaction:
   - Any problem with constraints to satisfy
   - Resource allocation, timetabling

5. Combinatorial Optimization:
   - Find valid configuration among many possibilities
   - Pruning infeasible branches early

SAMPLE OUTPUT:
--------------
8-Queens Problem using Backtracking
Board size: 8×8  (rows and columns are 0-indexed)

Enter row for first queen (0 to 7): 0
Enter column for first queen (0 to 7): 0

First queen placed at (0, 0)
Solving with backtracking...

Solution found!

  0  1  2  3  4  5  6  7
  -----------------------
0 | Q  .  .  .  .  .  .  .
1 | .  .  .  .  Q  .  .  .
2 | .  .  .  .  .  .  .  Q
3 | .  .  .  .  .  Q  .  .
4 | .  .  Q  .  .  .  .  .
5 | .  .  .  .  .  .  Q  .
6 | .  Q  .  .  .  .  .  .
7 | .  .  .  Q  .  .  .  .

Final 8-Queens matrix:
[1, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 1, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 1]
[0, 0, 0, 0, 0, 1, 0, 0]
[0, 0, 1, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 1, 0]
[0, 1, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 1, 0, 0, 0, 0]

ANOTHER EXAMPLE (No Solution):
-------------------------------
Enter row for first queen (0 to 7): 0
Enter column for first queen (0 to 7): 1

First queen placed at (0, 1)
Solving with backtracking...

No solution exists with first queen at (0, 1).
Try a different starting position.

PRACTICAL EXAM TIPS:
--------------------
✓ Explain the problem clearly (no two queens attack each other)
✓ Draw a small board (4×4) to demonstrate attacks
✓ Explain why backtracking is needed (huge search space)
✓ Trace through is_safe() for a sample position
✓ Show backtracking with a small example (4-Queens)
✓ Explain the three checks in is_safe (column, two diagonals)
✓ Mention time complexity O(N!) and why
✓ Discuss space complexity O(N²) for board
✓ Be ready to modify: find all solutions vs find one
✓ Know real-world applications

COMMON MISTAKES TO AVOID:
--------------------------
✗ Checking entire board in is_safe (only need to check above)
✗ Forgetting to backtrack (remove queen when recursion fails)
✗ Checking same row in is_safe (we place one queen per row)
✗ Wrong diagonal checking logic (off-by-one errors)
✗ Not handling base case (row == N)
✗ Claiming it's polynomial time (it's exponential/factorial)

ADVANTAGES OF BACKTRACKING:
---------------------------
+ Much faster than brute force
+ Guarantees finding solution if one exists
+ Memory efficient (only stores one path at a time)
+ Easy to extend to find all solutions
+ Works for any N (generalized N-Queens)

DISADVANTAGES:
--------------
- Still exponential time complexity
- May take long for large N (N > 15 gets slow)
- Not parallelizable easily (sequential exploration)
- Worst case explores entire search tree

MODIFICATIONS FOR INTERVIEW/EXAM:
----------------------------------
1. Find all solutions:
   - Don't return True on first solution
   - Collect all valid boards in a list
   - Continue exploring all branches

2. Count solutions:
   - Replace return True with counter += 1
   - Return count at the end

3. Optimized version:
   - Use arrays to track attacked positions
   - Reduce is_safe from O(N) to O(1)

===============================================================================
"""
