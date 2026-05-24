# E-Commerce Computer Store — Design Spec
## Goal
Build a minimal e-commerce platform for a computer store using Flask and SQLite, featuring a REST API for managing products, customers, and orders, alongside a simple server-rendered web interface for browsing, purchasing, and checkout.

## Data Model (SQLite)
Tables with columns and types:
- categories(id PK, name UNIQUE)
- items(id PK, name, description, price REAL, stock INT, category_id FK)
- customers(id PK, name, email UNIQUE)
- orders(id PK, customer_id FK, status, created_at)
- order_items(id PK, order_id FK, item_id FK, quantity INT, unit_price REAL)

## REST API
| Method | Path              | Body                     | Response              | Status         |
|--------|------------------|---------------------------|------------------------|----------------|
| GET    | /api/categories   | -                         | list of categories     | 200            |
| GET    | /api/categories/<id> | -                         | category details      | 200            |
| POST   | /api/categories | name                      | created category       | 201            |
| DELETE | /api/categories/<id> | -                         | deleted category      | 204            |
| GET    | /api/items       | -                         | list of items          | 200            |
| GET    | /api/items/<id>  | -                         | item details          | 200            |
| POST   | /api/items        | name, description, price, stock, category_id | created item | 201            |
| DELETE | /api/items/<id>   | -                         | deleted item          | 204            |
| GET    | /api/customers    | -                         | list of customers     | 200            |
| GET    | /api/customers/<id> | -                         | customer details     | 200            |
| POST   | /api/customers    | name, email               | created customer      | 201            |
| DELETE | /api/customers/<id> | -                         | deleted customer     | 204            |
| POST   | /api/checkout     | customer_id + list of {item_id, quantity} | order details | 201            |
| GET    | /api/orders      | -                         | list of orders        | 200            |
| GET    | /api/orders/<id>  | -                         | order details         | 200            |

## Web Pages
- GET /storefront (items grouped by category)
- GET /item/<id> detail
- GET /cart, POST /cart/add
- GET /checkout, POST /checkout

## Module Layout
app/__init__.py (app factory create_app(db_path)), app/db.py (connection + schema init + seed), app/categories.py, app/items.py, app/customers.py, app/orders.py (checkout logic), app/web.py (HTML pages), tests/ (pytest + Flask test client, one test file per module, TDD).

## Testing
pytest with Flask test client; in-memory or temp-file SQLite per test; TDD red-green-refactor per module.