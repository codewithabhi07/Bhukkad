# 📘 Student Code Walkthrough & Explanation Guide
## Lucky Traders - Full-Stack Python & SQL Web Application

> **Purpose of this Guide:**  
> This guide is specially created for college students and graduates. It explains the entire codebase in **simple, beginner-friendly terms** so you can easily understand, walk through, and explain every file to your professors, internal evaluators, and external examiners during project evaluations and viva voce.

---

## 🗂️ 1. Project Folder & File Structure

Here is how the project is organized:

```
Bhukkad/
│
├── 🐍 Backend & Database
│   ├── app.py                  # Main Flask Web Server & REST API Routes
│   ├── db.py                   # SQL Database Helper Functions (sqlite3)
│   ├── lucky_traders.db        # The actual SQLite Database File
│   ├── requirements.txt        # Python dependencies (Flask)
│   └── database/
│       ├── schema.sql          # SQL Table Definitions (5 relational tables)
│       └── seed.sql            # Initial sample data (20 products & users)
│
├── 🎨 Frontend (Client-Side)
│   ├── style.css               # Clean Master Stylesheet (Colors, Cards, Tables, Modals)
│   ├── app.js                  # Shared JavaScript (Cart, Checkout Modal, Login Session)
│   ├── upi_qr.jpg              # Official Google Pay UPI QR (Ashwini Bramhankar)
│   ├── index.html              # Store Homepage (Category cards, search bar, product catalog)
│   ├── masala.html             # Masalas Category Price List Table
│   ├── chutney.html            # Chutneys Category Price List Table
│   ├── pickle.html             # Pickles Category Price List Table
│   ├── login.html              # Customer Login, Admin Login & Registration
│   ├── admin.html              # Admin Dashboard (Categories, Customers, Orders, Stock)
│   └── receipt.html            # GST Tax Invoice Receipt Generator
│
└── 🧪 Testing & Documentation
    ├── test_app.py             # 8 Automated Unit Tests (unittest)
    ├── README.md               # Quick start guide
    ├── PROJECT_REPORT_SPPU_CS331FP.md  # 6-Chapter Syllabus Project Report (SPPU CS-331-FP)
    ├── COLLEGE_PRESENTATION_SCRIPT.md  # 5-minute speaking script & Viva questions
    └── CODE_EXPLANATION_GUIDE.md       # This file!
```

---

## 💻 2. File-by-File Explanation (What Every File Does)

### 1. `app.py` (Backend Controller)
- **What is it?**  
  It is the **brain of the server**. It uses **Python Flask** to listen for web requests (on port 5000).
- **Key Concepts to Explain:**
  1. **Serves HTML Pages:** When you open `http://localhost:5000/`, it serves `index.html`.
  2. **Exposes REST APIs:**
     - `/api/products` (GET): Sends the list of all 20 products as JSON.
     - `/api/orders` (POST): Accepts an order from the cart, saves it in SQL, and decrements stock.
     - `/api/auth/login` (POST): Checks username and password against the database.
     - `/api/admin/...`: Admin endpoints for adding/removing categories, managing stock, and viewing orders.
  3. **CORS Headers (`@app.after_request`):** Allows browsers to communicate with the server without security cross-origin blocking.

---

### 2. `db.py` (Database Model Layer)
- **What is it?**  
  It contains **pure Python SQL functions** using the standard library `sqlite3`. No heavy ORMs are needed—just clean SQL queries.
- **Key Functions to Explain:**
  - `get_connection()`: Connects to `lucky_traders.db` and enables `sqlite3.Row` (so database rows behave like Python dictionaries).
  - `get_products(...)`: Runs `SELECT * FROM products JOIN categories ...` with optional category filters or search terms.
  - `create_order(...)`: Runs an **atomic SQL transaction**:
    1. Inserts customer details into `orders`.
    2. Inserts each item into `order_items`.
    3. Executes `UPDATE products SET stock_qty = stock_qty - ?` to automatically reduce inventory.
  - `authenticate_user(username, password)`: Queries `users` table to match credentials.

---

### 3. `database/schema.sql` (Database Design)
- **What is it?**  
  The blueprint defining the **5 relational database tables**:
  1. `users`: Stores `id`, `username`, `password_hash`, `full_name`, `role` (`customer` or `admin`).
  2. `categories`: Stores `id`, `name`, `slug` (`masalas`, `chutneys`, `pickles`), `icon`.
  3. `products`: Stores `category_id` (foreign key), `name`, `marathi_name`, `price_1kg`, `price_250g`, `image_url`, `stock_qty`.
  4. `orders`: Stores `order_number`, `user_id`, `customer_name`, `payment_method`, `subtotal`, `cgst`, `sgst`, `total_amount`, `status`.
  5. `order_items`: Line items linking each ordered product, selected weight (`1 Kg` or `250 Gm`), and quantity to the parent order using foreign keys.

---

### 4. `app.js` (Frontend Brain)
- **What is it?**  
  The shared client-side script included on every page. It handles four key tasks:
  1. **`Cart` Object:**
     - Saves cart items to the browser's `localStorage` so items don't disappear if you refresh the page.
     - Automatically calculates **2.5% CGST** and **2.5% SGST** live.
     - Renders item photos, selected weights, and `+`/`-` quantity controls inside the sliding drawer.
  2. **`Auth` Object:**
     - Remembers who is logged in (`lalit` or `admin`).
     - Updates the top navigation bar to say *"Namaste, [Name]"* and shows the *"Admin Portal"* link if the user is an admin.
  3. **Auto-UI Injection (`ensureCartAndCheckoutMarkup`):**
     - Automatically injects the sliding cart drawer and checkout modal into any page that needs it! This prevents duplicating 100+ lines of HTML across multiple files.
  4. **`submitOrder()`:**
     - Sends the cart items, customer address, and payment method (COD or UPI) to `/api/orders` using `fetch()`. Then redirects to `receipt.html`.

---

### 5. `style.css` (Visual Design)
- **What is it?**  
  A clean, modular 475-line stylesheet that gives the application its warm Indian gourmet spice appearance.
- **Key Sections:**
  1. **Theme Variables (`:root`):** Deep navy blue (`#0a3d62`), spice chili red (`#c0392b`), and saffron turmeric (`#d35400`).
  2. **Product Grid:** Responsive CSS Grid (`repeat(auto-fill, minmax(260px, 1fr))`) that automatically adapts to phones, tablets, and desktops.
  3. **Sliding Cart Drawer:** Fixed position drawer with smooth CSS slide-in animation (`right: 0`).
  4. **Print Media Query (`@media print`):** Hides the navbar, buttons, and footer when printing the tax invoice receipt.

---

### 6. The HTML Pages
- **`index.html`:** The main shop page. Has category cards, real-time search, category filter tabs, and dynamic product cards with dual weight buttons (`1 Kg` & `250 Gm`).
- **`masala.html`, `chutney.html`, `pickle.html`:** Dedicated category pages displaying neat price list tables with instant order buttons.
- **`login.html`:** Clean 3-tab portal for **Customer Login**, **Admin Login**, and **Customer Registration**.
- **`admin.html`:** Admin dashboard with 4 distinct sections:
  1. Categories (Add & Remove)
  2. Customer Data (View accounts, order counts & total spent)
  3. Order Data (View live orders, change status from Confirmed to Delivered)
  4. Available Stock (Live inventory count, update quantity, add/remove products)
- **`receipt.html`:** GST tax invoice bill displaying items, tax breakdown, and a **Print Receipt** button.

---

## 🔄 3. How Data Flows (The Big Picture)

```
[Customer Browser]
       │
       ▼ (1. Clicks "Add to Basket")
[app.js (Cart in LocalStorage)]
       │
       ▼ (2. Clicks "Confirm Order" -> fetch('/api/orders', POST))
[app.py (Flask Server Route)]
       │
       ▼ (3. Calls db.create_order())
[db.py (Python SQLite Helper)]
       │
       ▼ (4. Executes SQL Transaction)
[lucky_traders.db (SQLite Database)]
       │   - Inserts order & items
       │   - Decrements stock: UPDATE products SET stock_qty = stock_qty - qty
       │
       ▼ (5. Returns order_number: "ORD-1234")
[receipt.html?order=ORD-1234]
       │
       ▼ (6. Fetches order details and prints GST Tax Invoice)
[Customer Receives Bill]
```

---

## 🎯 4. Top 7 Viva Questions & How to Answer

### Q1: "Why did you choose SQLite instead of MySQL or MongoDB?"
> **Answer:**  
> "SQLite is a zero-configuration, serverless, ACID-compliant relational SQL database engine that is built directly into Python's standard library (`sqlite3`). It requires no separate database server process, stores all data in a single file (`lucky_traders.db`), and supports standard SQL syntax, foreign keys, and transactions. For a college project or local merchant application, it is lightweight, extremely fast, and highly reliable."

---

### Q2: "How is SQL Injection prevented in your project?"
> **Answer:**  
> "We use **parameterized queries** with placeholder question marks (`?`) in all database queries inside `db.py`.  
> For example: `cursor.execute('SELECT * FROM products WHERE id = ?', (prod_id,))`.  
> Because user input is passed as query parameters rather than string concatenation, malicious SQL code cannot be executed."

---

### Q3: "How does the Dual-Weight pricing work?"
> **Answer:**  
> "In our `products` table, each product has two price columns: `price_1kg` and `price_250g`.  
> On the frontend (`index.html`), clicking the `1 Kg` or `250 Gm` buttons toggles the displayed price. When added to the cart, the selected weight is saved along with the corresponding unit price."

---

### Q4: "How does the shopping cart remember items when you reload the page?"
> **Answer:**  
> "We use the browser's `window.localStorage` API inside `app.js`. When a product is added or removed, the array is converted to a JSON string using `JSON.stringify()` and stored under the key `'lucky_traders_cart'`. On page load, `JSON.parse()` restores the cart items."

---

### Q5: "How is stock automatically reduced when an order is placed?"
> **Answer:**  
> "Inside `create_order()` in `db.py`, for every item in the order, we execute:  
> `UPDATE products SET stock_qty = MAX(0, stock_qty - ?), in_stock = CASE WHEN stock_qty - ? <= 0 THEN 0 ELSE 1 END WHERE id = ?`  
> This happens inside the same database transaction as the order creation, ensuring inventory is kept accurate in real time."

---

### Q6: "How did you prevent code duplication between HTML files?"
> **Answer:**  
> "Instead of copy-pasting the 100-line checkout modal and sliding cart drawer into every HTML file, `app.js` has a function called `ensureCartAndCheckoutMarkup()`. When any page loads, `app.js` checks if the cart drawer exists, and if not, injects it dynamically into the DOM. This adheres to the **DRY (Don't Repeat Yourself)** principle of software engineering."

---

### Q7: "What automated testing did you implement?"
> **Answer:**  
> "We implemented an automated test suite using Python's standard `unittest` library in `test_app.py`. It tests 8 critical operations:
> 1. API health check
> 2. Category retrieval
> 3. Product catalog count (20 products)
> 4. Customer and Admin login authentication
> 5. Category creation and deletion (CRUD)
> 6. Admin customer data retrieval
> 7. End-to-end order placement and atomic stock decrement
> 8. Admin inventory stock update  
> All 8 tests pass in less than 0.05 seconds."

---

## 🚀 5. How to Run the Project for Your Demo

1. Open your terminal in the project directory:
   ```powershell
   cd "c:\Users\lalit\OneDrive\Desktop\New folder (2)\Bhukkad"
   ```
2. Start the Python Flask Server:
   ```powershell
   python app.py
   ```
3. Open your web browser and go to:
   - **Storefront:** [http://localhost:5000](http://localhost:5000)
   - **Login Page:** [http://localhost:5000/login.html](http://localhost:5000/login.html)
   - **Admin Dashboard:** [http://localhost:5000/admin.html](http://localhost:5000/admin.html)

4. Run the automated tests:
   ```powershell
   python test_app.py
   ```
