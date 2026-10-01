"""
Lucky Traders - Python SQL Relational Database Layer
Uses Python standard library sqlite3 to manage relational database.
"""

import os
import sqlite3
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'lucky_traders.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')
SEED_PATH = os.path.join(BASE_DIR, 'database', 'seed.sql')


def get_connection():
    """Returns a SQLite connection with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initializes schema and seeds initial catalog if empty."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Execute schema.sql
    if os.path.exists(SCHEMA_PATH):
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

    # 2. Check stock_qty column migration
    cursor.execute("PRAGMA table_info(products)")
    columns = [col['name'] for col in cursor.fetchall()]
    if 'stock_qty' not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN stock_qty INTEGER DEFAULT 50;")

    # 3. Seed data if products table is empty
    cursor.execute("SELECT COUNT(*) as count FROM products")
    count = cursor.fetchone()['count']
    if count == 0 and os.path.exists(SEED_PATH):
        print("Seeding initial Lucky Traders catalog and sample orders via Python SQL...")
        with open(SEED_PATH, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        cursor.execute("UPDATE products SET stock_qty = 50 WHERE stock_qty IS NULL OR stock_qty = 0;")
        print("Database seeded successfully.")

    conn.commit()
    conn.close()


# Initialize database upon import
init_db()


# ==========================================================
# CATEGORIES API
# ==========================================================
def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, COUNT(p.id) as product_count
        FROM categories c
        LEFT JOIN products p ON c.id = p.category_id
        GROUP BY c.id
        ORDER BY c.id ASC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def add_category(name, slug=None, icon='🍲', description='', banner_image=''):
    if not name:
        raise ValueError("Category name is required.")
    
    if not slug:
        slug = name.lower().strip().replace(' ', '-')
    slug = ''.join(c for c in slug.lower() if c.isalnum() or c in '-_')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO categories (slug, name, icon, description, banner_image)
        VALUES (?, ?, ?, ?, ?)
    """, (slug, name, icon, description, banner_image))
    cat_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        'id': cat_id,
        'slug': slug,
        'name': name,
        'icon': icon,
        'description': description,
        'banner_image': banner_image
    }


def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE category_id = ?", (category_id,))
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        changes = cursor.rowcount
        conn.commit()
        return changes > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ==========================================================
# PRODUCTS & AVAILABLE STOCK
# ==========================================================
def get_products(category_slug=None, search=None, featured=False):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT p.*, c.name as category_name, c.slug as category_slug
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE 1=1
    """
    params = []

    if category_slug and category_slug != 'all':
        sql += " AND c.slug = ?"
        params.append(category_slug)

    if featured:
        sql += " AND p.is_featured = 1"

    if search:
        sql += " AND (p.name LIKE ? OR p.marathi_name LIKE ? OR p.description LIKE ?)"
        s = f"%{search}%"
        params.extend([s, s, s])

    sql += " ORDER BY p.category_id ASC, p.id ASC"
    cursor.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, c.name as category_name, c.slug as category_slug
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = ?
    """, (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_product(category_id, name, marathi_name='', description='', price_1kg=0, price_250g=0, image_url='', stock_qty=50):
    if not category_id or not name:
        raise ValueError("Category ID and product name are required.")

    default_img = 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=600&q=80'
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (
            category_id, name, marathi_name, description,
            price_1kg, price_250g, image_url, stock_qty, in_stock, is_featured
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0)
    """, (
        category_id, name, marathi_name, description,
        float(price_1kg), float(price_250g),
        image_url or default_img, int(stock_qty)
    ))
    prod_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return get_product_by_id(prod_id)


def update_product_stock(product_id, stock_qty, in_stock=None):
    qty = max(0, int(stock_qty))
    status = in_stock if in_stock is not None else (1 if qty > 0 else 0)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET stock_qty = ?, in_stock = ?
        WHERE id = ?
    """, (qty, 1 if status else 0, product_id))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes > 0


def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes > 0


# ==========================================================
# CUSTOMER DATA
# ==========================================================
def get_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            u.id, u.username, u.full_name, u.email, u.phone, u.address, u.created_at,
            COUNT(o.id) as total_orders,
            COALESCE(SUM(o.total_amount), 0) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.role = 'customer'
        GROUP BY u.id
        ORDER BY u.created_at DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# ==========================================================
# ORDERS & BILL TRANSACTIONS
# ==========================================================
def create_order(user_id=None, customer_name='', customer_phone='', customer_address='',
                 payment_method='Cash on Delivery', items=None, notes=''):
    if not customer_name or not customer_phone or not customer_address:
        raise ValueError("Customer Name, Phone, and Address are required.")
    if not items or len(items) == 0:
        raise ValueError("Order must contain at least one item.")

    conn = get_connection()
    cursor = conn.cursor()

    subtotal = 0.0
    validated_items = []

    for item in items:
        cursor.execute("SELECT * FROM products WHERE id = ?", (item['productId'],))
        prod = cursor.fetchone()
        if not prod:
            conn.close()
            raise ValueError(f"Product not found: ID {item['productId']}")

        weight = '250 Gm' if item.get('weight') == '250 Gm' else '1 Kg'
        unit_price = float(prod['price_250g']) if weight == '250 Gm' else float(prod['price_1kg'])
        qty = max(1, int(item.get('quantity', 1)))
        item_subtotal = round(unit_price * qty, 2)
        subtotal += item_subtotal

        display_name = f"{prod['marathi_name']} ({prod['name']})" if prod['marathi_name'] else prod['name']
        validated_items.append({
            'product_id': prod['id'],
            'product_name': display_name,
            'weight': weight,
            'unit_price': unit_price,
            'quantity': qty,
            'item_subtotal': item_subtotal
        })

    # GST calculation: 2.5% CGST + 2.5% SGST
    cgst = round(subtotal * 0.025, 2)
    sgst = round(subtotal * 0.025, 2)
    total_amount = round(subtotal + cgst + sgst, 2)

    random_suffix = random.randint(1000, 9999)
    order_number = f"ORD-{random_suffix}"

    try:
        cursor.execute("""
            INSERT INTO orders (
                order_number, user_id, customer_name, customer_phone,
                customer_address, payment_method, subtotal, cgst, sgst,
                total_amount, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmed', ?)
        """, (
            order_number, user_id, customer_name, customer_phone,
            customer_address, payment_method, subtotal, cgst, sgst,
            total_amount, notes
        ))
        order_id = cursor.lastrowid

        for v_item in validated_items:
            cursor.execute("""
                INSERT INTO order_items (
                    order_id, product_id, product_name, weight, unit_price, quantity, item_subtotal
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                order_id, v_item['product_id'], v_item['product_name'],
                v_item['weight'], v_item['unit_price'], v_item['quantity'],
                v_item['item_subtotal']
            ))

            # Auto-decrement stock in SQL
            cursor.execute("""
                UPDATE products
                SET stock_qty = MAX(0, stock_qty - ?),
                    in_stock = CASE WHEN stock_qty - ? <= 0 THEN 0 ELSE 1 END
                WHERE id = ?
            """, (v_item['quantity'], v_item['quantity'], v_item['product_id']))

        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

    conn.close()
    return get_order_by_number(order_number)


def get_order_by_number(order_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
    order_row = cursor.fetchone()
    if not order_row:
        conn.close()
        return None

    order = dict(order_row)
    cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order['id'],))
    order['items'] = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return order


def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = [dict(r) for r in cursor.fetchall()]

    for ord_dict in orders:
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (ord_dict['id'],))
        ord_dict['items'] = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return orders


def update_order_status(order_id, status):
    valid_statuses = ['Pending', 'Confirmed', 'Processing', 'Dispatched', 'Delivered', 'Cancelled']
    if status not in valid_statuses:
        raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes > 0


# ==========================================================
# ADMIN DASHBOARD STATS
# ==========================================================
def get_admin_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total_orders, COALESCE(SUM(total_amount), 0) as total_sales FROM orders")
    row_orders = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as pending FROM orders WHERE status IN ('Pending', 'Confirmed', 'Processing')")
    row_pending = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as total_products FROM products")
    row_prods = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as total_customers FROM users WHERE role = 'customer'")
    row_cust = cursor.fetchone()

    cursor.execute("""
        SELECT product_name, SUM(quantity) as units_sold, SUM(item_subtotal) as revenue
        FROM order_items
        GROUP BY product_name
        ORDER BY units_sold DESC
        LIMIT 5
    """)
    top_selling = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        'totalOrders': row_orders['total_orders'],
        'totalSales': row_orders['total_sales'],
        'pendingOrders': row_pending['pending'],
        'totalProducts': row_prods['total_products'],
        'totalCustomers': row_cust['total_customers'],
        'topSelling': top_selling
    }


# ==========================================================
# AUTHENTICATION
# ==========================================================
def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    user = dict(row)
    if user['password_hash'] == password:
        user.pop('password_hash', None)
        return user
    return None


def register_user(username, password, full_name, email='', phone='', address=''):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("Username already exists. Please choose another.")

    cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, email, phone, address, role)
        VALUES (?, ?, ?, ?, ?, ?, 'customer')
    """, (username, password, full_name, email, phone, address))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        'id': user_id,
        'username': username,
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'address': address,
        'role': 'customer'
    }
