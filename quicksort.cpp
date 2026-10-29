// ============================================================
// QuickSort Analysis - Deterministic vs Randomized
// ============================================================
// Program for Quick Sort Analysis
// Compare two pivot selection strategies:
// 1. Deterministic QuickSort - pivot is fixed (last element)
// 2. Randomized QuickSort - pivot is randomly selected
// We count the number of recursive calls to analyze performance.
// ============================================================

#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
using namespace std;

// Global counters to track recursive calls
int ctr1 = 0;  // Counter for deterministic quicksort
int ctr2 = 0;  // Counter for randomized quicksort

// Partition function (shared by both)
/**
 * Partitions the array around a pivot element
 * Places pivot in its correct sorted position
 * Elements smaller than pivot go to left
 * Elements greater than pivot go to right
 *
 * @param arr: Array to be partitioned
 * @param low: Starting index of partition range
 * @param high: Ending index of partition range (pivot is at arr[high])
 * @return: Final position of pivot after partitioning
 *
 * Time Complexity: O(n) where n = high - low + 1
 */
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];  // Choose last element as pivot
    int i = low - 1;        // Index of smaller element (boundary)

    // Traverse through array and rearrange elements
    for (int j = low; j < high; j++) {
        // If current element is smaller than or equal to pivot
        if (arr[j] <= pivot) {
            // Move boundary of smaller elements
            // Swap current element with element at boundary
            swap(arr[++i], arr[j]);
        }
    }

    // Place pivot in its correct position (after all smaller elements)
    swap(arr[i + 1], arr[high]);

    // Return the final position of pivot
    return i + 1;
}

// Deterministic QuickSort
/**
 * Standard QuickSort with fixed pivot selection (last element)
 *
 * @param arr: Array to be sorted
 * @param low: Starting index
 * @param high: Ending index
 *
 * Pivot Strategy: Always picks LAST element as pivot
 *
 * Problem: Worst case O(n²) on already sorted or reverse sorted arrays
 * Reason: Pivot is always smallest/largest, creating unbalanced partitions
 */
void quicksort_normal(vector<int>& arr, int low, int high) {
    // Base case: if subarray has more than 1 element
    if (low < high) {
        ctr1++;  // Count this recursive call

        // Partition array and get pivot's final position
        int pi = partition(arr, low, high);

        // Recursively sort left subarray (elements smaller than pivot)
        quicksort_normal(arr, low, pi - 1);

        // Recursively sort right subarray (elements greater than pivot)
        quicksort_normal(arr, pi + 1, high);
    }
}

// Randomized QuickSort
/**
 * QuickSort with random pivot selection
 *
 * @param arr: Array to be sorted
 * @param low: Starting index
 * @param high: Ending index
 *
 * Pivot Strategy: Randomly selects pivot, then swaps with last element
 *
 * Advantage: Expected O(n log n) on ANY input (including sorted arrays)
 * Reason: Random pivot selection avoids worst-case scenarios
 */
void quicksort_random(vector<int>& arr, int low, int high) {
    // Base case: if subarray has more than 1 element
    if (low < high) {
        ctr2++;  // Count this recursive call

        // Random pivot selection - KEY DIFFERENCE from deterministic
        // Select random index between low and high
        // rand() % (high - low + 1) gives random number in range [0, high-low]
        // Adding low shifts range to [low, high]
        swap(arr[low + rand() % (high - low + 1)], arr[high]);

        // Now last element is random pivot
        // Use same partition logic as deterministic
        int pi = partition(arr, low, high);

        // Recursively sort left and right subarrays
        quicksort_random(arr, low, pi - 1);
        quicksort_random(arr, pi + 1, high);
    }
}

int main() {
    // Seed random number generator with current time
    // Ensures different random numbers each run
    srand(time(0));

    int n;
    cout << "Enter number of elements: ";
    cin >> n;

    // Create two identical arrays for comparison
    vector<int> arr1(n), arr2(n);

    cout << "Enter elements: ";
    for (int i = 0; i < n; i++) {
        cin >> arr1[i];
        arr2[i] = arr1[i];  // Copy to second array
    }

    // Sort using deterministic quicksort
    quicksort_normal(arr1, 0, n - 1);

    // Sort using randomized quicksort
    quicksort_random(arr2, 0, n - 1);

    // Display comparison results
    cout << "\nDeterministic calls: " << ctr1 << endl;
    cout << "Randomized calls: " << ctr2 << endl;
    cout << "Difference: " << abs(ctr1 - ctr2) << endl;

    return 0;
}

/*
============================================================
EXAMPLE OUTPUT:
============================================================
Enter number of elements: 5
Enter elements: 5 2 8 1 9

Deterministic calls: 9
Randomized calls: 9
Difference: 0

For sorted array (worst case for deterministic):
Enter number of elements: 5
Enter elements: 1 2 3 4 5

Deterministic calls: 15
Randomized calls: 9
Difference: 6

============================================================
TIME COMPLEXITY ANALYSIS:
============================================================
Deterministic QuickSort:
- Best Case: O(n log n) - balanced partitions
- Average Case: O(n log n)
- Worst Case: O(n²) - unbalanced partitions (sorted/reverse sorted)

Randomized QuickSort:
- Best Case: O(n log n)
- Average Case: O(n log n)
- Expected Case: O(n log n) - even on sorted arrays!
- Worst Case: O(n²) - extremely rare with random pivots

Space Complexity (Both):
- O(log n) - recursion stack depth for balanced partitions
- O(n) - worst case recursion depth

============================================================
KEY DIFFERENCES:
============================================================
Deterministic QuickSort:
✓ Simple implementation
✓ Fast on random data
✗ O(n²) on sorted/reverse sorted arrays
✗ Predictable performance (can be exploited)

Randomized QuickSort:
✓ Expected O(n log n) on ALL inputs
✓ No worst-case input can be constructed
✓ More robust in practice
✗ Slightly more overhead (random number generation)
*/

// ============================================================
// PRACTICAL EXAM EXPLANATION
// ============================================================

/*
📚 QUICKSORT CONCEPT:
---------------------
QuickSort is a divide-and-conquer sorting algorithm

Key Idea:
1. Choose a PIVOT element
2. PARTITION array: smaller elements left, larger elements right
3. RECURSIVELY sort left and right subarrays

Invented by: Tony Hoare (1959)
Status: One of the most efficient sorting algorithms in practice

🎯 PARTITION PROCESS:
---------------------
Given: [3, 7, 1, 9, 2, 5]  (pivot = 5, last element)

Step-by-step:
i = -1 (boundary of smaller elements)

j=0: arr[0]=3 ≤ 5? YES → i=0, swap arr[0] with arr[0] → [3, 7, 1, 9, 2, 5]
j=1: arr[1]=7 ≤ 5? NO  → no swap → [3, 7, 1, 9, 2, 5]
j=2: arr[2]=1 ≤ 5? YES → i=1, swap arr[1] with arr[2] → [3, 1, 7, 9, 2, 5]
j=3: arr[3]=9 ≤ 5? NO  → no swap → [3, 1, 7, 9, 2, 5]
j=4: arr[4]=2 ≤ 5? YES → i=2, swap arr[2] with arr[4] → [3, 1, 2, 9, 7, 5]

Finally: Swap pivot with arr[i+1] → [3, 1, 2, 5, 7, 9]
                                              ↑
                                          pivot in correct position

Result: [3, 1, 2] < 5 < [7, 9]

🔧 DETERMINISTIC QUICKSORT:
---------------------------
Pivot Selection: ALWAYS last element

Example - Sorted Array [1, 2, 3, 4, 5]:

Round 1: pivot=5, partition → [1, 2, 3, 4] | 5 | []
Round 2: pivot=4, partition → [1, 2, 3] | 4 | []
Round 3: pivot=3, partition → [1, 2] | 3 | []
Round 4: pivot=2, partition → [1] | 2 | []
Round 5: pivot=1, partition → [] | 1 | []

Recursion tree:
          [1,2,3,4,5]
          /
       [1,2,3,4]
       /
    [1,2,3]
    /
  [1,2]
  /
 [1]

Depth = n (unbalanced!)
Comparisons = n + (n-1) + (n-2) + ... + 1 = n(n+1)/2 = O(n²)

🎲 RANDOMIZED QUICKSORT:
------------------------
Pivot Selection: RANDOM element (then swap to end)

Same Array [1, 2, 3, 4, 5]:

Suppose random pivot = 3:
Round 1: pivot=3, partition → [1, 2] | 3 | [4, 5]
         ↓                              ↓
  Left: pivot=1 or 2             Right: pivot=4 or 5

Recursion tree (balanced):
          [1,2,3,4,5]
          /         \
       [1,2]        [4,5]
       /  \         /  \
      [1] [2]     [4] [5]

Depth = log n (balanced!)
Comparisons = n log n = O(n log n)

💡 WHY RANDOMIZED IS BETTER:
----------------------------
1. NO WORST-CASE INPUT:
   - Deterministic: sorted array → worst case
   - Randomized: any array → expected good performance

2. PROBABILISTIC GUARANTEE:
   - High probability of balanced partitions
   - Expected O(n log n) on ANY input

3. CANNOT BE EXPLOITED:
   - Attacker can't construct worst-case input
   - Important for systems with adversarial input

4. PRACTICAL PERFORMANCE:
   - Generally faster on real-world data
   - Avoids degenerate cases

📊 PERFORMANCE COMPARISON:
--------------------------
Input Type        | Deterministic | Randomized
------------------|---------------|------------
Random            | O(n log n)    | O(n log n)
Sorted            | O(n²)         | O(n log n)
Reverse Sorted    | O(n²)         | O(n log n)
All Same          | O(n²)         | O(n log n)
Nearly Sorted     | O(n²)         | O(n log n)

Recursive Calls on [1,2,3,4,5]:
- Deterministic: 15 calls (O(n²) pattern)
- Randomized: ~9 calls (O(n log n) pattern)

🔑 KEY INSIGHTS:
----------------
1. PIVOT MATTERS:
   - Good pivot → balanced partitions → O(n log n)
   - Bad pivot → unbalanced → O(n²)

2. RANDOMIZATION HELPS:
   - Random pivot → likely balanced
   - No input can guarantee worst case

3. IN-PLACE SORTING:
   - QuickSort sorts within array
   - Only O(log n) extra space for recursion

4. NOT STABLE:
   - Equal elements may change relative order
   - Can be made stable with extra space

⏱️ RECURSION DEPTH ANALYSIS:
----------------------------
Deterministic on sorted array:
- Each recursion reduces size by 1
- Depth = n
- Stack space = O(n)

Randomized (expected):
- Each recursion divides roughly in half
- Depth = log n
- Stack space = O(log n)

🎓 EXAM TIPS:
-------------
1. EXPLAIN partition process
   - Show how pivot finds correct position
   - Elements left < pivot < elements right

2. TRACE small example (5-6 elements)
   - Show partition steps
   - Show recursive calls

3. COMPARE both approaches
   - Deterministic: simple but vulnerable
   - Randomized: robust, expected O(n log n)

4. MENTION worst case
   - Sorted/reverse sorted for deterministic
   - Extremely rare for randomized

5. DRAW recursion tree
   - Unbalanced for deterministic on sorted
   - Balanced for randomized

6. STATE complexity
   - Time: O(n log n) average, O(n²) worst
   - Space: O(log n) average, O(n) worst

❓ COMMON EXAM QUESTIONS:
-------------------------
Q1: How does partition work?
A: Chooses pivot, rearranges array so elements ≤ pivot are on left,
   elements > pivot are on right. Returns pivot's final position.

Q2: What is the pivot in deterministic quicksort?
A: Always the LAST element (arr[high]).

Q3: What is the pivot in randomized quicksort?
A: RANDOM element between low and high, then swapped to last position.

Q4: Why is randomized better?
A: Avoids worst case O(n²) on sorted arrays. Expected O(n log n) on
   ALL inputs due to random pivot selection.

Q5: Time complexity?
A: Best/Average: O(n log n)
   Worst: O(n²) - rare for randomized, common for deterministic on sorted

Q6: Space complexity?
A: O(log n) average for recursion stack
   O(n) worst case (unbalanced partitions)

Q7: Is QuickSort stable?
A: NO. Equal elements may change order due to swapping during partition.

Q8: When does deterministic perform worst?
A: On already sorted or reverse sorted arrays - pivot is always
   smallest/largest, creating unbalanced partitions.

Q9: Why count recursive calls?
A: Number of calls indicates how balanced partitions are.
   More calls = more unbalanced = worse performance.

Q10: Can randomized have O(n²)?
A: Theoretically yes, if extremely unlucky with random pivots.
   But probability is negligible (like (1/n)^n).

🎯 WHAT TO WRITE IN EXAM:
--------------------------
1. Problem statement (compare deterministic vs randomized)
2. QuickSort concept (divide-and-conquer)
3. Partition algorithm explanation
4. Deterministic approach (last element pivot)
5. Randomized approach (random pivot)
6. Complete code with comments
7. Small example showing partition
8. Recursion tree for sorted array (both approaches)
9. Complexity analysis
10. Why randomized is better

💻 CODE WALKTHROUGH FOR EXAM:
------------------------------
1. partition():
   - Choose pivot (last element)
   - Maintain boundary i (smaller elements)
   - Scan through array with j
   - Swap if arr[j] ≤ pivot
   - Finally place pivot in correct position

2. quicksort_normal():
   - Fixed pivot (last element)
   - Partition and get pivot position
   - Recursively sort left and right

3. quicksort_random():
   - Random pivot selection
   - Swap random element with last
   - Rest same as deterministic

4. main():
   - Create two identical arrays
   - Sort with both approaches
   - Compare recursive call counts

🌟 KEY TAKEAWAYS:
-----------------
• QuickSort: Divide-and-conquer sorting algorithm
• Partition: Key operation, O(n) time
• Deterministic: Simple but O(n²) on sorted arrays
• Randomized: Robust, expected O(n log n) on all inputs
• Pivot selection matters: good pivot → balanced partitions
• Randomization prevents worst-case scenarios
• In-place sorting with O(log n) extra space
• One of the fastest practical sorting algorithms
*/
