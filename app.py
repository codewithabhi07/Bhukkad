"""
Lucky Traders - Python Flask Web Application & REST APIs
Serves static frontend and handles all database queries via Python sqlite3.
"""

import os
from flask import Flask, request, jsonify, send_from_directory
import db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')


# ==========================================================
# CORS MIDDLEWARE (Allows cross-origin and local requests)
# ==========================================================
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    res = app.make_default_options_response()
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return res



# ==========================================================
# STATIC FRONTEND ROUTES
# ==========================================================
@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    if os.path.exists(os.path.join(BASE_DIR, filename)):
        return send_from_directory(BASE_DIR, filename)
    return send_from_directory(BASE_DIR, 'index.html')



# ==========================================================
# REST API ENDPOINTS
# ==========================================================

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'online',
        'runtime': 'Python 3.13 with SQLite3 and Flask',
        'app': 'Lucky Traders - Authentic Spices & Pickles',
        'database': 'Connected to lucky_traders.db (SQL)'
    })


# 1. Categories
@app.route('/api/categories', methods=['GET'])
def list_categories():
    try:
        categories = db.get_categories()
        return jsonify({'success': True, 'categories': categories})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/categories', methods=['POST'])
def create_category():
    data = request.get_json() or {}
    try:
        cat = db.add_category(
            name=data.get('name'),
            slug=data.get('slug'),
            icon=data.get('icon', '🍲'),
            description=data.get('description', ''),
            banner_image=data.get('bannerImage', '')
        )
        return jsonify({'success': True, 'category': cat}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/admin/categories/<int:cat_id>', methods=['DELETE'])
def remove_category(cat_id):
    try:
        deleted = db.delete_category(cat_id)
        if not deleted:
            return jsonify({'success': False, 'error': 'Category not found'}), 404
        return jsonify({'success': True, 'message': 'Category removed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# 2. Products
@app.route('/api/products', methods=['GET'])
def list_products():
    category = request.args.get('category')
    search = request.args.get('search')
    featured = request.args.get('featured') in ['1', 'true', 'True']

    try:
        products = db.get_products(category_slug=category, search=search, featured=featured)
        return jsonify({'success': True, 'count': len(products), 'products': products})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<int:prod_id>', methods=['GET'])
def get_product(prod_id):
    try:
        product = db.get_product_by_id(prod_id)
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        return jsonify({'success': True, 'product': product})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}
    try:
        prod = db.add_product(
            category_id=data.get('categoryId'),
            name=data.get('name'),
            marathi_name=data.get('marathiName', ''),
            description=data.get('description', ''),
            price_1kg=data.get('price1kg', 0),
            price_250g=data.get('price250g', 0),
            image_url=data.get('imageUrl', ''),
            stock_qty=data.get('stockQty', 50)
        )
        return jsonify({'success': True, 'product': prod}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/admin/products/<int:prod_id>/stock', methods=['PATCH'])
def update_stock(prod_id):
    data = request.get_json() or {}
    try:
        updated = db.update_product_stock(
            product_id=prod_id,
            stock_qty=data.get('stockQty', 0),
            in_stock=data.get('inStock')
        )
        if not updated:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        return jsonify({'success': True, 'message': 'Stock quantity updated in SQL'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/admin/products/<int:prod_id>', methods=['DELETE'])
def remove_product(prod_id):
    try:
        deleted = db.delete_product(prod_id)
        if not deleted:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        return jsonify({'success': True, 'message': 'Product removed from store'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# 3. Orders & Dynamic Bill
@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.get_json() or {}
    try:
        order = db.create_order(
            user_id=data.get('userId'),
            customer_name=data.get('customerName'),
            customer_phone=data.get('customerPhone'),
            customer_address=data.get('customerAddress'),
            payment_method=data.get('paymentMethod', 'Cash on Delivery'),
            items=data.get('items', []),
            notes=data.get('notes', '')
        )
        return jsonify({
            'success': True,
            'message': 'Order placed successfully and recorded in SQL.',
            'order': order
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/orders/<order_number>', methods=['GET'])
def get_order_bill(order_number):
    try:
        order = db.get_order_by_number(order_number)
        if not order:
            return jsonify({'success': False, 'error': 'Order not found in SQL'}), 404
        return jsonify({'success': True, 'order': order})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# 4. User & Admin Authentication
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400

    user = db.authenticate_user(username.strip(), password.strip())
    if not user:
        return jsonify({'success': False, 'error': 'Invalid username or password'}), 401

    return jsonify({
        'success': True,
        'message': 'Logged in successfully',
        'user': user
    })


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    try:
        user = db.register_user(
            username=data.get('username', '').strip(),
            password=data.get('password', '').strip(),
            full_name=data.get('fullName', '').strip(),
            email=data.get('email', '').strip(),
            phone=data.get('phone', '').strip(),
            address=data.get('address', '').strip()
        )
        return jsonify({
            'success': True,
            'message': 'Customer registered successfully in SQL',
            'user': user
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# 5. Admin Dashboard APIs
@app.route('/api/admin/orders', methods=['GET'])
def admin_orders():
    try:
        orders = db.get_all_orders()
        return jsonify({'success': True, 'count': len(orders), 'orders': orders})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/orders/<int:order_id>/status', methods=['PATCH'])
def admin_update_order_status(order_id):
    data = request.get_json() or {}
    try:
        updated = db.update_order_status(order_id, data.get('status'))
        if not updated:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        return jsonify({'success': True, 'message': f"Order status updated to {data.get('status')}"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/admin/customers', methods=['GET'])
def admin_customers():
    try:
        customers = db.get_customers()
        return jsonify({'success': True, 'count': len(customers), 'customers': customers})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    try:
        stats = db.get_admin_stats()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 60)
    print("Lucky Traders - Python & SQL Server is starting!")
    print(f"Local URL: http://localhost:{port}")
    print("Database: Python sqlite3 connected to lucky_traders.db")
    print("Admin Login: admin / admin123")
    print("Customer Login: lalit / lalit123")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)

