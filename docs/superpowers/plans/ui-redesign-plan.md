1. Create `app/static/css/style.css` with color palette, typography, spacing, and button styles as per design spec.
2. Create `app/templates/base.html` with sticky navbar, footer, and content block.
3. Create `app/templates/index.html` with hero banner, category filter, and responsive product card grid.
4. Create `app/templates/item_detail.html` with large image, product details, and add-to-cart button.
5. Create `app/templates/cart.html` with cart table, totals, and empty state message.
6. Create `app/templates/checkout.html` with checkout form, order summary, and submit button.
7. Create `app/templates/confirmation.html` with order confirmation message, order ID, and total.
8. Refactor `app/web.py` to use `render_template` instead of `render_template_string`, ensure all routes and behavior remain identical.
9. Pass `cart_count` to all templates from `web.py` to display in navbar.