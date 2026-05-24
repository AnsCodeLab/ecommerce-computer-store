```markdown
# Design Spec: Modern E-Commerce Storefront

## Visual Identity
- **Color Palette**:
  - Primary: `#1E3A8A` (navy)
  - Secondary: `#3B82F6` (blue)
  - Accent: `#EF4444` (red)
  - Background: `#F9FAFB` (light gray)
  - Text: `#111827` (dark)
- **Typography**:
  - Font: `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif`
- **Spacing Scale**:
  - 0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64 (px)

## Layout Components
- **Sticky Navbar**:
  - Brand logo + nav links (Home, Items, Cart)
  - Cart badge showing item count
- **Hero Banner**:
  - Full-width, centered text with CTA button
- **Category Filter**:
  - Sidebar with clickable categories (e.g. Laptops, Monitors)
- **Responsive Product-Card Grid**:
  - 3 columns (tablet+), 2 columns (mobile)
  - Card includes: image (emoji placeholder), name, price, stock badge
- **Product Detail Page**:
  - Large image (emoji), name, description, price, add-to-cart button
- **Cart Table**:
  - Product name, price, quantity, remove button
  - Total price and checkout button
- **Checkout Form**:
  - Form fields: name, email
  - Order summary (items, total)
  - Submit button
- **Confirmation Page**:
  - Order confirmation message
  - Order ID and total
- **Footer**:
  - Site info, copyright, links

## Interaction & Polish
- **Card Hover**: Scale up slightly, highlight border
- **Stock Badges**:
  - In stock: `In Stock` (green)
  - Low stock: `Low Stock` (yellow)
  - Out of stock: `Out of Stock` (red)
- **Button Styles**:
  - Primary: `#3B82F6` with white text, rounded
  - Secondary: `#EF4444` with white text, rounded
- **Empty Cart State**:
  - Display message: "Your cart is empty"
- **Responsive Breakpoints**:
  - Mobile: `max-width: 600px`
  - Tablet: `min-width: 600px`
  - Desktop: `min-width: 1024px`
```