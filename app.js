/**
 * Lucky Traders - Frontend Application Logic (app.js)
 * Clean, modular JavaScript designed for college presentation & viva.
 * 
 * Divided into 5 clear modules:
 * 1. Configuration & API Base
 * 2. Shopping Cart Management (LocalStorage & GST Calculation)
 * 3. User & Admin Session Management (Auth)
 * 4. Shared UI Components (Cart Drawer & Multi-Step Checkout Modal)
 * 5. Order Placement & Bill Redirection
 */

// ==========================================================
// 1. CONFIGURATION: Backend API Endpoint
// ==========================================================
// Automatically points to Flask backend (port 5000)
const API_BASE = (window.location.protocol === 'file:' || !window.location.origin.startsWith('http'))
  ? 'http://localhost:5000/api'
  : '/api';


// ==========================================================
// 2. SHOPPING CART MODULE (LocalStorage)
// ==========================================================
const Cart = {
  key: 'lucky_traders_cart',

  // Read cart items array from browser localStorage
  getItems() {
    try {
      const data = localStorage.getItem(this.key);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      return [];
    }
  },

  // Save updated items back to localStorage and refresh UI
  saveItems(items) {
    localStorage.setItem(this.key, JSON.stringify(items));
    this.updateCartBadge();
    this.renderCartDrawer();
  },

  // Add a product with selected weight (1 Kg or 250 Gm) to cart
  addItem(product, weight = '1 Kg', quantity = 1) {
    const items = this.getItems();
    const existingIndex = items.findIndex(
      item => item.productId === product.id && item.weight === weight
    );

    const unitPrice = weight === '250 Gm' ? Number(product.price_250g) : Number(product.price_1kg);
    const defaultImg = 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=600&q=80';
    const imageUrl = product.image_url || product.imageUrl || defaultImg;
    const marathiName = product.marathi_name || product.marathiName || '';

    if (existingIndex > -1) {
      items[existingIndex].quantity += quantity;
      items[existingIndex].subtotal = items[existingIndex].quantity * unitPrice;
    } else {
      items.push({
        productId: product.id,
        productName: product.name,
        marathiName: marathiName,
        weight: weight,
        unitPrice: unitPrice,
        quantity: quantity,
        subtotal: unitPrice * quantity,
        imageUrl: imageUrl
      });
    }

    this.saveItems(items);
    const displayName = marathiName ? `${marathiName} (${product.name})` : product.name;
    this.showToast(`Added ${quantity}x ${displayName} [${weight}] to cart!`);
  },

  // Change quantity (+ / -) in cart
  updateQuantity(index, newQty) {
    const items = this.getItems();
    if (index >= 0 && index < items.length) {
      if (newQty <= 0) {
        items.splice(index, 1);
      } else {
        items[index].quantity = newQty;
        items[index].subtotal = items[index].quantity * items[index].unitPrice;
      }
      this.saveItems(items);
    }
  },

  // Remove single item from cart
  removeItem(index) {
    const items = this.getItems();
    items.splice(index, 1);
    this.saveItems(items);
  },

  // Clear entire cart after order is confirmed
  clear() {
    localStorage.removeItem(this.key);
    this.updateCartBadge();
    this.renderCartDrawer();
  },

  // Calculate Subtotal, 2.5% CGST, 2.5% SGST, and Grand Total
  getTotal() {
    const items = this.getItems();
    const subtotal = items.reduce((sum, item) => sum + (item.subtotal || 0), 0);
    const cgst = Math.round((subtotal * 0.025) * 100) / 100;
    const sgst = Math.round((subtotal * 0.025) * 100) / 100;
    const total = Math.round((subtotal + cgst + sgst) * 100) / 100;
    const count = items.reduce((c, i) => c + i.quantity, 0);
    return { subtotal, cgst, sgst, total, count };
  },

  // Update navbar cart count badge
  updateCartBadge() {
    const badges = document.querySelectorAll('.cart-count-badge');
    const { count } = this.getTotal();
    badges.forEach(b => {
      b.textContent = count;
      b.style.display = count > 0 ? 'inline-flex' : 'none';
    });
  },

  // Render cart items with product images inside sliding drawer
  renderCartDrawer() {
    const container = document.getElementById('cart-items-container');
    const subtotalEl = document.getElementById('cart-subtotal');
    const cgstEl = document.getElementById('cart-cgst');
    const sgstEl = document.getElementById('cart-sgst');
    const totalEl = document.getElementById('cart-total');
    const checkoutBtn = document.getElementById('cart-checkout-btn');

    if (!container) return;

    const items = this.getItems();
    const totals = this.getTotal();

    if (items.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 40px 10px; color: #777;">
          <p style="font-size: 3rem; margin-bottom: 10px;">🛒</p>
          <p style="font-weight: 600; color: #333;">Your basket is empty.</p>
          <p style="font-size: 0.85rem; margin-top: 6px;">Add freshly ground masalas, dry chutneys or pickles!</p>
        </div>
      `;
      if (checkoutBtn) checkoutBtn.disabled = true;
    } else {
      const defaultImg = 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=200&q=80';
      container.innerHTML = items.map((item, idx) => `
        <div class="cart-item">
          <div class="cart-item-img-wrapper">
            <img src="${item.imageUrl || defaultImg}" alt="${item.productName}" class="cart-item-img" onerror="this.src='${defaultImg}'">
          </div>
          <div class="cart-item-details">
            <div class="cart-marathi-name">${item.marathiName || item.productName}</div>
            <div class="cart-english-name">${item.productName}</div>
            <div style="font-size:0.8rem; color:#666; margin: 3px 0;">
              <b>${item.weight}</b> @ ₹${item.unitPrice}
            </div>
            <div class="cart-item-qty-controls">
              <button class="btn-qty" onclick="Cart.updateQuantity(${idx}, ${item.quantity - 1})">-</button>
              <span style="font-size:0.9rem; font-weight:600; min-width:18px; text-align:center;">${item.quantity}</span>
              <button class="btn-qty" onclick="Cart.updateQuantity(${idx}, ${item.quantity + 1})">+</button>
              <button class="btn-remove" onclick="Cart.removeItem(${idx})" title="Remove item">🗑️</button>
            </div>
          </div>
          <div class="cart-item-subtotal">₹${item.subtotal}</div>
        </div>
      `).join('');
      if (checkoutBtn) checkoutBtn.disabled = false;
    }

    if (subtotalEl) subtotalEl.textContent = `₹${totals.subtotal}`;
    if (cgstEl) cgstEl.textContent = `₹${totals.cgst}`;
    if (sgstEl) sgstEl.textContent = `₹${totals.sgst}`;
    if (totalEl) totalEl.textContent = `₹${totals.total}`;
  },

  // Floating toast notification popup
  showToast(message) {
    let toast = document.getElementById('store-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'store-toast';
      toast.className = 'toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.remove('show'), 2800);
  }
};


// ==========================================================
// 3. USER AUTHENTICATION & SESSION MODULE
// ==========================================================
const Auth = {
  key: 'lucky_traders_user',

  // Retrieve current logged-in user object
  getUser() {
    try {
      const u = localStorage.getItem(this.key);
      return u ? JSON.parse(u) : null;
    } catch (e) {
      return null;
    }
  },

  // Save user session upon successful login
  setUser(user) {
    localStorage.setItem(this.key, JSON.stringify(user));
    this.updateUserNav();
  },

  // Logout and redirect to login page
  logout() {
    localStorage.removeItem(this.key);
    window.location.href = 'login.html';
  },

  // Update top navigation bar according to logged in state
  updateUserNav() {
    const userContainer = document.getElementById('user-nav-container');
    if (!userContainer) return;

    const user = this.getUser();
    if (user) {
      userContainer.innerHTML = `
        <span class="user-greeting">Namaste, <b>${user.full_name || user.username}</b></span>
        ${user.role === 'admin' ? '<a href="admin.html" class="nav-admin-link">🛡️ Admin Portal</a>' : ''}
        <a href="javascript:void(0)" onclick="Auth.logout()" class="nav-logout-btn">Logout</a>
      `;
    } else {
      userContainer.innerHTML = `
        <a href="login.html" class="nav-login-btn">Login / Register</a>
      `;
    }
  }
};


// ==========================================================
// 4. SHARED UI: CART DRAWER & MULTI-STEP CHECKOUT MODAL
// ==========================================================

// Ensure cart drawer & checkout modal exist in DOM (auto-injects if missing)
function ensureCartAndCheckoutMarkup() {
  if (!document.getElementById('cart-drawer')) {
    const cartHTML = `
      <div id="cart-overlay" class="cart-overlay" onclick="toggleCartDrawer()"></div>
      <div id="cart-drawer" class="cart-drawer">
        <div class="cart-drawer-header">
          <h3>🛒 Your Spice Basket</h3>
          <button class="close-drawer-btn" onclick="toggleCartDrawer()">&times;</button>
        </div>
        <div id="cart-items-container" class="cart-drawer-items"></div>
        <div class="cart-drawer-footer">
          <div class="cart-calc-row"><span>Subtotal:</span><span id="cart-subtotal">₹0.00</span></div>
          <div class="cart-calc-row"><span>CGST (2.5%):</span><span id="cart-cgst">₹0.00</span></div>
          <div class="cart-calc-row"><span>SGST (2.5%):</span><span id="cart-sgst">₹0.00</span></div>
          <div class="cart-calc-total"><span>Total Amount:</span><span id="cart-total">₹0.00</span></div>
          <button id="cart-checkout-btn" class="btn-checkout" onclick="openCheckoutModal()">
            Proceed to Checkout →
          </button>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', cartHTML);
  }

  if (!document.getElementById('checkout-modal')) {
    const modalHTML = `
      <div id="checkout-modal" class="modal">
        <div class="modal-content">
          <!-- STEP 1: INFO -->
          <div id="checkout-step-info">
            <div class="modal-header">
              <h2>📋 Step 1: Delivery Details</h2>
              <button class="close-modal-btn" onclick="closeCheckoutModal()">&times;</button>
            </div>
            <div class="form-group">
              <label for="checkout-name">Your Full Name *</label>
              <input type="text" id="checkout-name" class="form-control" placeholder="e.g. Lalit Kumar" required>
            </div>
            <div class="form-group">
              <label for="checkout-phone">Mobile Phone Number *</label>
              <input type="tel" id="checkout-phone" class="form-control" placeholder="10-digit mobile number" required>
            </div>
            <div class="form-group">
              <label for="checkout-address">Delivery Address *</label>
              <textarea id="checkout-address" class="form-control" rows="2" placeholder="House No, Street, Hadapsar, Pune" required></textarea>
            </div>
            <button type="button" class="btn-confirm-order" onclick="goToCheckoutStep('payment')">
              Proceed to Payment ➔
            </button>
          </div>

          <!-- STEP 2: PAYMENT -->
          <div id="checkout-step-payment" style="display: none;">
            <div class="modal-header">
              <h2>💳 Step 2: Payment Method</h2>
              <button class="close-modal-btn" onclick="closeCheckoutModal()">&times;</button>
            </div>
            <div id="payment-summary-display" class="checkout-summary-box"></div>
            <div class="form-group">
              <label><b>Choose Payment Option:</b></label>
              <div style="margin: 8px 0; display:flex; flex-direction:column; gap:8px;">
                <label style="display:flex; align-items:center; gap:8px; cursor:pointer; background:#f9f9f9; padding:8px 12px; border-radius:4px; border:1px solid #ddd;">
                  <input type="radio" name="paymentMethod" value="Cash on Delivery" checked onchange="togglePaymentMethodDetails('COD')">
                  <span>💵 <b>Cash on Delivery (COD)</b></span>
                </label>
                <label style="display:flex; align-items:center; gap:8px; cursor:pointer; background:#f9f9f9; padding:8px 12px; border-radius:4px; border:1px solid #ddd;">
                  <input type="radio" name="paymentMethod" value="UPI" onchange="togglePaymentMethodDetails('UPI')">
                  <span>⚡ <b>Instant UPI / QR Code</b></span>
                </label>
              </div>
            </div>
            <div id="upi-qr-box" style="display:none; text-align:center; background:#fdf5eb; border:1px dashed #d35400; padding:14px; border-radius:8px; margin-bottom:12px;">
              <p style="font-size:0.95rem; font-weight:bold; color:#112d42; margin-bottom:2px;">Ashwini Bramhankar</p>
              <p style="font-size:0.85rem; color:#b75304; font-weight:600; margin-bottom:8px;">Scan to Pay with Any UPI App</p>
              <div style="background:white; display:inline-block; padding:8px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.15);">
                <img src="upi_qr.jpg" alt="UPI QR Code - Ashwini Bramhankar" style="width:160px; height:auto; display:block; border-radius:4px;">
              </div>
              <p style="font-size:0.85rem; margin-top:8px; color:#333;">UPI ID: <b style="color:#0a3d62;">ashutb1210@okhdfcbank</b></p>
            </div>
            <div style="display:flex; gap:10px;">
              <button type="button" class="btn-home" style="flex:1;" onclick="goToCheckoutStep('info')">← Back</button>
              <button type="button" id="submit-order-btn" class="btn-confirm-order" style="flex:2;" onclick="submitOrder()">
                Confirm & View Bill 🧾
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
  }
}

// Slide cart drawer in / out
function toggleCartDrawer() {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-overlay');
  if (drawer && overlay) {
    const isOpen = drawer.classList.contains('open');
    if (isOpen) {
      drawer.classList.remove('open');
      overlay.classList.remove('open');
    } else {
      Cart.renderCartDrawer();
      drawer.classList.add('open');
      overlay.classList.add('open');
    }
  }
}

// Open checkout modal (pre-fills with user details if logged in)
function openCheckoutModal() {
  const items = Cart.getItems();
  if (items.length === 0) {
    alert('Your basket is empty. Please add items before checking out.');
    return;
  }

  const user = Auth.getUser();
  if (user) {
    const nameInput = document.getElementById('checkout-name');
    const phoneInput = document.getElementById('checkout-phone');
    const addressInput = document.getElementById('checkout-address');
    if (nameInput && !nameInput.value) nameInput.value = user.full_name || '';
    if (phoneInput && !phoneInput.value) phoneInput.value = user.phone || '';
    if (addressInput && !addressInput.value) addressInput.value = user.address || '';
  }

  goToCheckoutStep('info');
  const modal = document.getElementById('checkout-modal');
  if (modal) modal.classList.add('open');
}

function closeCheckoutModal() {
  const modal = document.getElementById('checkout-modal');
  if (modal) modal.classList.remove('open');
}

// Navigate between Step 1 (Info) and Step 2 (Payment)
function goToCheckoutStep(step) {
  const stepInfo = document.getElementById('checkout-step-info');
  const stepPayment = document.getElementById('checkout-step-payment');

  if (step === 'payment') {
    const name = document.getElementById('checkout-name').value.trim();
    const phone = document.getElementById('checkout-phone').value.trim();
    const address = document.getElementById('checkout-address').value.trim();

    if (!name || !phone || !address) {
      alert('Please fill in your Name, Phone Number, and Delivery Address to proceed.');
      return;
    }

    const totals = Cart.getTotal();
    const paymentSummaryEl = document.getElementById('payment-summary-display');
    if (paymentSummaryEl) {
      paymentSummaryEl.innerHTML = `
        <div style="font-size: 0.88rem; margin-bottom: 4px;">
          <span>Items: <b>${totals.count}</b> | Subtotal: <b>₹${totals.subtotal}</b></span><br>
          <span>GST (2.5% CGST + 2.5% SGST): <b>₹${totals.cgst + totals.sgst}</b></span>
        </div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #c0392b;">
          Payable Total: ₹${totals.total}
        </div>
        <div style="font-size: 0.8rem; color: #555; margin-top: 4px;">
          Deliver to: <b>${name}</b> (${phone})
        </div>
      `;
    }

    if (stepInfo) stepInfo.style.display = 'none';
    if (stepPayment) stepPayment.style.display = 'block';
  } else {
    if (stepInfo) stepInfo.style.display = 'block';
    if (stepPayment) stepPayment.style.display = 'none';
  }
}

function togglePaymentMethodDetails(method) {
  const upiBox = document.getElementById('upi-qr-box');
  if (upiBox) {
    upiBox.style.display = method === 'UPI' ? 'block' : 'none';
  }
}


// ==========================================================
// 5. ORDER SUBMISSION & BILL REDIRECTION
// ==========================================================
async function submitOrder() {
  const submitBtn = document.getElementById('submit-order-btn');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Saving Order to SQL...';
  }

  const customerName = document.getElementById('checkout-name').value.trim();
  const customerPhone = document.getElementById('checkout-phone').value.trim();
  const customerAddress = document.getElementById('checkout-address').value.trim();
  const paymentRadio = document.querySelector('input[name="paymentMethod"]:checked');
  const paymentMethod = paymentRadio ? paymentRadio.value : 'Cash on Delivery';

  const user = Auth.getUser();
  const items = Cart.getItems().map(item => ({
    productId: item.productId,
    weight: item.weight,
    quantity: item.quantity
  }));

  try {
    const res = await fetch(`${API_BASE}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: user ? user.id : null,
        customerName,
        customerPhone,
        customerAddress,
        paymentMethod,
        items
      })
    });

    const result = await res.json();
    if (!result.success) throw new Error(result.error || 'Failed to record order.');

    Cart.clear();
    closeCheckoutModal();
    // Redirect customer straight to their GST tax bill receipt
    window.location.href = `receipt.html?order=${encodeURIComponent(result.order.order_number)}`;
  } catch (err) {
    alert(`Order Error: ${err.message}`);
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Confirm & View Bill 🧾';
    }
  }
}

// Quick Buy directly adds item and opens checkout modal
function quickBuy(productId, productName, price1kg, price250g, selectedWeight = '1 Kg', imageUrl = '', marathiName = '') {
  Cart.addItem({
    id: productId,
    name: productName,
    marathi_name: marathiName,
    price_1kg: price1kg,
    price_250g: price250g,
    image_url: imageUrl
  }, selectedWeight, 1);

  openCheckoutModal();
}


// ==========================================================
// INITIALIZE ON DOM READY
// ==========================================================
document.addEventListener('DOMContentLoaded', () => {
  ensureCartAndCheckoutMarkup();
  Cart.updateCartBadge();
  Auth.updateUserNav();

  const checkoutModal = document.getElementById('checkout-modal');
  if (checkoutModal) {
    checkoutModal.addEventListener('click', (e) => {
      if (e.target === checkoutModal) closeCheckoutModal();
    });
  }
});
