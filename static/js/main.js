// Art Market Faridabad - Core Frontend & E-Commerce State Engine

const STORE_WHATSAPP_NUMBER = "919876543210";
const FREE_SHIPPING_THRESHOLD = 1999;

// Load Cart from LocalStorage
function getCart() {
    try {
        const cart = localStorage.getItem('artmarket_cart');
        return cart ? JSON.parse(cart) : [];
    } catch (e) {
        return [];
    }
}

function saveCart(cart) {
    localStorage.setItem('artmarket_cart', JSON.stringify(cart));
    updateCartUI();
}

// Add Item to Cart
function addToCart(id, name, price, image, sku) {
    let cart = getCart();
    const existingIndex = cart.findIndex(item => item.id == id);
    
    if (existingIndex > -1) {
        cart[existingIndex].quantity += 1;
    } else {
        cart.push({
            id: id,
            name: name,
            price: parseFloat(price),
            image: image,
            sku: sku || ('AMF-' + id),
            quantity: 1
        });
    }

    saveCart(cart);
    showToast(`Added "${name}" to your cart!`);
    openCartDrawer();
}

// Update Quantity
function updateCartQuantity(id, delta) {
    let cart = getCart();
    const item = cart.find(i => i.id == id);
    if (item) {
        item.quantity += delta;
        if (item.quantity <= 0) {
            cart = cart.filter(i => i.id != id);
        }
        saveCart(cart);
    }
}

// Remove Item
function removeFromCart(id) {
    let cart = getCart();
    cart = cart.filter(i => i.id != id);
    saveCart(cart);
    showToast('Item removed from cart');
}

// Clear Cart
function clearCart() {
    if (confirm('Are you sure you want to clear your shopping cart?')) {
        saveCart([]);
        showToast('Cart has been cleared');
    }
}

// Update All Cart UI Elements
function updateCartUI() {
    const cart = getCart();
    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    // 1. Update Header Badge
    const badge = document.getElementById('cartCountBadge');
    if (badge) {
        badge.innerText = totalCount;
        badge.classList.toggle('hidden', totalCount === 0);
    }

    // 2. Update Drawer Subtotal & Grand Total
    const subtotalEl = document.getElementById('cartSubtotal');
    const grandTotalEl = document.getElementById('cartGrandTotal');
    if (subtotalEl) subtotalEl.innerText = `?${subtotal.toLocaleString('en-IN')}`;
    if (grandTotalEl) grandTotalEl.innerText = `?${subtotal.toLocaleString('en-IN')}`;

    // 3. Update Free Shipping Bar
    const progressBar = document.getElementById('shippingProgressBar');
    const progressText = document.getElementById('shippingProgressText');
    if (progressBar && progressText) {
        if (subtotal >= FREE_SHIPPING_THRESHOLD) {
            progressBar.style.width = '100%';
            progressBar.classList.add('bg-emerald-600');
            progressText.innerText = '?? You unlocked Free Delivery in Faridabad & NCR!';
        } else {
            const pct = Math.min(100, Math.round((subtotal / FREE_SHIPPING_THRESHOLD) * 100));
            progressBar.style.width = `${pct}%`;
            progressBar.classList.remove('bg-emerald-600');
            const diff = FREE_SHIPPING_THRESHOLD - subtotal;
            progressText.innerText = `Add ?${diff.toLocaleString('en-IN')} more for Free Delivery`;
        }
    }

    // 4. Render Drawer Items
    const drawerList = document.getElementById('cartItemsList');
    if (drawerList) {
        if (cart.length === 0) {
            drawerList.innerHTML = `
                <div class="text-center py-12 space-y-3">
                    <div class="w-14 h-14 rounded-full bg-stone-100 text-stone-400 flex items-center justify-center mx-auto text-xl">
                        <i class="fas fa-shopping-bag"></i>
                    </div>
                    <p class="font-cinzel text-sm font-bold text-stone-700">Your cart is empty</p>
                    <p class="text-xs text-stone-500">Explore our antique decor and botanical plants collection.</p>
                </div>
            `;
        } else {
            drawerList.innerHTML = cart.map(item => `
                <div class="flex items-center gap-3 p-3 bg-stone-50 rounded-xl border border-stone-100">
                    <img src="${item.image}" alt="${item.name}" class="w-14 h-14 object-cover rounded-lg flex-shrink-0 bg-stone-200">
                    <div class="flex-grow min-w-0">
                        <h4 class="text-xs font-bold text-stone-900 truncate">${item.name}</h4>
                        <span class="text-[10px] text-stone-500 font-mono">${item.sku}</span>
                        <div class="flex items-center justify-between mt-2">
                            <span class="text-xs font-bold text-amber-900">?${(item.price * item.quantity).toLocaleString('en-IN')}</span>
                            <div class="flex items-center border border-stone-200 rounded-lg bg-white overflow-hidden text-xs">
                                <button onclick="updateCartQuantity('${item.id}', -1)" class="px-2 py-0.5 hover:bg-stone-100 text-stone-600">-</button>
                                <span class="px-2 py-0.5 font-bold text-stone-800">${item.quantity}</span>
                                <button onclick="updateCartQuantity('${item.id}', 1)" class="px-2 py-0.5 hover:bg-stone-100 text-stone-600">+</button>
                            </div>
                        </div>
                    </div>
                    <button onclick="removeFromCart('${item.id}')" class="text-stone-400 hover:text-rose-600 p-1 text-xs" title="Remove">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            `).join('');
        }
    }

    // 5. Render Full Cart Page (if on /cart/)
    const fullCartContainer = document.getElementById('fullCartItemsContainer');
    if (fullCartContainer) {
        const pageSubtotal = document.getElementById('pageCartSubtotal');
        const pageTotal = document.getElementById('pageCartTotal');
        if (pageSubtotal) pageSubtotal.innerText = `?${subtotal.toLocaleString('en-IN')}`;
        if (pageTotal) pageTotal.innerText = `?${subtotal.toLocaleString('en-IN')}`;

        if (cart.length === 0) {
            fullCartContainer.innerHTML = `
                <div class="text-center py-16 p-6 space-y-4">
                    <div class="w-16 h-16 rounded-full bg-stone-100 text-stone-400 flex items-center justify-center mx-auto text-2xl">
                        <i class="fas fa-shopping-bag"></i>
                    </div>
                    <h3 class="font-cinzel text-lg font-bold text-stone-800">Your cart is currently empty</h3>
                    <p class="text-xs text-stone-500">Looks like you haven't added any antique decor or artificial plants yet.</p>
                    <a href="/shop/" class="inline-block px-6 py-2.5 bg-stone-900 text-white rounded-xl text-xs font-semibold hover:bg-stone-800">
                        Explore Catalog &rarr;
                    </a>
                </div>
            `;
        } else {
            fullCartContainer.innerHTML = cart.map(item => `
                <div class="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div class="flex items-center gap-4">
                        <img src="${item.image}" alt="${item.name}" class="w-16 h-16 sm:w-20 sm:h-20 object-cover rounded-xl bg-stone-100 flex-shrink-0">
                        <div>
                            <h4 class="font-cinzel text-sm font-bold text-stone-900">${item.name}</h4>
                            <span class="text-xs text-stone-500 font-mono">${item.sku}</span>
                            <span class="text-xs text-amber-800 font-semibold block mt-1">?${item.price.toLocaleString('en-IN')} each</span>
                        </div>
                    </div>
                    <div class="flex items-center justify-between sm:justify-end gap-6">
                        <div class="flex items-center border border-stone-200 rounded-xl bg-white overflow-hidden text-sm">
                            <button onclick="updateCartQuantity('${item.id}', -1)" class="px-3 py-1 hover:bg-stone-100 text-stone-600">-</button>
                            <span class="px-3 py-1 font-bold text-stone-800">${item.quantity}</span>
                            <button onclick="updateCartQuantity('${item.id}', 1)" class="px-3 py-1 hover:bg-stone-100 text-stone-600">+</button>
                        </div>
                        <span class="font-bold text-stone-900 text-base">?${(item.price * item.quantity).toLocaleString('en-IN')}</span>
                        <button onclick="removeFromCart('${item.id}')" class="text-stone-400 hover:text-rose-600 text-sm">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        }
    }

    // 6. Render Checkout Page Items & Update Form inputs (if on /checkout/)
    const checkoutList = document.getElementById('checkoutItemsList');
    if (checkoutList) {
        const subDisplay = document.getElementById('checkoutSubtotalDisplay');
        const totalDisplay = document.getElementById('checkoutTotalDisplay');
        const hiddenAmount = document.getElementById('checkoutTotalAmount');
        const hiddenItems = document.getElementById('checkoutItemsJson');

        if (subDisplay) subDisplay.innerText = `?${subtotal.toLocaleString('en-IN')}`;
        if (totalDisplay) totalDisplay.innerText = `?${subtotal.toLocaleString('en-IN')}`;
        if (hiddenAmount) hiddenAmount.value = subtotal;
        if (hiddenItems) hiddenItems.value = JSON.stringify(cart);

        if (cart.length === 0) {
            checkoutList.innerHTML = `<p class="text-xs text-stone-500 text-center py-4">No items in cart. Please add items before checking out.</p>`;
        } else {
            checkoutList.innerHTML = cart.map(item => `
                <div class="flex items-center justify-between text-xs py-2">
                    <div class="flex items-center gap-2 truncate">
                        <span class="font-bold text-stone-700">${item.quantity}?</span>
                        <span class="text-stone-800 truncate">${item.name}</span>
                    </div>
                    <span class="font-semibold text-stone-900 flex-shrink-0">?${(item.price * item.quantity).toLocaleString('en-IN')}</span>
                </div>
            `).join('');
        }
    }
}

// Drawer Toggle Logic
function openCartDrawer() {
    const drawer = document.getElementById('cartDrawer');
    const overlay = document.getElementById('cartDrawerOverlay');
    if (drawer && overlay) {
        overlay.classList.remove('hidden');
        drawer.classList.remove('translate-x-full');
    }
}

function closeCartDrawer() {
    const drawer = document.getElementById('cartDrawer');
    const overlay = document.getElementById('cartDrawerOverlay');
    if (drawer && overlay) {
        drawer.classList.add('translate-x-full');
        overlay.classList.add('hidden');
    }
}

// Toast Notification
function showToast(message) {
    const existing = document.getElementById('appToast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.id = 'appToast';
    toast.className = 'fixed bottom-24 right-6 z-50 bg-stone-900 text-white text-xs font-semibold px-4 py-3 rounded-2xl shadow-2xl flex items-center gap-2 border border-amber-500/30 toast-badge';
    toast.innerHTML = `<i class="fas fa-check-circle text-emerald-400"></i> <span>${message}</span>`;
    document.body.appendChild(toast);

    setTimeout(() => {
        if (toast) toast.remove();
    }, 3000);
}

// Send Whole Cart to WhatsApp
function sendCartToWhatsApp() {
    const cart = getCart();
    if (cart.length === 0) {
        alert('Your cart is empty! Please add some antique decor or plants first.');
        return;
    }

    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    let msg = `*??? New Order Request - Art Market Faridabad*%0A%0A`;
    msg += `Hello! I would like to place an order for the following items:%0A`;
    
    cart.forEach((item, index) => {
        msg += `%0A${index + 1}. *${item.name}*%0A   - SKU: ${item.sku}%0A   - Qty: ${item.quantity} ? ?${item.price}%0A   - Subtotal: ?${item.price * item.quantity}`;
    });

    msg += `%0A%0A*?? Total Cart Amount: ?${subtotal.toLocaleString('en-IN')}*%0A`;
    msg += `?? Please confirm home delivery availability and payment options for Faridabad / Delhi NCR.`;

    const url = `https://wa.me/${STORE_WHATSAPP_NUMBER}?text=${msg}`;
    window.open(url, '_blank');
}

// Initialize Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();

    // Drawer triggers
    const cartOpenBtn = document.getElementById('cartDrawerBtn');
    const cartCloseBtn = document.getElementById('cartDrawerCloseBtn');
    const overlay = document.getElementById('cartDrawerOverlay');
    const whatsappCartBtn = document.getElementById('whatsappCartOrderBtn');
    const pageWhatsappCartBtn = document.getElementById('pageWhatsappCartBtn');

    if (cartOpenBtn) cartOpenBtn.addEventListener('click', openCartDrawer);
    if (cartCloseBtn) cartCloseBtn.addEventListener('click', closeCartDrawer);
    if (overlay) overlay.addEventListener('click', closeCartDrawer);
    if (whatsappCartBtn) whatsappCartBtn.addEventListener('click', sendCartToWhatsApp);
    if (pageWhatsappCartBtn) pageWhatsappCartBtn.addEventListener('click', sendCartToWhatsApp);

    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Live Search Overlay Logic
    const searchOpenBtn = document.getElementById('searchOpenBtn');
    const searchModal = document.getElementById('searchModal');
    const searchCloseBtn = document.getElementById('searchCloseBtn');
    const liveSearchInput = document.getElementById('liveSearchInput');
    const searchResults = document.getElementById('searchResults');

    if (searchOpenBtn && searchModal) {
        searchOpenBtn.addEventListener('click', () => {
            searchModal.classList.remove('hidden');
            searchModal.classList.add('flex');
            if (liveSearchInput) liveSearchInput.focus();
        });
    }

    if (searchCloseBtn && searchModal) {
        searchCloseBtn.addEventListener('click', () => {
            searchModal.classList.add('hidden');
            searchModal.classList.remove('flex');
        });
    }

    if (searchModal) {
        searchModal.addEventListener('click', (e) => {
            if (e.target === searchModal) {
                searchModal.classList.add('hidden');
                searchModal.classList.remove('flex');
            }
        });
    }

    // Debounced Search AJAX
    let searchDebounce = null;
    if (liveSearchInput && searchResults) {
        liveSearchInput.addEventListener('input', (e) => {
            clearTimeout(searchDebounce);
            const val = e.target.value.trim();
            if (val.length < 2) {
                searchResults.innerHTML = `<div class="text-center py-8 text-stone-400 text-xs">Type at least 2 characters to search...</div>`;
                return;
            }

            searchDebounce = setTimeout(() => {
                fetch(`/api/products/?q=${encodeURIComponent(val)}`)
                    .then(res => res.json())
                    .then(data => {
                        if (!data.products || data.products.length === 0) {
                            searchResults.innerHTML = `<div class="text-center py-8 text-stone-400 text-xs">No matching products found for "${val}"</div>`;
                            return;
                        }

                        searchResults.innerHTML = data.products.map(p => `
                            <a href="/product/${p.slug}/" class="flex items-center gap-3 p-3 hover:bg-stone-50 rounded-xl transition-colors">
                                <img src="${p.image_url}" alt="${p.name}" class="w-12 h-12 object-cover rounded-lg bg-stone-100 flex-shrink-0">
                                <div class="flex-grow min-w-0">
                                    <h4 class="text-xs font-bold text-stone-900 truncate">${p.name}</h4>
                                    <span class="text-[10px] text-amber-800 font-semibold">${p.category}</span>
                                </div>
                                <div class="text-right">
                                    <span class="text-xs font-bold text-stone-900">?${p.price.toLocaleString('en-IN')}</span>
                                    <span class="block text-[10px] text-emerald-600 font-semibold">View &rarr;</span>
                                </div>
                            </a>
                        `).join('');
                    })
                    .catch(() => {
                        searchResults.innerHTML = `<div class="text-center py-4 text-rose-500 text-xs">Error searching products.</div>`;
                    });
            }, 250);
        });
    }
});
