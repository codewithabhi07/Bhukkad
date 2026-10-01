-- ==========================================================
-- Lucky Traders Database Seed Data
-- ==========================================================

-- Clean existing data
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM products;
DELETE FROM categories;
DELETE FROM users;

-- 1. Insert Categories
INSERT INTO categories (id, slug, name, icon, description, banner_image) VALUES
(1, 'masalas', 'Masalas (मसाले)', '🌶️', 'Pure stone-ground Maharashtrian spices, blends, and aromatic powders.', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=600&q=80'),
(2, 'chutneys', 'Chutneys (चटण्या)', '🥜', 'Handmade dry chutneys made with fresh roasted peanuts, garlic, and seeds.', 'https://5.imimg.com/data5/VC/BS/MY-32260496/dry-chutney-1000x1000.jpg'),
(3, 'pickles', 'Pickles (लोणचे)', '🥭', 'Traditional sun-cured homemade pickles bursting with authentic tangy flavor.', 'https://florafoods.in/wp-content/uploads/2023/04/Mango-Pickle-5.jpg');

-- 2. Insert Products (Exact Marathi Names & Dual Pricing)
-- Masalas (10 items)
INSERT INTO products (id, category_id, name, marathi_name, description, price_1kg, price_250g, image_url, stock_qty, in_stock, is_featured) VALUES
(1, 1, 'Mirchi Powder', 'मिरची पावडर', 'Finely ground bright red hot chili powder made from sun-dried chillies.', 510.00, 130.00, 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=600&q=80', 50, 1, 1),
(2, 1, 'Bedgi Mirchi Powder', 'बेडगी मिरची पावडर', 'Premium Byadgi chili powder known for rich crimson red color with mild aromatic pungency.', 1000.00, 260.00, 'https://images.unsplash.com/photo-1621996346565-e3d5d6281744?auto=format&fit=crop&w=600&q=80', 50, 1, 1),
(3, 1, 'Halad Powder', 'हळद पावडर', 'Golden aromatic turmeric powder with rich natural curcumin content.', 350.00, 90.00, 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=600&q=80', 50, 1, 0),
(4, 1, 'Dhana Powder', 'धना पावडर', 'Freshly ground coriander seeds powder for aromatic depth in everyday curries.', 310.00, 80.00, 'https://images.unsplash.com/photo-1599940824399-b87987ceb72a?auto=format&fit=crop&w=600&q=80', 50, 1, 0),
(5, 1, 'Kanda Lasun Masala', 'कांदा लसुण मसाला', 'Iconic Maharashtrian blend of roasted onions, garlic, and special spices.', 320.00, 80.00, 'https://images.unsplash.com/photo-1505253758473-96b3015f27eb?auto=format&fit=crop&w=600&q=80', 50, 1, 1),
(6, 1, 'Special Masala', 'स्पेशल मसाला', 'Signature secret house recipe blend crafted with over 20 roasted ingredients.', 870.00, 220.00, 'https://images.unsplash.com/photo-1532336414038-cf19250c5757?auto=format&fit=crop&w=600&q=80', 50, 1, 1),
(7, 1, 'Kala Masala', 'काळा मसाला', 'Traditional slow-roasted dark aromatic masala, the soul of Khandeshi cuisine.', 790.00, 200.00, 'https://images.unsplash.com/photo-1596040033282-35a09282362b?auto=format&fit=crop&w=600&q=80', 50, 1, 0),
(8, 1, 'Goda Masala', 'गोडा मसाला', 'Sweetly spiced mild Brahmin-style Maharashtrian masala made with stone flower (dagad phool).', 510.00, 130.00, 'https://images.unsplash.com/photo-1599940824399-b87987ceb72a?auto=format&fit=crop&w=600&q=80', 50, 1, 0),
(9, 1, 'Kitchen King Masala', 'किचन किंग मसाला', 'All-in-one versatile spice blend for rich paneer and mixed vegetable curries.', 670.00, 170.00, 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=600&q=80', 50, 1, 0),
(10, 1, 'Khada Masala', 'खडा मसाला', 'Whole aromatic spices mix (cinnamon, cloves, star anise, black cardamom, bay leaf).', 1000.00, 250.00, 'https://images.unsplash.com/photo-1509358271058-acd22cc93898?auto=format&fit=crop&w=600&q=80', 50, 1, 0);

-- Chutneys (6 items)
INSERT INTO products (id, category_id, name, marathi_name, description, price_1kg, price_250g, image_url, stock_qty, in_stock, is_featured) VALUES
(11, 2, 'Peanut Chutney', 'शेंगदाणा चटणी', 'Solapur style roasted crispy peanut chutney with garlic, cumin, and red chili.', 510.00, 130.00, 'https://5.imimg.com/data5/VC/BS/MY-32260496/dry-chutney-1000x1000.jpg', 50, 1, 1),
(12, 2, 'Coconut Chutney', 'खोबरे चटणी', 'Dry roasted desiccated coconut blended with pungent garlic, red chili, and rock salt.', 480.00, 130.00, 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=600&q=80', 50, 1, 1),
(13, 2, 'Sesame Chutney', 'तिळ चटणी', 'Nutty roasted white sesame seeds blended with spicy red chillies and salt.', 480.00, 130.00, 'https://images.unsplash.com/photo-1599940824399-b87987ceb72a?auto=format&fit=crop&w=600&q=80', 50, 1, 0),
(14, 2, 'Flaxseed Chutney', 'जवस चटणी', 'Omega-3 rich nutritious roasted flaxseed chutney with mild garlic aroma.', 360.00, 100.00, 'https://images.unsplash.com/photo-1509358271058-acd22cc93898?auto=format&fit=crop&w=600&q=80', 50, 1, 0),
(15, 2, 'Karale Chutney', 'कराळे चटणी', 'Traditional Niger seed dry chutney with robust earthy flavor, perfect with jowar bhakri.', 400.00, 110.00, 'https://5.imimg.com/data5/VC/BS/MY-32260496/dry-chutney-1000x1000.jpg', 50, 1, 0),
(16, 2, 'Special Garlic Chutney', 'स्पेशल लसुण चटणी', 'Intense fiery red chili and golden fried garlic chutney for vada pav and snacks.', 600.00, 160.00, 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=600&q=80', 50, 1, 1);

-- Pickles (4 items)
INSERT INTO products (id, category_id, name, marathi_name, description, price_1kg, price_250g, image_url, stock_qty, in_stock, is_featured) VALUES
(17, 3, 'Mango Pickle', 'आंबा लोणचे', 'Traditional raw Rajapuri mango pickle with mustard seeds and cold-pressed oil.', 430.00, 110.00, 'https://florafoods.in/wp-content/uploads/2023/04/Mango-Pickle-5.jpg', 50, 1, 1),
(18, 3, 'Amla Pickle', 'आवळा लोणचे', 'Tangy and vitamin C rich Indian gooseberry pickle cured in aromatic mustard spices.', 480.00, 120.00, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=600&q=80', 50, 1, 0),
(19, 3, 'Chilli Pickle', 'मिरचीचे लोणचे', 'Spicy green chillies marinated in crushed mustard, fenugreek, and lemon juice.', 400.00, 100.00, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=600&q=80', 50, 1, 0),
(20, 3, 'Lemon Pickle', 'लिंबाचे लोणचे', 'Savory spiced aged lemon pickle, sweet-and-sour with traditional spices.', 480.00, 120.00, 'https://images.unsplash.com/photo-1534432182912-63863115e106?auto=format&fit=crop&w=600&q=80', 50, 1, 1);

-- 3. Insert Users (Admin & Customer accounts)
INSERT INTO users (id, username, password_hash, full_name, email, phone, address, role) VALUES
(1, 'admin', 'admin123', 'Store Manager (Lucky Traders)', 'admin@luckytraders.com', '9890012345', 'Hadapsar, Pune 411002', 'admin'),
(2, 'lalit', 'lalit123', 'Lalit Kumar', 'lalit@example.com', '9876543210', 'Flat 402, Green Avenue, Hadapsar, Pune', 'customer'),
(3, 'demo', 'demo123', 'Sample Customer', 'demo@luckytraders.com', '9822001122', 'FC Road, Shivajinagar, Pune', 'customer');

-- 4. Insert Demo Orders & Line Items
INSERT INTO orders (id, order_number, user_id, customer_name, customer_phone, customer_address, payment_method, subtotal, cgst, sgst, total_amount, status, created_at) VALUES
(1, 'ORD-3112', 2, 'Lalit Kumar', '9876543210', 'Hadapsar, Pune 411002', 'Cash on Delivery', 320.00, 8.00, 8.00, 336.00, 'Delivered', '2026-04-14 11:30:00'),
(2, 'ORD-3105', 3, 'Sample Customer', '9822001122', 'FC Road, Pune', 'UPI', 510.00, 12.75, 12.75, 535.50, 'Dispatched', '2026-04-12 15:45:00');

INSERT INTO order_items (order_id, product_id, product_name, weight, unit_price, quantity, item_subtotal) VALUES
(1, 5, 'कांदा लसुण मसाला (Kanda Lasun Masala)', '1 Kg', 320.00, 1, 320.00),
(2, 11, 'शेंगदाणा चटणी (Peanut Chutney)', '1 Kg', 510.00, 1, 510.00);
