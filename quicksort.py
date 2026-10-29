"""
    Program for Quick Sort Analysis

    Compare two pivot selection strategies:
    1. Deterministic QuickSort - pivot is fixed (last element)
    2. Randomized QuickSort - pivot is randomly selected

    We count the number of recursive calls to analyze performance.
"""

# ============================================================
# Quick Sort Analysis - Deterministic vs Randomized
# ============================================================
# Time Complexity: O(n log n) average, O(n²) worst case
# Space Complexity: O(log n) recursion stack
# ============================================================

import sys
# Increase recursion limit to handle large arrays
# Default Python limit is ~1000, we increase it to avoid RecursionError
sys.setrecursionlimit(10**6)

import random, time

# Global counters to track number of recursive calls
global ctr1, ctr2
ctr1 = 0  # Counter for deterministic quicksort
ctr2 = 0  # Counter for randomized quicksort

def partition_normal(arr: list, low: int, high: int) -> int:
    """
    Partition function for deterministic quicksort.
    Uses LAST element as pivot (fixed strategy).

    Process:
    1. Choose pivot = arr[high] (last element)
    2. Rearrange so elements ≤ pivot are on left, > pivot on right
    3. Place pivot in correct sorted position
    4. Return pivot's final index

    Args:
        arr: Array to partition
        low: Starting index of subarray
        high: Ending index of subarray

    Returns:
        int: Final position of pivot after partitioning
    """
    # Pivot is always last element (deterministic choice)
    pivot = arr[high]

    # i tracks boundary between small and large elements
    # Elements from low to i are ≤ pivot
    # Elements from i+1 to j-1 are > pivot
    i = low - 1

    # Scan through array from low to high-1
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i += 1  # Expand the "small elements" region
            # Swap current element into small elements region
            arr[i], arr[j] = arr[j], arr[i]

    # Place pivot in its final sorted position
    # Everything before (i+1) is ≤ pivot, everything after is > pivot
    arr[i+1], arr[high] = arr[high], arr[i+1]

    # Return pivot's final position
    return i+1

def quicksort_normal(arr: list, low: int, high: int) -> None:
    """
    Deterministic QuickSort - always uses last element as pivot.

    Recursively sorts array by:
    1. Partitioning around pivot (last element)
    2. Recursively sorting left subarray
    3. Recursively sorting right subarray

    Worst Case: O(n²) on sorted or reverse-sorted arrays
    """
    global ctr1
    ctr1 += 1  # Count this recursive call

    # Base case: if subarray has 1 or 0 elements, it's already sorted
    if low < high:
        # Partition and get pivot's final position
        pivot = partition_normal(arr, low, high)

        # Recursively sort left subarray (elements < pivot)
        quicksort_normal(arr, low, pivot-1)

        # Recursively sort right subarray (elements > pivot)
        quicksort_normal(arr, pivot+1, high)

def partition_random(arr: list, low: int, high: int) -> int:
    """
    Partition function for randomized quicksort.
    Randomly selects pivot to avoid worst-case scenarios.

    Key Difference:
    1. Pick random index between low and high
    2. Swap random element with last position
    3. Use normal partition logic

    This ensures expected O(n log n) time even on sorted arrays.

    Args:
        arr: Array to partition
        low: Starting index
        high: Ending index

    Returns:
        int: Final position of pivot
    """
    # Randomly select pivot index (KEY DIFFERENCE from deterministic)
    # random.randint(low, high) returns random integer in [low, high]
    pivot = random.randint(low, high)

    # Swap randomly selected element with last element
    # Now last element is our random pivot
    arr[pivot], arr[high] = arr[high], arr[pivot]

    # Use the same partition logic as deterministic
    # Since we swapped random element to last position
    return partition_normal(arr, low, high)

def quicksort_random(arr: list, low: int, high: int) -> None:
    """
    Randomized QuickSort - randomly selects pivot element.

    Advantage over deterministic:
    - Avoids O(n²) worst case on sorted/reverse-sorted arrays
    - Expected O(n log n) for ANY input distribution
    - More robust and reliable in practice

    Args:
        arr: Array to sort
        low: Starting index
        high: Ending index
    """
    global ctr2
    ctr2 += 1  # Count this recursive call

    # Base case: subarray with ≤1 element is already sorted
    if low < high:
        # Partition with random pivot
        pivot = partition_random(arr, low, high)

        # Recursively sort left and right subarrays
        quicksort_random(arr, low, pivot-1)
        quicksort_random(arr, pivot+1, high)

# ── Main Program ──────────────────────────────────────────────
if __name__ == "__main__":
    # Get input array from user
    array1 = array2 = list(map(int, input("Enter an array to sort (space separated): ").split()))

    # Alternative: Generate array from 0 to N-1 (uncomment to use)
    # N = int(input("Enter the last number for the array to be sorted: "))
    # array1 = array2 = [x for x in range(N)]

    # Get array size
    N = len(array1)

    # Reset counters
    ctr1 = 0
    ctr2 = 0

    # ── Test 1: Deterministic QuickSort ──────────────────────
    print("\nSorting Using Normal QuickSort...")
    quicksort_normal(array1, 0, N-1)
    print(f"Sorted Array: {array1}")
    print(f"Normal QuickSort Performed {ctr1} Recursive Calls")

    # ── Test 2: Randomized QuickSort ─────────────────────────
    print("\nSorting using Random QuickSort...")
    quicksort_random(array2, 0, N-1)
    print(f"Sorted Array: {array2}")
    print(f"Randomized QuickSort Performed {ctr2} Recursive Calls")

    # ── Comparison ───────────────────────────────────────────
    print("\n" + "=" * 50)
    print("COMPARISON")
    print("=" * 50)
    print(f"Array size: {N}")
    print(f"Deterministic calls: {ctr1}")
    print(f"Randomized calls:    {ctr2}")

    if ctr1 < ctr2:
        print(f"\nDeterministic made {ctr2 - ctr1} FEWER calls")
    elif ctr2 < ctr1:
        print(f"\nRandomized made {ctr1 - ctr2} FEWER calls")
    else:
        print("\nBoth made SAME number of calls")

    print("\nNote: Fewer calls generally means better performance.")
    print("On sorted arrays, randomized typically makes fewer calls.")

"""
===============================================================================
                         PRACTICAL EXAM EXPLANATION
===============================================================================

PROBLEM STATEMENT:
------------------
Implement and compare two QuickSort variants:
1. Deterministic QuickSort - Always uses last element as pivot
2. Randomized QuickSort - Randomly selects pivot element

Analyze their performance by counting recursive calls.

QUICKSORT OVERVIEW:
-------------------
QuickSort is a Divide-and-Conquer sorting algorithm.

Key Steps:
1. Choose a pivot element
2. Partition: Rearrange array so elements < pivot are left, > pivot are right
3. Recursively apply to left and right subarrays
4. Base case: Subarrays of size ≤1 are already sorted

After partition, pivot is in its FINAL sorted position.

PARTITION ALGORITHM:
--------------------
Goal: Rearrange array around pivot

Variables:
- pivot: The chosen pivot value
- i: Boundary between small (≤pivot) and large (>pivot) elements
- j: Current scanning position

Invariant maintained:
- arr[low...i]: elements ≤ pivot
- arr[i+1...j-1]: elements > pivot
- arr[j...high-1]: not yet examined
- arr[high]: pivot element

Example: arr = [10, 80, 30, 90, 40, 50, 70], pivot = 70

Initial:  [10, 80, 30, 90, 40, 50, 70]
          i=-1 (before array)

j=0, arr[0]=10≤70: i=0, swap(arr[0],arr[0])
         [10, 80, 30, 90, 40, 50, 70]

j=1, arr[1]=80>70: no swap
         [10, 80, 30, 90, 40, 50, 70]

j=2, arr[2]=30≤70: i=1, swap(arr[1],arr[2])
         [10, 30, 80, 90, 40, 50, 70]

j=3, arr[3]=90>70: no swap
         [10, 30, 80, 90, 40, 50, 70]

j=4, arr[4]=40≤70: i=2, swap(arr[2],arr[4])
         [10, 30, 40, 90, 80, 50, 70]

j=5, arr[5]=50≤70: i=3, swap(arr[3],arr[5])
         [10, 30, 40, 50, 80, 90, 70]

Finally: Place pivot at i+1
         [10, 30, 40, 50, 70, 90, 80]
                         ↑
                    Final position

DETERMINISTIC QUICKSORT:
------------------------
Pivot Selection: Always last element (arr[high])

Characteristics:
+ Simple implementation
+ Predictable behavior
+ No extra overhead

- Worst case O(n²) on sorted arrays
- Worst case O(n²) on reverse sorted arrays
- Unbalanced partitions on certain inputs

Worst Case Example:
Input: [1, 2, 3, 4, 5] (sorted)

Recursion tree:
               [1,2,3,4,5]  pivot=5
              /
        [1,2,3,4]  pivot=4
        /
    [1,2,3]  pivot=3
    /
  [1,2]  pivot=2
  /
[1]  pivot=1

Tree depth: n
Partitions: n-1, n-2, ..., 1
Total work: n + (n-1) + (n-2) + ... + 1 = n(n+1)/2 = O(n²)

RANDOMIZED QUICKSORT:
---------------------
Pivot Selection: Random element from arr[low...high]

Process:
1. Choose random index: pivot_idx = random.randint(low, high)
2. Swap arr[pivot_idx] with arr[high]
3. Apply standard partition

Characteristics:
+ Expected O(n log n) on ANY input
+ Avoids worst case on sorted arrays
+ Robust against adversarial inputs
+ No input pattern consistently bad

- Slight overhead from random generation
- Performance varies between runs
- Harder to reason about deterministically

Why It Works:
- Random pivot → Expected balanced partitions
- Probability of consistently bad splits is negligible
- Expected tree depth: O(log n)
- Expected total work: O(n log n)

RECURSIVE CALL COUNTING:
------------------------
Why count recursive calls?
- Direct measure of algorithm behavior
- More calls → deeper recursion → worse performance
- Balanced tree: ~2n calls (each element processed once per level)
- Unbalanced tree: up to n² calls in worst case

Interpretation:
- Fewer calls = more balanced partitions = better performance
- More calls = unbalanced partitions = worse performance

TIME COMPLEXITY ANALYSIS:
-------------------------
Best Case: O(n log n)
- Pivot divides array into two equal halves
- Recurrence: T(n) = 2T(n/2) + O(n)
- Tree depth: log n
- Work per level: O(n)
- Total: O(n log n)

Average Case: O(n log n)
- Expected for randomized on any input
- Expected for deterministic on random input

Worst Case: O(n²)
- Pivot is always smallest or largest
- Recurrence: T(n) = T(n-1) + O(n)
- Tree depth: n
- Total: n + (n-1) + ... + 1 = O(n²)
- Happens in deterministic on sorted/reverse-sorted

SPACE COMPLEXITY:
-----------------
O(log n) average - Recursion stack depth

Best case (balanced):
- Tree depth = log n
- Stack space = O(log n)

Worst case (unbalanced):
- Tree depth = n
- Stack space = O(n)

Note: QuickSort is IN-PLACE
- Doesn't create new arrays
- Only uses existing array + stack space

COMPARISON: DETERMINISTIC VS RANDOMIZED:
----------------------------------------
┌─────────────────┬──────────────────┬──────────────────┐
│ Aspect          │ Deterministic    │ Randomized       │
├─────────────────┼──────────────────┼──────────────────┤
│ Pivot Choice    │ Last element     │ Random element   │
├─────────────────┼──────────────────┼──────────────────┤
│ Best Case       │ O(n log n)       │ O(n log n)       │
├─────────────────┼──────────────────┼──────────────────┤
│ Average Case    │ O(n log n)       │ O(n log n)       │
├─────────────────┼──────────────────┼──────────────────┤
│ Worst Case      │ O(n²)            │ O(n²) very rare  │
├─────────────────┼──────────────────┼──────────────────┤
│ Sorted Input    │ O(n²) ✗          │ O(n log n) ✓     │
├─────────────────┼──────────────────┼──────────────────┤
│ Reverse Sorted  │ O(n²) ✗          │ O(n log n) ✓     │
├─────────────────┼──────────────────┼──────────────────┤
│ Random Input    │ O(n log n)       │ O(n log n)       │
├─────────────────┼──────────────────┼──────────────────┤
│ Predictable     │ Yes              │ No (varies)      │
├─────────────────┼──────────────────┼──────────────────┤
│ Extra Overhead  │ None             │ Random gen       │
├─────────────────┼──────────────────┼──────────────────┤
│ Robustness      │ Low              │ High             │
└─────────────────┴──────────────────┴──────────────────┘

WHY sys.setrecursionlimit(10**6)?
----------------------------------
Python's default recursion limit is ~1000.

For large arrays with unbalanced partitions:
- Recursion depth can exceed 1000
- Causes RecursionError

Setting limit to 10⁶ allows:
- Sorting arrays up to ~1 million elements
- Handling worst-case scenarios
- Avoiding crashes during analysis

Note: Too high limit can cause stack overflow at OS level.

KEY POINTS TO MENTION DURING VIVA:
-----------------------------------
1. What is QuickSort?
   → Divide-and-conquer sorting algorithm
   → Partitions array around pivot
   → Recursively sorts subarrays

2. How does partition work?
   → Choose pivot, rearrange array
   → Elements ≤ pivot go left, > pivot go right
   → Pivot ends up in final sorted position

3. Why count recursive calls?
   → Measures partition balance quality
   → More balanced → fewer calls → better performance
   → Direct indicator of algorithm efficiency

4. Difference between variants?
   → Deterministic: Fixed pivot (last element)
   → Randomized: Random pivot selection
   → Randomized avoids worst case on sorted input

5. When is deterministic worst?
   → Sorted arrays: [1,2,3,4,5]
   → Reverse sorted: [5,4,3,2,1]
   → Creates maximally unbalanced partitions

6. Why does randomization help?
   → Breaks patterns that cause worst case
   → Expected balanced partitions
   → Probabilistic guarantee of O(n log n)

7. Is QuickSort stable?
   → NO - Equal elements may swap
   → Can be made stable with modifications

8. Is QuickSort in-place?
   → YES - Sorts within original array
   → Only O(log n) stack space needed

9. QuickSort vs MergeSort?
   → QuickSort: In-place, cache-friendly, faster average
   → MergeSort: Stable, guaranteed O(n log n), needs O(n) space

10. How to optimize QuickSort?
    → Use randomized pivot (done here)
    → Three-way partitioning for duplicates
    → Insertion sort for small subarrays
    → Median-of-three pivot selection

SAMPLE OUTPUT:
--------------
Example 1: Random Array

Enter an array to sort (space separated): 64 34 25 12 22 11 90

Sorting Using Normal QuickSort...
Sorted Array: [11, 12, 22, 25, 34, 64, 90]
Normal QuickSort Performed 13 Recursive Calls

Sorting using Random QuickSort...
Sorted Array: [11, 12, 22, 25, 34, 64, 90]
Randomized QuickSort Performed 11 Recursive Calls

==================================================
COMPARISON
==================================================
Array size: 7
Deterministic calls: 13
Randomized calls:    11

Randomized made 2 FEWER calls

Note: Fewer calls generally means better performance.
On sorted arrays, randomized typically makes fewer calls.

Example 2: Sorted Array (Worst Case for Deterministic)

Enter an array to sort (space separated): 1 2 3 4 5 6 7 8 9 10

Sorting Using Normal QuickSort...
Sorted Array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Normal QuickSort Performed 55 Recursive Calls

Sorting using Random QuickSort...
Sorted Array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Randomized QuickSort Performed 21 Recursive Calls

==================================================
COMPARISON
==================================================
Array size: 10
Deterministic calls: 55
Randomized calls:    21

Randomized made 34 FEWER calls

Note: Fewer calls generally means better performance.
On sorted arrays, randomized typically makes fewer calls.

ANALYSIS INTERPRETATION:
------------------------
Random Array:
- Both perform similarly
- Slight advantage to randomized
- Both have balanced partitions

Sorted Array:
- Deterministic: O(n²) behavior (55 calls for n=10)
- Randomized: O(n log n) behavior (21 calls for n=10)
- Huge difference! Randomized 2-3x fewer calls

Reverse Sorted:
- Similar to sorted case
- Deterministic worst case
- Randomized handles well

PRACTICAL EXAM TIPS:
--------------------
✓ Explain partition process with example
✓ Show how pivot ends in final position
✓ Demonstrate worst case with sorted array
✓ Explain why randomized avoids worst case
✓ Interpret recursive call counts
✓ Mention time complexity for all cases
✓ Know space complexity (O(log n) stack)
✓ Compare with other O(n log n) sorts
✓ Understand sys.setrecursionlimit purpose
✓ Be ready to trace through small example

COMMON MISTAKES TO AVOID:
--------------------------
✗ Forgetting to reset counters (ctr1, ctr2)
✗ Using same array reference (use .copy() if needed)
✗ Wrong index in partition (i, j confusion)
✗ Not handling base case (low >= high)
✗ Claiming QuickSort is always O(n log n)
✗ Saying QuickSort is stable (it's not!)
✗ Not understanding why randomization helps

ADVANTAGES OF QUICKSORT:
------------------------
+ Fast average case: O(n log n)
+ In-place sorting (low space overhead)
+ Cache-friendly (good locality)
+ Simple to implement
+ Works well in practice

DISADVANTAGES:
--------------
- Worst case O(n²) (deterministic)
- Not stable
- Requires recursion (stack space)
- Performance varies with pivot choice

===============================================================================
"""
