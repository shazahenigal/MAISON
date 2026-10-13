// MAISON Fashion House - Tickets JavaScript

function getCart() {
  return JSON.parse(localStorage.getItem('maison_tickets_cart')) || [];
}

function saveCart(cart) {
  localStorage.setItem('maison_tickets_cart', JSON.stringify(cart));
  updateCartCount();
}

function updateCartCount() {
  const cart = getCart();
  const count = cart.reduce((sum, item) => sum + item.quantity, 0);
  const countEl = document.getElementById('cartCount');
  if (countEl) countEl.innerText = count;
}

window.addToCart = function(ticketId, title, price) {
  let cart = getCart();
  const existing = cart.find(item => item.id === ticketId);

  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ id: ticketId, title: title, price: parseFloat(price), quantity: 1 });
  }

  saveCart(cart);
  openMyCart();
};

window.openMyCart = function() {
  const cartDrawer = document.getElementById('cartDrawer');
  const cartOverlay = document.getElementById('cartOverlay');
  
  if (cartDrawer) cartDrawer.classList.add('open');
  if (cartOverlay) cartOverlay.style.display = 'block';
  renderCartItems();
};

window.closeMyCart = function() {
  const cartDrawer = document.getElementById('cartDrawer');
  const cartOverlay = document.getElementById('cartOverlay');
  
  if (cartDrawer) cartDrawer.classList.remove('open');
  if (cartOverlay) cartOverlay.style.display = 'none';
};

document.addEventListener('DOMContentLoaded', () => {
  updateCartCount();
});

let currentDiscountRate = 0;

function renderCartItems() {
  const container = document.getElementById('cartItemsContainer');
  if (!container) return;

  const cart = getCart();

  if (cart.length === 0) {
    container.innerHTML = `<p style="text-align: center; color: var(--text-muted); margin-top: 40px; font-size: 14px;">No runway passes selected yet.</p>`;
    updateTotals(0, 0);
    return;
  }

  container.innerHTML = cart.map(item => `
    <div style="display: flex; gap: 15px; align-items: center; margin-bottom: 15px; border-bottom: 1px solid var(--border-color); padding-bottom: 15px;">
      <div style="flex: 1;">
        <h4 style="font-size: 14px; font-family: 'Playfair Display', serif; color: var(--text-main);">${item.title}</h4>
        <p style="font-size: 12px; color: var(--accent-gold);">${item.price} EGP x ${item.quantity}</p>
      </div>
      <div style="display: flex; gap: 5px;">
        <button onclick="updateQty(${item.id}, 1)" style="padding: 4px 8px; cursor: pointer; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 4px;">+</button>
        <button onclick="updateQty(${item.id}, -1)" style="padding: 4px 8px; cursor: pointer; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 4px;">-</button>
      </div>
    </div>
  `).join('');

  calculateTotals();
}

window.updateQty = function(ticketId, change) {
  let cart = getCart();
  const item = cart.find(i => i.id === ticketId);
  if (!item) return;

  item.quantity += change;
  if (item.quantity <= 0) {
    cart = cart.filter(i => i.id !== ticketId);
  }

  saveCart(cart);
  renderCartItems();
};

function calculateTotals() {
  const cart = getCart();
  let subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const discount = subtotal * currentDiscountRate;
  const total = subtotal - discount;

  updateTotals(subtotal, discount, total);
}

function updateTotals(subtotal, discount, total = subtotal - discount) {
  const subEl = document.getElementById('cartSubtotal');
  const discRow = document.getElementById('discountRow');
  const discEl = document.getElementById('cartDiscount');
  const totEl = document.getElementById('cartTotal');

  if (subEl) subEl.innerText = `${subtotal.toFixed(2)} EGP`;
  if (totEl) totEl.innerText = `${total.toFixed(2)} EGP`;

  if (discRow && discEl) {
    if (discount > 0) {
      discRow.style.display = 'flex';
      discEl.innerText = `-${discount.toFixed(2)} EGP`;
    } else {
      discRow.style.display = 'none';
    }
  }
}

const applyPromoBtn = document.getElementById('applyPromoBtn');
const promoInput = document.getElementById('promoInput');
const promoMessage = document.getElementById('promoMessage');

if (applyPromoBtn) {
  applyPromoBtn.addEventListener('click', () => {
    const code = promoInput.value.trim();
    if (!code) return;

    if (code.toUpperCase() === 'MAISONVIP') {
      currentDiscountRate = 0.15;
      promoMessage.style.color = '#27ae60';
      promoMessage.innerText = 'VIP Pass Applied: 15% OFF!';
    } else {
      currentDiscountRate = 0;
      promoMessage.style.color = '#c0392b';
      promoMessage.innerText = 'Invalid promo code.';
    }
    calculateTotals();
  });
}

const checkoutBtn = document.getElementById('checkoutBtn');
if (checkoutBtn) {
  checkoutBtn.addEventListener('click', () => {
    const cart = getCart();
    if (cart.length === 0) {
      alert('Your booking bag is empty.');
      return;
    }
    alert('Thank you for booking with MAISON! Your runway passes have been securely reserved via Visa.');
    
    localStorage.removeItem('maison_tickets_cart');
    currentDiscountRate = 0;
    updateCartCount();
    closeMyCart();
  });
} 