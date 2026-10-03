# 🌶️ Lucky Traders - Python & SQL Web Application

> **Savitribai Phule Pune University, Pune (SPPU)**  
> **T. Y. B. Sc. (Computer Science) — Sem - V | Course Code: CS-331-FP (Project)**  
> **Pattern: NEP CBCS 2026-27 | Major: Computer Science**  
> *Examination Scheme: CE: 15 Marks (7+8) + EE: 35 Marks (15+10+10) = 50 Marks Total*

---

## 📋 1. Project Abstract & Syllabus Compliance

**Lucky Traders** is a full-stack e-commerce web application engineered to modernize a traditional Maharashtrian spice and condiment merchant based in Hadapsar, Pune. Built in accordance with SPPU Syllabus CS-331-FP guidelines, the system includes:
- **Full Academic Project Report**: [`PROJECT_REPORT_SPPU_CS331FP.md`](file:///c:/Users/lalit/OneDrive/Desktop/New%20folder%20(2)/Bhukkad/PROJECT_REPORT_SPPU_CS331FP.md) strictly following Chapters 1–6 (Preliminary Investigation, Requirements, Database Design, System UML Diagrams, Screen Layouts, References).
- **Official UPI QR Payment**: Real Google Pay QR scanning for **Ashwini Bramhankar** (UPI ID: `ashutb1210@okhdfcbank`), saved in [`upi_qr.jpg`](file:///c:/Users/lalit/OneDrive/Desktop/New%20folder%20(2)/Bhukkad/upi_qr.jpg).
- **Student Code Walkthrough Guide**: [`CODE_EXPLANATION_GUIDE.md`](file:///c:/Users/lalit/OneDrive/Desktop/New%20folder%20(2)/Bhukkad/CODE_EXPLANATION_GUIDE.md) and Presentation Script in [`COLLEGE_PRESENTATION_SCRIPT.md`](file:///c:/Users/lalit/OneDrive/Desktop/New%20folder%20(2)/Bhukkad/COLLEGE_PRESENTATION_SCRIPT.md). 

### Core Features:
- **Dual-Pricing & Packaging**: Every product supports both wholesale (`1 Kg`) and retail (`250 Gm`) weights with dynamic price calculation.
- **Bilingual Marathi & English Catalog**: Exactly 20 authentic Maharashtrian recipes (e.g., *मिरची पावडर, कांदा लसुण मसाला, शेंगदाणा चटणी, आंबा लोणचे*).
- **Dual Role Architecture**: Distinct, secure flows for **Customers** and **Store Administrators**.
- **Interactive Shopping Basket**: Visual cart drawer with high-resolution product thumbnails, quantity steppers, and real-time GST tax calculation.
- **Relational SQL Database**: Powered by Python's `sqlite3` relational database engine with ACID transactions, foreign keys, and automatic inventory stock decrementing.
- **Computer-Generated GST Tax Invoices**: Dynamic receipt bills with breakdown of CGST (2.5%) and SGST (2.5%).
- **100% Responsive Design**: Smoothly adapts to smartphones, tablets, laptops, and desktops.

---

## 💻 2. Technology Stack & Architecture

The application follows the **Client-Server RESTful Architecture** and the **Model-View-Controller (MVC)** design pattern:

```
┌────────────────────────────────────────────────────────┐
│                   CLIENT BROWSER                       │
│  HTML5 • Responsive CSS3 • Vanilla JavaScript (ES6+)   │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP JSON REST Requests
                            ▼
┌────────────────────────────────────────────────────────┐
│               PYTHON BACKEND SERVER                    │
│      Flask Controller (`app.py`) • REST APIs           │
└───────────────────────────┬────────────────────────────┘
                            │ Python DB-API (`db.py`)
                            ▼
┌────────────────────────────────────────────────────────┐
│             RELATIONAL DATABASE (SQL)                  │
│       SQLite (`lucky_traders.db`) • 5 Tables           │
└────────────────────────────────────────────────────────┘
```

| Layer | Technology | Description |
|---|---|---|
| **Frontend View** | HTML5, CSS3, JavaScript ES6 | Semantic layout, CSS Grid & Flexbox, responsive breakpoints, localStorage caching |
| **Backend Controller** | Python 3.x, Flask | RESTful API server, routing, static asset serving, CORS middleware |
| **Database Model** | SQLite3 (`lucky_traders.db`) | Relational database, relational schema (`schema.sql`), seed catalog (`seed.sql`), SQL transactions |
| **Testing** | Python `unittest` | Automated unit testing suite (`test_app.py`) |

---

## 🗄️ 3. Relational Database Schema (ER Design)

The database schema consists of **5 relational tables** defined in [`database/schema.sql`](file:///c:/Users/lalit/OneDrive/Desktop/New%20folder%20%282%29/Bhukkad/database/schema.sql):

```
┌────────────────┐          ┌────────────────┐
│   categories   │ 1      * │    products    │
├────────────────┼──────────┤────────────────┤
│ id (PK)        │          │ id (PK)        │
│ name           │          │ category_id(FK)│
│ slug           │          │ name           │
│ icon           │          │ marathi_name   │
│ description    │          │ price_1kg      │
└────────────────┘          │ price_250g     │
                            │ stock_qty      │
                            │ in_stock       │
                            └───────┬────────┘
                                    │ 1
┌────────────────┐                  │
│     users      │ 1                │
├────────────────┤                  │
│ id (PK)        │                  │
│ username       │                  │
│ password_hash  │                  │
│ full_name      │                  │
│ role (admin/   │                  │
│       customer)│                  │
└───────┬────────┘                  │
        │ 1                         │
        │ *                         │ *
┌───────┴────────┐          ┌───────┴────────┐
│     orders     │ 1      * │  order_items   │
├────────────────┼──────────┤────────────────┤
│ id (PK)        │          │ id (PK)        │
│ order_number   │          │ order_id (FK)  │
│ user_id (FK)   │          │ product_id (FK)│
│ customer_name  │          │ weight         │
│ total_amount   │          │ unit_price     │
│ status         │          │ quantity       │
│ created_at     │          │ item_subtotal  │
└────────────────┘          └────────────────┘
```

### Table Definitions:
1. **`users`**: Stores user authentication credentials, contact phone, delivery address, and permission role (`admin` or `customer`).
2. **`categories`**: Stores product categories (`masalas`, `chutneys`, `pickles`) with icons and descriptions.
3. **`products`**: Stores catalog items, bilingual names, dual pricing (`price_1kg`, `price_250g`), image URLs, and live inventory count (`stock_qty`).
4. **`orders`**: Stores transaction headers, unique order tokens (`ORD-XXXX`), customer info, payment methods (COD / UPI), subtotal, CGST, SGST, and fulfillment status (`Confirmed`, `Processing`, `Delivered`, etc.).
5. **`order_items`**: Line items of each order capturing product snapshot, selected weight option, unit price, quantity, and line total.

---

## 🔄 4. System Workflows

### A. Customer Flow
```
Login / Register ──> Homepage ──> Select Category ──> Choose Weight (1Kg/250g)
                                                            │
Bill Invoice Receipt <── Payment (COD/UPI) <── Checkout Info <── Add to Basket
```

### B. Admin Flow
```
Admin Login ──> Dashboard Overview (KPI Metrics)
                      │
   ┌──────────────────┼──────────────────┬──────────────────┐
   ▼                  ▼                  ▼                  ▼
📁 Categories       👥 Customer Data   📦 Order Data      📊 Avail. Stock
 (Add / Remove)      (Spends & Orders)  (Status Update)    (Inventory Edit)
```

---

## 🔌 5. RESTful API Specification

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Server health check and runtime status |
| `/api/categories` | GET | List all active product categories |
| `/api/products` | GET | Retrieve product catalog (supports `?category=`, `?search=`) |
| `/api/products/<id>` | GET | Get single product detail |
| `/api/auth/login` | POST | Authenticate Customer or Store Admin |
| `/api/auth/register` | POST | Register a new customer record in SQL |
| `/api/orders` | POST | Place order, validate items, decrement stock atomically |
| `/api/orders/<order_number>` | GET | Retrieve dynamic tax invoice data for bill display |
| `/api/admin/stats` | GET | Fetch dashboard KPI counters (Revenue, Orders, Customers, Products) |
| `/api/admin/customers` | GET | List registered customers with lifetime order count and total spend |
| `/api/admin/orders` | GET | List all orders with line-item breakdowns |
| `/api/admin/orders/<id>/status`| PATCH | Update order fulfillment status |
| `/api/admin/categories` | POST | Add a new category to SQL database |
| `/api/admin/categories/<id>` | DELETE | Delete category and associated products |
| `/api/admin/products` | POST | Add a new product to catalog |
| `/api/admin/products/<id>/stock` | PATCH | Update available stock quantity (`stock_qty`) |
| `/api/admin/products/<id>` | DELETE | Remove product from inventory |

---

## 🚀 6. How to Run & Test

### Prerequisites
- Python 3.8 or higher installed on your computer.

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
*(Only `Flask==3.0.0` is required. SQLite is built directly into Python's standard library).*

### Step 2: Start the Web Application
```bash
python app.py
```

Open your browser and navigate to:
👉 **`http://localhost:5000`**

### Step 3: Run Automated Test Suite
```bash
python test_app.py
```
*Executes all 8 backend automated unit test cases, validating health, categories, products, authentication, orders, stock adjustments, and administrative stats.*

---

## 🔑 7. Demo Login Credentials

| Role | Username | Password | Notes |
|---|---|---|---|
| **Customer** | `lalit` | `lalit123` | Pre-seeded with past orders and delivery address |
| **Admin** | `admin` | `admin123` | Full access to manage catalog, orders, and stock |
| **New User** | *(Register)* | *(Any)* | Can be registered on the **📝 Register** tab |

---

## 🎓 8. College Project Viva & Defense Guide

### Frequently Asked Questions for Examiners:

#### Q1: Why did you choose Python and SQLite instead of MySQL or MongoDB?
> **Answer**: Python provides clean, readable code and strong standard library support. SQLite is a lightweight, serverless relational database engine stored in a single file (`lucky_traders.db`). It implements full SQL standards (ACID compliance, foreign keys, constraints) with zero installation overhead, making it ideal for self-contained desktop and web application demonstrations.

#### Q2: How do you handle concurrency and stock integrity when an order is placed?
> **Answer**: We use atomic SQL transactions inside `db.create_order()`. When an order is confirmed, an `UPDATE products SET stock_qty = MAX(0, stock_qty - ?)` statement executes inside the same transaction block. If any error occurs, `conn.rollback()` executes so no partial orders or corrupted stock counts remain.

#### Q3: How does the application handle dual pricing for 1 Kg and 250 Gm?
> **Answer**: In `products` table, we store `price_1kg` and `price_250g` as separate columns. When a user selects a packaging size on the frontend, the weight string is passed to `Cart.addItem()`. When the order is posted to `/api/orders`, the backend validates the price against the database to prevent client-side tampering.

#### Q4: How is responsive design achieved without heavy UI frameworks?
> **Answer**: We implemented pure CSS3 media queries (`max-width: 992px`, `768px`, `480px`), CSS Grid with `repeat(auto-fit, minmax(...))`, and touch-friendly tables using `overflow-x: auto; -webkit-overflow-scrolling: touch;`. This ensures optimal performance without the overhead of external CSS libraries.

---

### Project Developed by
*Department of Computer Science & Engineering / Information Technology*  
**Lucky Traders Web Application Project**
