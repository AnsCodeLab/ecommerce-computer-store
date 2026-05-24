# Code Review — Qwen3-8B (local)

```markdown
## High Severity
- **SQL Injection in `checkout` route**: Using `db.execute("INSERT INTO orders ...")` with raw string formatting allows for SQL injection. Use parameterized queries.
- **Missing validation for `customer_id` in `checkout`**: No check for valid `customer_id` exists, leading to potential database errors or incorrect order creation.
- **No input validation for `name` and `email` in `process_checkout`**: Allows for invalid or malicious input, potentially leading to duplicate or invalid customer entries.
- **No error handling for `db.execute` in `process_checkout`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.

## Medium Severity
- **Missing validation for `item_id` in `add_to_cart`**: No check to ensure `item_id` exists, leading to potential errors when retrieving item data.
- **No validation for `quantity` in `add_to_cart`**: Allows for negative or zero quantities, which may lead to incorrect stock management.
- **No validation for `item_id` in `view_cart`**: No check to ensure `item_id` exists, leading to potential errors when retrieving item data.
- **No validation for `quantity` in `view_cart`**: Allows for negative or zero quantities, which may lead to incorrect stock management.
- **No validation for `item_id` in `item_detail`**: No check to ensure `item_id` exists, leading to potential errors when retrieving item data.
- **No validation for `item_id` in `storefront`**: No check to ensure `item_id` exists, leading to potential errors when retrieving item data.
- **No validation for `item_id` in `checkout`**: No check to ensure `item_id` exists, leading to potential errors when retrieving item data.

## Low Severity
- **No error handling for `db.execute` in `get_items`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
- **No error handling for `db.execute` in `get_item`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
- **No error handling for `db.execute` in `create_item`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
- **No error handling for `db.execute` in `delete_item`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
- **No error handling for `db.execute` in `get_customers`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
- **No error handling for `db.execute` in `get_customer`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
- **No error handling for `db.execute` in `create_customer`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
- **No error handling for `db.execute` in `delete_customer`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
- **No error handling for `db.execute` in `get_orders`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
- **No error handling for `db.execute` in `get_order`**: If `db.execute` fails, the transaction is not rolled back, leading to inconsistent data.
```

---
**Controller note (Claude):** The "SQL injection in checkout" High finding is a FALSE POSITIVE — all queries use parameterized `?` placeholders, not string formatting. The legitimate finding (no guard against non-positive quantity) was fixed + covered by `test_checkout_rejects_negative_quantity`. Remaining items (per-route input validation, web-checkout stock guard, DELETE-on-missing → 404) are noted as future hardening for this demo.
