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
(1, 'masalas', 'Masalas (मसाले)', '🌶️', 'Pure stone-ground Maharashtrian spices, blends, and aromatic powders.', 'images/1_mirchi_powder.jpg'),
(2, 'chutneys', 'Chutneys (चटण्या)', '🥜', 'Handmade dry chutneys made with fresh roasted peanuts, garlic, and seeds.', 'images/11_shengdana_chutney.jpg'),
(3, 'pickles', 'Pickles (लोणचे)', '🥭', 'Traditional sun-cured homemade pickles bursting with authentic tangy flavor.', 'images/17_amba_lonache.jpg');

-- 2. Insert Products (Exact Name-Related Dedicated Photos & Dual Pricing)
-- Masalas (10 items)
INSERT INTO products (id, category_id, name, marathi_name, description, price_1kg, price_250g, image_url, stock_qty, in_stock, is_featured) VALUES
(1, 1, 'Mirchi Powder', 'मिरची पावडर', 'Finely ground bright red hot chili powder made from sun-dried chillies.', 510.00, 130.00, 'images/1_mirchi_powder.jpg', 50, 1, 1),
(2, 1, 'Bedgi Mirchi Powder', 'बेडगी मिरची पावडर', 'Premium Byadgi chili powder known for rich crimson red color with mild aromatic pungency.', 1000.00, 260.00, 'images/2_bedgi_mirchi.jpg', 50, 1, 1),
(3, 1, 'Halad Powder', 'हळद पावडर', 'Golden aromatic turmeric powder with rich natural curcumin content.', 350.00, 90.00, 'images/3_halad_powder.jpg', 50, 1, 0),
(4, 1, 'Dhana Powder', 'धना पावडर', 'Freshly ground coriander seeds powder for aromatic depth in everyday curries.', 310.00, 80.00, 'images/4_dhana_powder.jpg', 50, 1, 0),
(5, 1, 'Kanda Lasun Masala', 'कांदा लसुण मसाला', 'Iconic Maharashtrian blend of roasted onions, garlic, and special spices.', 320.00, 80.00, 'images/5_kanda_lasun_masala.jpg', 50, 1, 1),
(6, 1, 'Special Masala', 'स्पेशल मसाला', 'Signature secret house recipe blend crafted with over 20 roasted ingredients.', 870.00, 220.00, 'images/6_special_masala.jpg', 50, 1, 1),
(7, 1, 'Kala Masala', 'काळा मसाला', 'Traditional slow-roasted dark aromatic masala, the soul of Khandeshi cuisine.', 790.00, 200.00, 'images/7_kala_masala.jpg', 50, 1, 0),
(8, 1, 'Goda Masala', 'गोडा मसाला', 'Sweetly spiced mild Brahmin-style Maharashtrian masala made with stone flower (dagad phool).', 510.00, 130.00, 'images/8_goda_masala.jpg', 50, 1, 0),
(9, 1, 'Kitchen King Masala', 'किचन किंग मसाला', 'All-in-one versatile spice blend for rich paneer and mixed vegetable curries.', 670.00, 170.00, 'images/9_kitchen_king_masala.jpg', 50, 1, 0),
(10, 1, 'Khada Masala', 'खडा मसाला', 'Whole aromatic spices mix (cinnamon, cloves, star anise, black cardamom, bay leaf).', 1000.00, 250.00, 'images/10_khada_masala.jpg', 50, 1, 0);

-- Chutneys (6 items)
INSERT INTO products (id, category_id, name, marathi_name, description, price_1kg, price_250g, image_url, stock_qty, in_stock, is_featured) VALUES
(11, 2, 'Peanut Chutney', 'शेंगदाणा चटणी', 'Solapur style roasted crispy peanut chutney with garlic, cumin, and red chili.', 510.00, 130.00, 'images/11_shengdana_chutney.jpg', 50, 1, 1),
(12, 2, 'Coconut Chutney', 'खोबरे चटणी', 'Dry roasted desiccated coconut blended with pungent garlic, red chili, and rock salt.', 480.00, 130.00, 'images/12_khobare_chutney.jpg', 50, 1, 1),
(13, 2, 'Til Chutney', 'तिळ चटणी', 'Nutty roasted white sesame seeds blended with spicy red chillies and salt.', 480.00, 130.00, 'images/13_til_chutney.jpg', 50, 1, 0),
(14, 2, 'Flaxseed Chutney', 'जवस चटणी', 'Omega-3 rich nutritious roasted flaxseed chutney with mild garlic aroma.', 360.00, 100.00, 'images/14_jawas_chutney.jpg', 50, 1, 0),
(15, 2, 'Karale Chutney', 'कराळे चटणी', 'Traditional Niger seed dry chutney with robust earthy flavor, perfect with jowar bhakri.', 400.00, 110.00, 'images/15_karale_chutney.jpg', 50, 1, 0),
(16, 2, 'Special Garlic Chutney', 'स्पेशल लसुण चटणी', 'Intense fiery red chili and golden fried garlic chutney for vada pav and snacks.', 600.00, 160.00, 'images/16_lasun_chutney.jpg', 50, 1, 1);

-- Pickles (4 items)
INSERT INTO products (id, category_id, name, marathi_name, description, price_1kg, price_250g, image_url, stock_qty, in_stock, is_featured) VALUES
(17, 3, 'Mango Pickle', 'आंबा लोणचे', 'Traditional raw Rajapuri mango pickle with mustard seeds and cold-pressed oil.', 430.00, 110.00, 'images/17_amba_lonache.jpg', 50, 1, 1),
(18, 3, 'Amla Pickle', 'आवळा लोणचे', 'Tangy and vitamin C rich Indian gooseberry pickle cured in aromatic mustard spices.', 480.00, 120.00, 'images/18_amla_lonache.jpg', 50, 1, 0),
(19, 3, 'Chilli Pickle', 'मिरचीचे लोणचे', 'Spicy green chillies marinated in crushed mustard, fenugreek, and lemon juice.', 400.00, 100.00, 'images/19_mirchi_lonache.jpg', 50, 1, 0),
(20, 3, 'Lemon Pickle', 'लिंबाचे लोणचे', 'Savory spiced aged lemon pickle, sweet-and-sour with traditional spices.', 480.00, 120.00, 'images/20_limbu_lonache.jpg', 50, 1, 1);

-- 3. Pre-seed Users (Customer and Admin)
INSERT INTO users (id, username, password_hash, full_name, email, phone, address, role) VALUES
(1, 'admin', 'admin123', 'Store Administrator', 'admin@luckytraders.local', '9822000000', 'Shop No. 12, Market Yard, Pune - 411037', 'admin'),
(2, 'User', 'User123', 'Customer User', 'user@example.com', '9876543210', 'Flat 402, Green Avenue, Hadapsar, Pune', 'customer'),
(3, 'lalit', 'lalit123', 'Lalit Kumar', 'lalit@example.com', '9822001122', 'FC Road, Shivajinagar, Pune', 'customer');
