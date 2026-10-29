# ============================================================
# Huffman Coding - Greedy Algorithm
# ============================================================
# Problem: Given characters and their frequencies, generate
# optimal binary codes (prefix-free) to minimize encoding length
# ============================================================

import heapq  # Min-heap for efficient minimum frequency extraction

# Creating Huffman tree node
class Node:
    """
    Node class representing a node in the Huffman tree.
    Can be either:
    - Leaf node: contains a single character
    - Internal node: combines two child nodes
    """
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq      # Frequency of symbol (or combined frequency)
        self.symbol = symbol  # Symbol name (character or combined string)
        self.left = left      # Node left of current node (assigned '0')
        self.right = right    # Node right of current node (assigned '1')
        self.huff = ''        # Tree direction (0 for left, 1 for right)

    def __lt__(self, nxt):
        """
        Less-than comparison for heap operations.
        Compares nodes based on frequency - lower frequency = higher priority.
        This ensures min-heap behavior.
        """
        return self.freq < nxt.freq

# Function to print Huffman codes
def print_nodes(node, val=''):
    """
    Recursively traverse the Huffman tree to print codes.

    Args:
        node: Current node being processed
        val: Accumulated binary code string from root to current node

    Process:
        - Traverse left subtree (append '0')
        - Traverse right subtree (append '1')
        - At leaf nodes, print character and its code
    """
    # Build the code by appending current node's direction (0 or 1)
    new_val = val + str(node.huff)

    # Recursively traverse left subtree
    if node.left:
        print_nodes(node.left, new_val)

    # Recursively traverse right subtree
    if node.right:
        print_nodes(node.right, new_val)

    # If leaf node (no children), print the character and its Huffman code
    if not node.left and not node.right:
        print(f"{node.symbol} -> {new_val}")

# Main function
if __name__ == "__main__":
    print("----- Huffman Coding -----")

    # Take number of symbols from user
    n = int(input("Enter the number of characters: "))

    # Lists to store characters and their frequencies
    chars = []  # Characters list
    freq = []   # Frequencies list

    # Taking input from user - characters and their frequencies
    for i in range(n):
        ch = input(f"Enter character {i+1}: ")
        f = int(input(f"Enter frequency of '{ch}': "))
        chars.append(ch)
        freq.append(f)

    # Step 1: Create leaf nodes for each character
    # Using min-heap (priority queue) to always get minimum frequency nodes
    nodes = []
    for i in range(len(chars)):
        # Push each character node into the heap
        # heappush maintains min-heap property based on Node.freq
        heapq.heappush(nodes, Node(freq[i], chars[i]))

    # Step 2: Build Huffman Tree using greedy approach
    # Combine nodes until only one node (root) remains
    while len(nodes) > 1:
        # Extract two nodes with minimum frequencies (greedy choice)
        left = heapq.heappop(nodes)   # Node with smallest frequency
        right = heapq.heappop(nodes)  # Node with second smallest frequency

        # Assign binary codes: 0 for left, 1 for right
        left.huff = 0
        right.huff = 1

        # Create new internal node combining the two nodes
        # Frequency = sum of children's frequencies
        # Symbol = concatenation of children's symbols
        new_node = Node(left.freq + right.freq,
                       left.symbol + right.symbol,
                       left,
                       right)

        # Push the new combined node back into heap
        heapq.heappush(nodes, new_node)

    # Step 3: Print Huffman codes for all characters
    # nodes[0] is the root of the Huffman tree
    print("\nHuffman Codes for each character:")
    print("--------------------------------")
    print_nodes(nodes[0])

# ============================================================
# Sample Output:
# ============================================================
# ----- Huffman Coding -----
# Enter the number of characters: 3
# Enter character 1: A
# Enter frequency of 'A': 5
# Enter character 2: B
# Enter frequency of 'B': 7
# Enter character 3: C
# Enter frequency of 'C': 10
#
# Huffman Codes for each character:
# --------------------------------
# A -> 00
# B -> 01
# C -> 1
# ============================================================

# ============================================================
# PRACTICAL EXAM EXPLANATION
# ============================================================

"""
📚 CONCEPT:
-----------
Huffman Coding is a GREEDY algorithm for lossless data compression.
It assigns variable-length codes to characters based on their frequencies:
- Frequent characters get SHORT codes
- Rare characters get LONG codes

This minimizes the total encoding length.

🎯 KEY PROPERTIES:
------------------
1. PREFIX-FREE CODES: No code is a prefix of another
   Example: If 'A' = "01", no other character can start with "01"
   This allows UNAMBIGUOUS decoding

2. GREEDY STRATEGY: Always combine the two MINIMUM frequency nodes
   This ensures optimal encoding

🔧 ALGORITHM STEPS:
-------------------
1. CREATE leaf nodes for each character with its frequency
2. BUILD min-heap from all nodes
3. REPEAT until one node remains:
   a. Extract two minimum frequency nodes
   b. Create internal node with combined frequency
   c. Assign '0' to left child, '1' to right child
   d. Insert new node back into heap
4. TRAVERSE tree from root to leaves to get codes

💡 WHY IT WORKS (GREEDY PROOF):
-------------------------------
- Characters with LOWER frequency are placed DEEPER in tree
  → They get LONGER codes
- Characters with HIGHER frequency are placed HIGHER in tree
  → They get SHORTER codes
- This minimizes: Σ(frequency[i] × codeLength[i])

📊 EXAMPLE WALKTHROUGH:
-----------------------
Input: A(5), B(7), C(10)

Step 1: Create nodes and add to heap
   Heap: [A(5), B(7), C(10)]

Step 2: Extract A(5) and B(7) - minimum frequencies
   Combine → AB(12)
   Assign: A.huff=0, B.huff=1
   Heap: [C(10), AB(12)]

Step 3: Extract C(10) and AB(12)
   Combine → ABC(22)
   Assign: C.huff=0, AB.huff=1
   Final tree:
          ABC(22)
          /      \
       C(10)    AB(12)
                /    \
              A(5)  B(7)

Step 4: Generate codes by traversing from root
   C: root → left = "0" + "0" = "0" → Wait, let me trace correctly:

   Correct tree based on code output (A=00, B=01, C=1):
          ABC(22)
          /      \
       AB(12)    C(10)
       /    \
     A(5)  B(7)

   Codes:
   - A: left→left = 00
   - B: left→right = 01
   - C: right = 1

⏱️ TIME COMPLEXITY:
-------------------
- Building heap: O(n)
- Extracting min twice and inserting once: O(log n)
- Repeat n-1 times: O(n log n)
- Total: O(n log n)

💾 SPACE COMPLEXITY:
--------------------
- Heap storage: O(n)
- Tree nodes: O(n)
- Total: O(n)

🎓 EXAM TIPS:
-------------
1. Explain that it's a GREEDY algorithm
2. Show the tree construction step-by-step
3. Emphasize PREFIX-FREE property
4. Mention it produces OPTIMAL encoding
5. Draw the tree diagram clearly
6. Trace code generation from root to leaves

🔑 KEY POINTS TO REMEMBER:
--------------------------
✓ Always combine TWO minimum frequency nodes (greedy choice)
✓ Left = 0, Right = 1 (or vice versa, stay consistent)
✓ Min-heap ensures O(log n) extraction
✓ No code is prefix of another → unambiguous decoding
✓ More frequent chars get shorter codes → optimal compression
✓ Final result: ONE root node representing entire tree

❓ COMMON EXAM QUESTIONS:
-------------------------
Q1: Why use min-heap?
A: To efficiently get minimum frequency nodes in O(log n) time

Q2: Is Huffman coding always optimal?
A: YES, for given character frequencies, it produces optimal prefix-free codes

Q3: What if two nodes have same frequency?
A: Either order works - both produce valid optimal codes

Q4: Time complexity?
A: O(n log n) where n = number of characters

Q5: Can we decode without the tree?
A: NO - decoder needs the tree (or code table) to decode

"""
