# AdNabu QA Assignment

## Task 1: Test Design

### A) Product Search (3 test cases)

- **TC-PS-01 (Positive): Search with exact product keyword**  
  Steps: Open store -> search with valid product keyword (e.g., `shirt`) -> submit search.  
  Expected: Relevant products are shown and at least one product card is visible.

- **TC-PS-02 (Negative): Search with invalid/non-existing keyword**  
  Steps: Search using a random string (e.g., `zzzznotaproduct123`).  
  Expected: "No results" state appears and no product cards are listed.

- **TC-PS-03 (Edge): Search with leading/trailing spaces**  
  Steps: Search with `  shirt  ` (extra spaces around keyword).  
  Expected: Input is handled gracefully (trimmed or processed) and relevant results are still returned.

### B) Add to Cart (3 test cases)

- **TC-AC-01 (Positive): Add in-stock product to cart**  
  Steps: Open product detail page for in-stock item -> click **Add to cart**.  
  Expected: Item is added and cart count/cart drawer updates correctly.

- **TC-AC-02 (Negative): Add out-of-stock product to cart**  
  Steps: Open out-of-stock product page -> attempt add to cart.  
  Expected: Add button is disabled or clear stock message is shown; item is not added.

- **TC-AC-03 (Edge): Rapid double-click on Add to cart**  
  Steps: On product page, click **Add to cart** twice quickly.  
  Expected: Cart behavior is deterministic (either quantity increments correctly or duplicate prevention works as designed), no UI crash/error.

## Task 2: Automation (Python + Selenium)

Automated scenario: **Search for a product and add it to the cart successfully**

### Files
- `tests/test_search_add_to_cart.py` - Selenium automation script (modular page object style, explicit waits, no hardcoded sleep)
- `requirements.txt` - Python dependencies
- `reports/latest_run.txt` - generated test execution output

### Setup
1. Install Python 3.10+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run
```bash
python tests/test_search_add_to_cart.py
```

### Expected console output on success
```text
PASS: Product search and add-to-cart flow succeeded.
```

## Test Report

Latest generated report:
- File: `reports/latest_run.txt`
- Result in this environment: **FAILED**
- Failure reason: Browser process launch is blocked in this sandbox (Chrome exits before WebDriver session starts).
- Note: Script is ready; run the same command on a normal local desktop session to execute end-to-end.
