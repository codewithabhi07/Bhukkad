// ==========================================================
// Lucky Traders - Frontend Client Application
// Manages API data loading, cart with images, checkout, session & receipts
// ==========================================================

// Auto-detect if page is opened via file:// or http://
const API_BASE = (window.location.protocol === 'file:' || !window.location.origin.startsWith('http'))
  ? 'http://localhost:5000/api'
  : '/api';


// Cart Management with Image & Marathi Name Support
const Cart = {
  key: 'lucky_traders_cart',
  
  getItems() {
    try {
      const data = localStorage.getItem(this.key) || localStorage.getItem('bhukkad_cart');
      return data ? JSON.parse(data) : [];
    } catch (e) {
      return [];
    }
  },

  saveItems(items) {
    localStorage.setItem(this.key, JSON.stringify(items));
    this.updateCartBadge();
    this.renderCartDrawer();
  },

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
      // Update image if previously missing
      if (!items[existingIndex].imageUrl) items[existingIndex].imageUrl = imageUrl;
      if (!items[existingIndex].marathiName) items[existingIndex].marathiName = marathiName;
    } else {
      items.push({
        productId: product.id,
        productName: product.name,
        marathiName: marathiName,
        weight,
        unitPrice,
        quantity,
        subtotal: unitPrice * quantity,
        imageUrl: imageUrl
      });
    }

    this.saveItems(items);
    const displayName = marathiName ? `${marathiName} (${product.name})` : product.name;
    this.showToast(`Added ${quantity}x ${displayName} [${weight}] to cart!`);
  },

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

  removeItem(index) {
    const items = this.getItems();
    items.splice(index, 1);
    this.saveItems(items);
  },

  clear() {
    localStorage.removeItem(this.key);
    this.updateCartBadge();
    this.renderCartDrawer();
  },

  getTotal() {
    const items = this.getItems();
    const subtotal = items.reduce((sum, item) => sum + (item.subtotal || 0), 0);
    const cgst = Math.round((subtotal * 0.025) * 100) / 100;
    const sgst = Math.round((subtotal * 0.025) * 100) / 100;
    const total = Math.round((subtotal + cgst + sgst) * 100) / 100;
    return { subtotal, cgst, sgst, total, count: items.reduce((c, i) => c + i.quantity, 0) };
  },

  updateCartBadge() {
    const badges = document.querySelectorAll('.cart-count-badge');
    const { count } = this.getTotal();
    badges.forEach(b => {
      b.textContent = count;
      b.style.display = count > 0 ? 'inline-flex' : 'none';
    });
  },

  // Renders cart drawer WITH IMAGE THUMBNAILS for every single item!
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
        <div class="empty-cart-message" style="text-align: center; padding: 40px 10px;">
          <p style="font-size: 3rem; margin: 10px 0;">🛒</p>
          <p style="font-weight: 600;">Your cart is empty.</p>
          <p style="font-size: 0.85rem; color: #777; margin-top: 6px;">
            Explore our traditional masalas, dry chutneys, and pickles to add items!
          </p>
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
            <div class="cart-item-name">
              ${item.marathiName ? `<span class="cart-marathi-name">${item.marathiName}</span><br>` : ''}
              <span class="cart-english-name">${item.productName}</span>
            </div>
            <div class="cart-item-weight"><span class="badge-weight">${item.weight}</span> @ ₹${item.unitPrice}</div>
            <div class="cart-item-qty-controls">
              <button class="btn-qty" onclick="Cart.updateQuantity(${idx}, ${item.quantity - 1})">-</button>
              <span class="qty-num">${item.quantity}</span>
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
    toast._timer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2800);
  }
};

// User Session Management
const Auth = {
  key: 'lucky_traders_user',

  getUser() {
    try {
      const u = localStorage.getItem(this.key) || localStorage.getItem('bhukkad_user');
      return u ? JSON.parse(u) : null;
    } catch (e) {
      return null;
    }
  },

  setUser(user) {
    localStorage.setItem(this.key, JSON.stringify(user));
    this.updateUserNav();
  },

  logout() {
    localStorage.removeItem(this.key);
    localStorage.removeItem('bhukkad_user');
    window.location.href = 'login.html';
  },

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

// UI Toggles (Drawer & Modals)
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

// Multi-step Checkout Modal: Step 1 (Info) -> Step 2 (Payment) -> Bill
function openCheckoutModal() {
  const items = Cart.getItems();
  if (items.length === 0) {
    alert('Please add at least one product to your cart before proceeding to checkout.');
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
        <div style="font-size: 0.9rem; margin-bottom: 6px;">
          <span>Items: <b>${totals.count}</b> | Subtotal: <b>₹${totals.subtotal}</b></span><br>
          <span>GST (2.5% CGST + 2.5% SGST): <b>₹${totals.cgst + totals.sgst}</b></span>
        </div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #c0392b;">
          Payable Amount: ₹${totals.total}
        </div>
        <div style="font-size: 0.8rem; color: #555; margin-top: 4px;">
          Deliver to: <b>${name}</b>, ${phone}
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

// Order Submission (Step 2 -> Generate Bill)
async function submitOrder(event) {
  if (event) event.preventDefault();
  const submitBtn = document.getElementById('submit-order-btn');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processing in SQL & Generating Bill...';
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
    const response = await fetch(`${API_BASE}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: user ? user.id : null,
        customerName,
        customerPhone,
        customerAddress,
        paymentMethod,
        items,
        notes: ''
      })
    });

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'Failed to place order.');
    }

    Cart.clear();
    closeCheckoutModal();

    window.location.href = `receipt.html?order=${encodeURIComponent(result.order.order_number)}`;
  } catch (err) {
    alert(`Order submission error: ${err.message}`);
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Confirm Order & Generate Bill 🧾';
    }
  }
}

// Quick Buy directly from product card or table row
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

// Setup Event Listeners on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  // If user opened page via file:// protocol, show a prominent helper banner
  if (window.location.protocol === 'file:') {
    const pageName = window.location.pathname.split('/').pop() || 'index.html';
    const serverUrl = `http://localhost:5000/${pageName}`;
    const banner = document.createElement('div');
    banner.style.cssText = 'background: #c0392b; color: white; padding: 12px 16px; text-align: center; font-size: 0.95rem; position: sticky; top: 0; z-index: 10000; box-shadow: 0 4px 10px rgba(0,0,0,0.3);';
    banner.innerHTML = `
      <span>⚠️ <b>Notice:</b> You opened this directly as a file (<code>file://</code>). Web browsers block database fetch on local files!</span>
      <a href="${serverUrl}" style="background: white; color: #c0392b; padding: 6px 14px; border-radius: 4px; font-weight: bold; margin-left: 12px; text-decoration: none; display: inline-block;">
        🚀 Click to Open via Local Server (${serverUrl})
      </a>
    `;
    document.body.prepend(banner);
  }

  Cart.updateCartBadge();
  Auth.updateUserNav();

  const checkoutModal = document.getElementById('checkout-modal');
  if (checkoutModal) {
    checkoutModal.addEventListener('click', (e) => {
      if (e.target === checkoutModal) closeCheckoutModal();
    });
  }

  const overlay = document.getElementById('cart-overlay');
  if (overlay) {
    overlay.addEventListener('click', toggleCartDrawer);
  }
});
