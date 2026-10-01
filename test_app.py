"""
Lucky Traders - Python Automated Test Suite
Verifies all SQL operations, authentication, stock management, and REST APIs.
"""

import unittest
import json
import db
from app import app


class LuckyTradersPythonTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_01_health_check(self):
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'online')
        self.assertIn('Python', data['runtime'])

    def test_02_categories_list(self):
        res = self.client.get('/api/categories')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['categories']), 3)

    def test_03_products_catalog(self):
        res = self.client.get('/api/products')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['count'], 20)

    def test_04_user_authentication(self):
        # 1. Customer login
        res = self.client.post('/api/auth/login', json={'username': 'lalit', 'password': 'lalit123'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['role'], 'customer')

        # 2. Admin login
        res = self.client.post('/api/auth/login', json={'username': 'admin', 'password': 'admin123'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['role'], 'admin')

    def test_05_admin_category_crud(self):
        # Add Category
        res = self.client.post('/api/admin/categories', json={
            'name': 'Python Specials',
            'slug': 'python-specials',
            'icon': '🐍',
            'description': 'Special spices created by Python'
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        cat_id = data['category']['id']

        # Delete Category
        del_res = self.client.delete(f'/api/admin/categories/{cat_id}')
        self.assertEqual(del_res.status_code, 200)

    def test_06_admin_customer_data(self):
        res = self.client.get('/api/admin/customers')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['count'], 2)

    def test_07_order_flow_and_stock_auto_decrement(self):
        # 1. Get initial stock of product 2 (Bedgi Mirchi)
        initial_prod = db.get_product_by_id(2)
        initial_stock = initial_prod['stock_qty']

        # 2. Place Order for 3 units
        res = self.client.post('/api/orders', json={
            'customerName': 'Suresh Kulkarni',
            'customerPhone': '9890123456',
            'customerAddress': 'Deccan Gymkhana, Pune',
            'paymentMethod': 'UPI',
            'items': [
                {'productId': 2, 'weight': '1 Kg', 'quantity': 3}
            ]
        })
        self.assertEqual(res.status_code, 201)
        order_data = res.get_json()['order']
        order_number = order_data['order_number']

        # 3. Check stock decremented
        after_prod = db.get_product_by_id(2)
        self.assertEqual(after_prod['stock_qty'], initial_stock - 3)

        # 4. Fetch dynamic Bill
        bill_res = self.client.get(f'/api/orders/{order_number}')
        self.assertEqual(bill_res.status_code, 200)
        bill_data = bill_res.get_json()['order']
        self.assertEqual(bill_data['order_number'], order_number)
        self.assertIn('Bedgi Mirchi Powder', bill_data['items'][0]['product_name'])

    def test_08_admin_stock_update(self):
        res = self.client.patch('/api/admin/products/1/stock', json={'stockQty': 85})
        self.assertEqual(res.status_code, 200)
        updated_prod = db.get_product_by_id(1)
        self.assertEqual(updated_prod['stock_qty'], 85)


if __name__ == '__main__':
    unittest.main()
