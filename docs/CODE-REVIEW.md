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

---

## UI Rework Review (2026-05-24)

Reworked the bare `render_template_string` storefront into a production-style templated UI
(navy/blue theme, sticky navbar with cart badge, hero, responsive product-card grid with
stock badges, item detail, cart table, two-column checkout with order summary, confirmation
panel, footer). Driven through the flow: brainstorm → design spec → plan → implement → review,
with Qwen3-8B as the generation engine and Claude as the controller running tests + fixing forward.

**Model self-review findings & resolution:**
- _Accessibility (valid):_ decorative emoji not hidden from screen readers, thumbnails/cart link
  unlabeled → **fixed** (`aria-hidden` on emoji, `aria-label` on thumb + cart links).
- _"`_cart_lines` doesn't check item exists"_ → **false positive** (guarded by `if not row: continue`).
- _"checkout doesn't update stock"_ → **false positive** (it decrements `items.stock` per line).
- _"`<html>` lacks lang"_ → **false positive** (`<html lang="en">` is present).

**Controller-fixed 8B mistakes during generation:**
- CSS-selector dot notation written into HTML `class` attrs (`class="btn.accent"` → `class="btn accent"`).
- Invalid Jinja filter syntax `{{ x | '%.2f'|format }}` → `{{ '%.2f'|format(x) }}`.
- `<form>` placed as a direct child of `<tbody>` (invalid) → moved into a table cell.
- `category.items` in Jinja resolved to the dict's `.items()` method → renamed key to `products`.
- Double `.container` nesting and a misplaced `<h2>` inside the product grid → restructured.
- Non-idempotent `seed()` duplicated the catalog on restart → guarded to seed only when empty.
