// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

// ============================================================
// Bank Smart Contract
// Operations: Deposit | Withdraw | Show Balance
// Deploy on: Remix IDE → Injected Provider (MetaMask testnet)
//            or Remix VM for local testing
// ============================================================

contract Bank {

    // Maps each wallet address to its balance
    mapping(address => uint) private balances;

    // ── Events (emitted on every transaction) ────────────────
    event Deposited(address indexed account, uint amount);
    event Withdrawn(address indexed account, uint amount);

    // ── Show Balance ─────────────────────────────────────────
    // view → does not modify state, no gas cost when called externally
    function getBalance() public view returns (uint) {
        return balances[msg.sender];
    }

    // ── Deposit Money ─────────────────────────────────────────
    function deposit(uint amount) public payable {
        // require(msg.value == amount); // uncomment for ETH-backed deposits
        require(amount > 0, "Deposit amount must be greater than zero");
        balances[msg.sender] += amount;
        emit Deposited(msg.sender, amount);
    }

    // ── Withdraw Money ────────────────────────────────────────
    function withdraw(uint amount) public payable {
        require(amount > 0, "Withdrawal amount must be greater than zero");
        require(amount <= balances[msg.sender], "Insufficient balance");
        balances[msg.sender] -= amount;
        // msg.sender.transfer(amount); // uncomment for ETH transfer
        emit Withdrawn(msg.sender, amount);
    }
}

// ============================================================
// HOW TO RUN IN REMIX IDE
// ============================================================

/*
STEP 1: OPEN & COMPILE
----------------------
1. Go to https://remix.ethereum.org
2. Create new file: Bank.sol
3. Copy-paste this entire code
4. Click "Solidity Compiler" tab (left sidebar icon: 📄)
5. Compiler version: Select any between 0.7.0 to 0.8.x
6. Click blue "Compile Bank.sol" button
7. ✅ Green checkmark = compilation successful

STEP 2: DEPLOY CONTRACT
------------------------
1. Click "Deploy & Run Transactions" tab (left sidebar icon: 🚀)
2. Environment: Select "Remix VM (London)" for testing
   (or "Injected Provider - MetaMask" for testnet)
3. Account: Note the address shown (e.g., 0x5B38Da6...)
   This is YOUR account for testing
4. Gas Limit: Leave as default (3000000)
5. Value: Leave as 0 wei
6. Contract dropdown: Select "Bank"
7. Click orange "Deploy" button
8. Check console output for confirmation
9. Under "Deployed Contracts" section, you'll see:
   "BANK AT 0x..." - click to expand

STEP 3: DEPLOYED CONTRACT INTERFACE
-----------------------------------
After deployment, you'll see 3 function buttons:

🔵 getBalance (blue button)
   - No input field
   - Just click to see your balance

🟠 deposit (orange button)
   - Input field: amount (uint256)
   - Enter amount to deposit

🟠 withdraw (orange button)
   - Input field: amount (uint256)
   - Enter amount to withdraw

// ============================================================
// TEST CASES WITH EXACT INPUT/OUTPUT
// ============================================================

═══════════════════════════════════════════════════════════
TEST CASE 1: Check Initial Balance
═══════════════════════════════════════════════════════════
Function: getBalance
Input:    (no input - just click the blue button)

Expected Output:
   0: uint256: 0

Console Output: (none - it's a free read operation)

✅ PASS: Initial balance is 0

═══════════════════════════════════════════════════════════
TEST CASE 2: First Deposit
═══════════════════════════════════════════════════════════
Function: deposit
Input:    5000

Steps:
1. In the "deposit" input field, type: 5000
2. Click orange "transact" button

Expected Console Output:
-----------------------------------------------------------
[vm] from: 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
to: Bank.deposit(uint256) 0xd9145CCE52D386f254917e481eB44e9943F39138
value: 0 wei
data: 0xb6b55f250000000000000000000000000000000000000000000000000000000000001388
logs: [
  {
    "from": "0xd9145CCE52D386f254917e481eB44e9943F39138",
    "topic": "0x2da466a7b24304f47e87fa2e1e5a81b9831ce54fec19055ce277ca2f39ba42c4",
    "event": "Deposited",
    "args": {
      "0": "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4",
      "1": "5000",
      "account": "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4",
      "amount": "5000"
    }
  }
]
status: true ✅
transaction hash: 0x...
gas: 50985 gas
transaction cost: 44335 gas
execution cost: 23263 gas
-----------------------------------------------------------

✅ PASS: Deposit successful, event emitted with amount 5000

═══════════════════════════════════════════════════════════
TEST CASE 3: Verify Balance After Deposit
═══════════════════════════════════════════════════════════
Function: getBalance
Input:    (click button)

Expected Output:
   0: uint256: 5000

✅ PASS: Balance correctly shows 5000

═══════════════════════════════════════════════════════════
TEST CASE 4: Second Deposit (Accumulation)
═══════════════════════════════════════════════════════════
Function: deposit
Input:    3000

Expected Console Output:
-----------------------------------------------------------
status: true ✅
logs: Deposited event
   account: 0x5B38...
   amount: 3000
gas: ~44000 gas
-----------------------------------------------------------

✅ PASS: Second deposit successful

═══════════════════════════════════════════════════════════
TEST CASE 5: Check Accumulated Balance
═══════════════════════════════════════════════════════════
Function: getBalance
Input:    (click button)

Expected Output:
   0: uint256: 8000

Calculation: 5000 + 3000 = 8000

✅ PASS: Balance correctly accumulated

═══════════════════════════════════════════════════════════
TEST CASE 6: Valid Withdrawal
═══════════════════════════════════════════════════════════
Function: withdraw
Input:    2000

Expected Console Output:
-----------------------------------------------------------
status: true ✅
logs: [
  {
    "event": "Withdrawn",
    "args": {
      "account": "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4",
      "amount": "2000"
    }
  }
]
gas: ~30000 gas
-----------------------------------------------------------

✅ PASS: Withdrawal successful, event emitted

═══════════════════════════════════════════════════════════
TEST CASE 7: Verify Balance After Withdrawal
═══════════════════════════════════════════════════════════
Function: getBalance
Input:    (click button)

Expected Output:
   0: uint256: 6000

Calculation: 8000 - 2000 = 6000

✅ PASS: Balance correctly reduced

═══════════════════════════════════════════════════════════
TEST CASE 8: Multiple Small Withdrawals
═══════════════════════════════════════════════════════════
Function: withdraw
Input:    1000

Expected Output: status: true ✅

Then:
Function: withdraw
Input:    500

Expected Output: status: true ✅

Then:
Function: getBalance

Expected Output:
   0: uint256: 4500

Calculation: 6000 - 1000 - 500 = 4500

✅ PASS: Multiple withdrawals work correctly

═══════════════════════════════════════════════════════════
TEST CASE 9: ERROR - Withdraw More Than Balance
═══════════════════════════════════════════════════════════
Function: withdraw
Input:    10000

(Current balance is 4500, trying to withdraw 10000)

Expected Console Output:
-----------------------------------------------------------
❌ transact to Bank.withdraw errored: VM error: revert.

revert
  The transaction has been reverted to the initial state.

Reason provided by the contract: "Insufficient balance"

Debug:
  Transaction reverted
  Gas estimation failed
-----------------------------------------------------------

✅ PASS: Transaction correctly REJECTED with error message

═══════════════════════════════════════════════════════════
TEST CASE 10: ERROR - Deposit Zero Amount
═══════════════════════════════════════════════════════════
Function: deposit
Input:    0

Expected Console Output:
-----------------------------------------------------------
❌ transact to Bank.deposit errored: VM error: revert.

Reason: "Deposit amount must be greater than zero"
-----------------------------------------------------------

✅ PASS: Zero deposit correctly rejected

═══════════════════════════════════════════════════════════
TEST CASE 11: ERROR - Withdraw Zero Amount
═══════════════════════════════════════════════════════════
Function: withdraw
Input:    0

Expected Console Output:
-----------------------------------------------------------
❌ transact to Bank.withdraw errored: VM error: revert.

Reason: "Withdrawal amount must be greater than zero"
-----------------------------------------------------------

✅ PASS: Zero withdrawal correctly rejected

═══════════════════════════════════════════════════════════
TEST CASE 12: Large Number Deposit
═══════════════════════════════════════════════════════════
Function: deposit
Input:    999999999999999

Expected Output:
   status: true ✅
   Deposited event with amount: 999999999999999

Then:
Function: getBalance

Expected Output:
   0: uint256: 1000000000004499

Calculation: 4500 (previous) + 999999999999999

✅ PASS: Large numbers handled correctly

═══════════════════════════════════════════════════════════
TEST CASE 13: Withdraw Exact Balance (Edge Case)
═══════════════════════════════════════════════════════════
First, check current balance:
Function: getBalance
Output: (let's say it shows 1000000000004499)

Then withdraw exact amount:
Function: withdraw
Input:    1000000000004499

Expected Output:
   status: true ✅

Then verify:
Function: getBalance

Expected Output:
   0: uint256: 0

✅ PASS: Can withdraw exact balance, leaving 0

═══════════════════════════════════════════════════════════
TEST CASE 14: Multi-Account Testing
═══════════════════════════════════════════════════════════
Step 1: Current account deposits
Function: deposit
Input:    5000
Output: status: true ✅

Step 2: Check balance
Function: getBalance
Output: 5000

Step 3: Switch account
- In "Account" dropdown at top, select different address
  (e.g., 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2)

Step 4: Check balance with new account
Function: getBalance
Output: 0

✅ PASS: Each account has separate balance

Step 5: Deposit with second account
Function: deposit
Input:    3000
Output: status: true ✅

Step 6: Check second account balance
Function: getBalance
Output: 3000

Step 7: Switch back to first account
Function: getBalance
Output: 5000

✅ PASS: Balances are isolated per account

// ============================================================
// COMPLETE TEST SEQUENCE (QUICK COPY-PASTE)
// ============================================================

// Initial state
getBalance() → 0

// Make deposits
deposit(5000) → ✅ Event: Deposited(address, 5000)
getBalance() → 5000

deposit(3000) → ✅ Event: Deposited(address, 3000)
getBalance() → 8000

// Make withdrawals
withdraw(2000) → ✅ Event: Withdrawn(address, 2000)
getBalance() → 6000

withdraw(1000) → ✅
getBalance() → 5000

// Test error cases
withdraw(10000) → ❌ "Insufficient balance"
deposit(0) → ❌ "Deposit amount must be greater than zero"
withdraw(0) → ❌ "Withdrawal amount must be greater than zero"

// Withdraw remaining balance
withdraw(5000) → ✅
getBalance() → 0

// ============================================================
// GAS COSTS (Approximate)
// ============================================================

Contract Deployment:        ~250,000 gas
First deposit():            ~45,000 gas
Subsequent deposit():       ~28,000 gas
First withdraw():           ~30,000 gas
Subsequent withdraw():      ~15,000 gas
getBalance():               FREE (view function, no gas)

Note: Actual gas costs vary based on:
- Network congestion
- Compiler optimizations
- Storage operations

// ============================================================
// UNDERSTANDING THE REMIX INTERFACE
// ============================================================

DEPLOYED CONTRACTS PANEL:
-------------------------
After deployment, you'll see:

BANK AT 0xd9145CCE52D386f254917e481eB44e9943F39138
  ↓ (click to expand)

  🔵 getBalance        ← Blue = read-only (FREE)
      [call]
      ↓ 0: uint256: 0

  🟠 deposit           ← Orange = state-changing (COSTS GAS)
      amount: [_____]
      [transact]

  🟠 withdraw          ← Orange = state-changing (COSTS GAS)
      amount: [_____]
      [transact]

LOW LEVEL INTERACTIONS:
-----------------------
Value: [0] wei        ← Amount of ETH to send
Gas limit: [3000000]  ← Max gas for transaction
Balance: 0 wei        ← Contract's ETH balance

CONSOLE OUTPUT:
---------------
Shows detailed transaction information:
- Transaction hash
- From/To addresses
- Gas used
- Events emitted
- Success/Failure status
- Error messages (if any)

// ============================================================
// BUTTON COLOR MEANINGS
// ============================================================

🔵 BLUE BUTTON = view/pure function
   - Does NOT change blockchain state
   - FREE to call (no gas cost)
   - Returns data immediately
   - Example: getBalance()

🟠 ORANGE BUTTON = state-changing function
   - MODIFIES blockchain state
   - COSTS GAS to execute
   - Creates a transaction
   - Example: deposit(), withdraw()

🔴 RED BUTTON = payable + state-changing
   - Same as orange but accepts ETH
   - Currently our deposit/withdraw are orange
   - Would be red if msg.value checks were uncommented

// ============================================================
// COMMON ERRORS & SOLUTIONS
// ============================================================

ERROR: "Insufficient balance"
CAUSE: Trying to withdraw more than deposited
FIX:   Deposit more or withdraw less
       Use getBalance() to check current balance

ERROR: "Deposit amount must be greater than zero"
CAUSE: Entered 0 in deposit field
FIX:   Enter positive number (1 or higher)

ERROR: "Withdrawal amount must be greater than zero"
CAUSE: Entered 0 in withdraw field
FIX:   Enter positive number (1 or higher)

ERROR: "Gas estimation failed"
CAUSE: Transaction will revert (above errors)
FIX:   Check your input values meet requirements

ERROR: "Transaction has been reverted"
CAUSE: A require() statement failed
FIX:   Read the "Reason provided by contract" message

// ============================================================
// TIPS & BEST PRACTICES
// ============================================================

1. Always check balance before withdrawing
   - Call getBalance() first
   - Ensure you have sufficient funds

2. Start with small amounts when testing
   - Use 100, 500, 1000 for initial tests
   - Test edge cases separately

3. Watch the console output
   - Green checkmark ✅ = success
   - Red X ❌ = failure
   - Read event logs for details

4. Test error cases
   - Verify validations work correctly
   - Ensures contract security

5. Try multiple accounts
   - Switch accounts in dropdown
   - Verify balances are isolated

6. Note gas costs
   - First operations cost more (storage initialization)
   - Subsequent operations cheaper

// ============================================================
// WHAT EACH FUNCTION DOES
// ============================================================

getBalance()
------------
PURPOSE:  Check your current balance in the bank
INPUT:    None (automatically uses your address)
OUTPUT:   Your balance as uint256
GAS COST: Free (read-only)
EXAMPLE:  getBalance() returns 5000

deposit(uint amount)
--------------------
PURPOSE:  Add money to your bank account
INPUT:    amount - positive integer
OUTPUT:   None (check console for event)
GAS COST: ~28,000-45,000 gas
EXAMPLE:  deposit(1000) adds 1000 to your balance
EVENT:    Emits Deposited(your_address, 1000)

withdraw(uint amount)
---------------------
PURPOSE:  Remove money from your bank account
INPUT:    amount - positive integer ≤ your balance
OUTPUT:   None (check console for event)
GAS COST: ~15,000-30,000 gas
EXAMPLE:  withdraw(500) removes 500 from balance
EVENT:    Emits Withdrawn(your_address, 500)

// ============================================================
// CONCEPT EXPLANATIONS
// ============================================================

MAPPING:
--------
mapping(address => uint) private balances;

Think of it as a database table:
┌──────────────────────────┬──────────┐
│ Address (Key)            │ Balance  │
├──────────────────────────┼──────────┤
│ 0x5B38Da6a701c568...     │ 5000     │
│ 0xAb8483F64d9C6d1...     │ 3000     │
│ 0x4B20993Bc481177...     │ 0        │
└──────────────────────────┴──────────┘

EVENTS:
-------
event Deposited(address indexed account, uint amount);

Events are cheaper than storage and create searchable logs.
Used by:
- Block explorers (Etherscan)
- Frontend applications
- Analytics tools

MSG.SENDER:
-----------
msg.sender is the address calling the function.
- If you call deposit(): msg.sender = your address
- Each transaction has a different msg.sender
- Used to identify which account's balance to update

REQUIRE():
----------
require(condition, "error message");

If condition is false:
- Transaction is reverted
- No state changes are saved
- Gas is still consumed
- Error message is shown

Example:
require(amount > 0, "Must be positive");
// If amount is 0 or negative, transaction fails

// ============================================================
// NEXT STEPS / ENHANCEMENTS
// ============================================================

Once you understand this basic bank, try adding:

1. Interest calculation
   - Add timestamp tracking
   - Calculate interest based on time

2. Transaction history
   - Store array of deposits/withdrawals
   - Add function to view history

3. Admin functions
   - Owner can pause contract
   - Emergency withdraw function

4. Multi-currency support
   - Support different token types
   - Add exchange rates

5. Transfer between accounts
   - Send money to another address
   - Add transfer() function

*/
