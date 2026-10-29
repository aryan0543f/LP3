// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// ============================================================
// Student Data Smart Contract
// Demonstrates: Structures | Arrays | Fallback | Modifier
// Deploy on Remix IDE and observe Gas & Transaction Fee
// ============================================================

contract StudentData {

    // ── Structure ─────────────────────────────────────────────
    // Defines a Student with ID, name, and marks (array of 2)
    struct Student {
        int     ID;
        string  fName;
        string  lName;
        int[2]  marks;   // fixed-size array: [subject1, subject2]
    }

    // ── State Variables ───────────────────────────────────────
    address owner;
    int public stdCount = 0;

    // Mapping: student number → Student record
    mapping(int => Student) public stdRecords;

    // ── Modifier ──────────────────────────────────────────────
    // Restricts function access to contract owner only
    modifier onlyOwner {
        require(owner == msg.sender, "Only owner can add records");
        _;
    }

    // ── Constructor ───────────────────────────────────────────
    // Sets the deployer as the owner
    constructor() {
        owner = msg.sender;
    }

    // ── Fallback Function ─────────────────────────────────────
    // Called when contract receives ETH with no matching function
    // or when called with unknown function signature
    fallback() external payable { }

    // ── Add New Student Record ────────────────────────────────
    function addNewRecords(
        int           _ID,
        string memory _fName,
        string memory _lName,
        int[2] memory _marks
    ) public onlyOwner {
        stdCount = stdCount + 1;                                    // increment counter
        stdRecords[stdCount] = Student(_ID, _fName, _lName, _marks); // store record
    }
}

// ── Concepts Used ─────────────────────────────────────────────
// struct     : Groups related data (ID, name, marks) into one type
// int[2]     : Fixed-size array storing marks for 2 subjects
// mapping    : Key-value store — stdCount → Student
// modifier   : Reusable access control (onlyOwner)
// fallback   : Catches any ETH sent directly to the contract
// constructor: Runs once at deployment to set the owner

// ============================================================
// HOW TO RUN IN REMIX IDE
// ============================================================

/*
STEP 1: OPEN & COMPILE
----------------------
1. Go to https://remix.ethereum.org
2. Create new file: StudentData.sol
3. Copy-paste this entire code
4. Click "Solidity Compiler" tab (left sidebar)
5. Select compiler: 0.8.0 or higher
6. Click "Compile StudentData.sol"
7. Green checkmark = success

STEP 2: DEPLOY CONTRACT
-----------------------
1. Click "Deploy & Run Transactions" tab
2. Environment: Select "Remix VM (London)" for testing
3. Account: Note the selected account (this becomes owner)
4. Contract: Select "StudentData" from dropdown
5. Click orange "Deploy" button
6. Check console: "creation of StudentData pending..."
7. Under "Deployed Contracts", expand "STUDENTDATA AT 0x..."

STEP 3: INTERACT WITH DEPLOYED CONTRACT
---------------------------------------
You'll see these functions:

🔵 stdCount (blue button)
   - Click to view current student count
   - Returns: 0 initially

🔵 stdRecords (blue button)
   - Input: int256 (student number)
   - Returns: Student details for that number

🟠 addNewRecords (orange button)
   - Adds a new student record
   - Only owner can call this

// ============================================================
// TEST CASES WITH INPUT/OUTPUT
// ============================================================

TEST CASE 1: Check Initial Count
---------------------------------
Function: stdCount
Input:    (just click the button, no input needed)
Output:   int256: 0

Expected: Initially 0 students

TEST CASE 2: Add First Student
-------------------------------
Function: addNewRecords
Inputs:
   _ID:     101
   _fName:  "John"
   _lName:  "Doe"
   _marks:  [85, 90]

Steps:
1. Enter _ID: 101
2. Enter _fName: "John" (with quotes)
3. Enter _lName: "Doe" (with quotes)
4. Enter _marks: [85,90] (with brackets, no spaces)
5. Click orange "transact" button

Output (Console):
   status: true ✅
   transaction hash: 0x...
   from: 0x5B38... (your account)
   to: StudentData.addNewRecords(int256,string,string,int256[2])
   gas: ~150000 gas
   transaction cost: ~130000 gas
   execution cost: ~105000 gas

TEST CASE 3: Verify Count Increased
------------------------------------
Function: stdCount
Input:    (click button)
Output:   int256: 1

Expected: Count increased from 0 to 1

TEST CASE 4: Retrieve First Student
------------------------------------
Function: stdRecords
Input:    1

Output:
   0: int256: ID 101
   1: string: fName John
   2: string: lName Doe
   3: int256[2]: marks 85,90

Expected: Returns all details of first student

TEST CASE 5: Add Second Student
--------------------------------
Function: addNewRecords
Inputs:
   _ID:     102
   _fName:  "Alice"
   _lName:  "Smith"
   _marks:  [78, 92]

Output (Console):
   status: true ✅
   gas used: ~130000 gas (slightly less, reusing storage)

TEST CASE 6: Add Third Student
-------------------------------
Function: addNewRecords
Inputs:
   _ID:     103
   _fName:  "Bob"
   _lName:  "Johnson"
   _marks:  [95, 88]

Output: status: true ✅

TEST CASE 7: Check Final Count
-------------------------------
Function: stdCount
Input:    (click button)
Output:   int256: 3

Expected: Total 3 students added

TEST CASE 8: Retrieve Second Student
-------------------------------------
Function: stdRecords
Input:    2

Output:
   0: int256: ID 102
   1: string: fName Alice
   2: string: lName Smith
   3: int256[2]: marks 78,92

TEST CASE 9: Retrieve Third Student
------------------------------------
Function: stdRecords
Input:    3

Output:
   0: int256: ID 103
   1: string: fName Bob
   2: string: lName Johnson
   3: int256[2]: marks 95,88

TEST CASE 10: Try Non-Existent Student
---------------------------------------
Function: stdRecords
Input:    99

Output:
   0: int256: ID 0
   1: string: fName
   2: string: lName
   3: int256[2]: marks 0,0

Expected: Returns empty/default values (student doesn't exist)

TEST CASE 11: Access Control Test (NEGATIVE TEST)
--------------------------------------------------
Steps:
1. In "Account" dropdown, select a DIFFERENT account
2. Try to call addNewRecords with any inputs

Input Example:
   _ID:     104
   _fName:  "Test"
   _lName:  "User"
   _marks:  [70, 75]

Output (Console):
   ❌ transact to StudentData.addNewRecords errored:
   VM error: revert
   Reason: "Only owner can add records"

Expected: Transaction REVERTS because caller is not owner
         This proves the onlyOwner modifier works!

TEST CASE 12: Test Fallback Function
-------------------------------------
Steps:
1. In "Deploy & Run" tab, find "Low level interactions"
2. Set Value: 1 ether
3. Copy deployed contract address
4. In Remix console, send transaction:
   {
     "to": "<contract_address>",
     "value": "1000000000000000000"
   }

Output:
   Transaction succeeds (fallback accepts ETH)
   Contract balance increases by 1 ETH

Note: Fallback function is automatically called

// ============================================================
// EXPECTED GAS COSTS (approximate)
// ============================================================

Contract Deployment:       ~450,000 gas
First addNewRecords:       ~150,000 gas
Subsequent addNewRecords:  ~130,000 gas
stdCount (read):           ~FREE (view function)
stdRecords (read):         ~FREE (view function)

// ============================================================
// SUMMARY OF ALL FUNCTIONS
// ============================================================

PUBLIC FUNCTIONS:
-----------------
1. stdCount()
   - Returns total number of students
   - No input required
   - Free to call (view function)

2. stdRecords(int256 _studentNumber)
   - Returns student details
   - Input: Student number (1, 2, 3, ...)
   - Free to call (view function)

3. addNewRecords(int _ID, string _fName, string _lName, int[2] _marks)
   - Adds new student record
   - Only owner can call
   - Costs gas
   - Automatically increments stdCount

SPECIAL FUNCTIONS:
------------------
- constructor(): Runs once at deployment, sets owner
- fallback(): Accepts ETH sent to contract

// ============================================================
// QUICK REFERENCE: REMIX BUTTON COLORS
// ============================================================

🔵 BLUE = Read-only (view/pure) → FREE, no gas
🟠 ORANGE = State-changing → COSTS GAS
🔴 RED = Payable + state-changing → COSTS GAS + accepts ETH

// ============================================================
// COMPLETE TEST SEQUENCE (COPY-PASTE READY)
// ============================================================

// 1. Check initial count
stdCount() → 0

// 2. Add student 1
addNewRecords(101, "John", "Doe", [85,90])

// 3. Verify count
stdCount() → 1

// 4. Retrieve student 1
stdRecords(1) → 101, "John", "Doe", [85,90]

// 5. Add student 2
addNewRecords(102, "Alice", "Smith", [78,92])

// 6. Add student 3
addNewRecords(103, "Bob", "Johnson", [95,88])

// 7. Final count
stdCount() → 3

// 8. Retrieve student 2
stdRecords(2) → 102, "Alice", "Smith", [78,92]

// 9. Retrieve student 3
stdRecords(3) → 103, "Bob", "Johnson", [95,88]

// 10. Test access control (switch account first)
addNewRecords(104, "Test", "User", [70,75]) → ❌ REVERTS

// ============================================================
// TROUBLESHOOTING
// ============================================================

ERROR: "Only owner can add records"
CAUSE: You switched accounts
FIX:   Switch back to the account that deployed the contract

ERROR: Gas estimation failed
CAUSE: Function will revert (likely wrong account)
FIX:   Check you're using owner account

ERROR: Invalid array format
CAUSE: Wrong syntax for marks array
FIX:   Use [85,90] not 85,90 or "85,90"

ERROR: String not properly formatted
CAUSE: Missing quotes around strings
FIX:   Use "John" not John

*/
