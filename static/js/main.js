// Main JavaScript for Trà Sữa Online

// Global variables
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let products = [];
let banners = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    loadProducts();
    loadBanners();
    
    // Add event listeners
    document.addEventListener('click', handleClick);
});

// Handle click events
function handleClick(e) {
    if (e.target.classList.contains('btn-add-to-cart')) {
        e.preventDefault();
        const productId = parseInt(e.target.dataset.productId);
        addToCart(productId);
    }
    
    if (e.target.classList.contains('quantity-btn')) {
        const action = e.target.dataset.action;
        const productId = parseInt(e.target.dataset.productId);
        updateQuantity(productId, action);
    }
    
    if (e.target.classList.contains('remove-item')) {
        const productId = parseInt(e.target.dataset.productId);
        removeFromCart(productId);
    }
}

// Load products from API
async function loadProducts() {
    try {
        const response = await fetch('/api/products/products/');
        products = await response.json();
        renderProducts();
    } catch (error) {
        console.error('Error loading products:', error);
        showAlert('Không thể tải sản phẩm', 'danger');
    }
}

// Load banners from API
async function loadBanners() {
    try {
        const response = await fetch('/api/products/banners/');
        banners = await response.json();
        renderBanners();
    } catch (error) {
        console.error('Error loading banners:', error);
    }
}

// Render products
function renderProducts() {
    const container = document.getElementById('products-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    products.forEach(product => {
        const productCard = createProductCard(product);
        container.appendChild(productCard);
    });
}

// Render banners
function renderBanners() {
    const container = document.getElementById('banners-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    banners.forEach(banner => {
        const bannerCard = createBannerCard(banner);
        container.appendChild(bannerCard);
    });
}

// Create product card HTML
function createProductCard(product) {
    const div = document.createElement('div');
    div.className = 'col-md-4 col-lg-3 mb-4';
    
    // Create status badge if product has status
    let statusBadge = '';
    if (product.status) {
        const statusClass = getStatusBadgeClass(product.status);
        let statusText = product.get_status_display;
        
        // Special handling for sale status
        if (product.status === 'sale' && parseInt(product.discount_percentage) > 0) {
            statusText = `-${product.discount_percentage}%`;
        }
        
        statusBadge = `<span class="badge ${statusClass} product-status-badge">${statusText}</span>`;
    }
    
    div.innerHTML = `
        <div class="product-card">
            <div class="product-image-container">
                <img src="${product.image}" alt="${product.name}" class="product-image">
                ${statusBadge}
            </div>
            <div class="product-info">
                <h5 class="product-title">${product.name}</h5>
                <p class="product-description">${product.description}</p>
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div class="product-price-container">
                        ${product.status === 'sale' && product.original_price ? 
                            `<div class="price-row">
                                <span class="product-price-sale">${product.formatted_price}</span>
                                <span class="product-price-original">${product.formatted_original_price}</span>
                            </div>` : 
                            `<span class="product-price">${product.formatted_price}</span>`
                        }
                    </div>
                    <span class="size-badge">${product.get_size_display}</span>
                </div>
                <button class="btn btn-add-to-cart" data-product-id="${product.id}">
                    <i class="fas fa-shopping-cart"></i> Thêm vào giỏ
                </button>
            </div>
        </div>
    `;
    return div;
}

// Get status badge class for frontend
function getStatusBadgeClass(status) {
    switch(status) {
        case 'hot': return 'bg-danger';
        case 'sale': return 'bg-success';
        case 'sold_out': return 'bg-secondary';
        default: return 'bg-light text-dark';
    }
}

// Create banner card HTML
function createBannerCard(banner) {
    const div = document.createElement('div');
    div.className = 'col-md-6 mb-4';
    div.innerHTML = `
        <div class="banner-card">
            <img src="${banner.image}" alt="${banner.title}" class="banner-image">
            <div class="banner-content">
                <h3 class="banner-title">${banner.title}</h3>
                <p class="banner-subtitle">${banner.subtitle}</p>
            </div>
        </div>
    `;
    return div;
}

// Add product to cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image,
            quantity: 1
        });
    }
    
    saveCart();
    updateCartCount();
    showAlert(`${product.name} đã được thêm vào giỏ hàng!`, 'success');
}

// Update quantity
function updateQuantity(productId, action) {
    const item = cart.find(item => item.id === productId);
    if (!item) return;
    
    if (action === 'increase') {
        item.quantity += 1;
    } else if (action === 'decrease' && item.quantity > 1) {
        item.quantity -= 1;
    }
    
    saveCart();
    updateCartCount();
    renderCart();
}

// Remove from cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    updateCartCount();
    renderCart();
    showAlert('Sản phẩm đã được xóa khỏi giỏ hàng!', 'info');
}

// Save cart to localStorage
function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Update cart count in navbar
function updateCartCount() {
    const countElement = document.getElementById('cart-count');
    if (countElement) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        countElement.textContent = totalItems;
    }
}

// Render cart page
function renderCart() {
    const container = document.getElementById('cart-container');
    if (!container) return;
    
    if (cart.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
                <h4>Giỏ hàng trống</h4>
                <p>Hãy thêm sản phẩm vào giỏ hàng để tiếp tục mua sắm!</p>
                <a href="/" class="btn btn-primary">Tiếp tục mua sắm</a>
            </div>
        `;
        return;
    }
    
    let total = 0;
    container.innerHTML = '';
    
    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div class="row align-items-center">
                <div class="col-md-2">
                    <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                </div>
                <div class="col-md-4">
                    <h6>${item.name}</h6>
                </div>
                <div class="col-md-2">
                    <span class="text-muted">${formatPrice(item.price)}</span>
                </div>
                <div class="col-md-2">
                    <div class="quantity-controls">
                        <button class="btn btn-sm quantity-btn" data-action="decrease" data-product-id="${item.id}">-</button>
                        <span class="mx-2">${item.quantity}</span>
                        <button class="btn btn-sm quantity-btn" data-action="increase" data-product-id="${item.id}">+</button>
                    </div>
                </div>
                <div class="col-md-1">
                    <span class="fw-bold">${formatPrice(itemTotal)}</span>
                </div>
                <div class="col-md-1">
                    <button class="btn btn-sm btn-outline-danger remove-item" data-product-id="${item.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
        container.appendChild(cartItem);
    });
    
    // Add total and checkout button
    const totalDiv = document.createElement('div');
    totalDiv.className = 'text-end mt-4';
    totalDiv.innerHTML = `
        <h5>Tổng cộng: <span class="text-primary">${formatPrice(total)}</span></h5>
        <a href="/checkout/" class="btn btn-primary btn-lg">Thanh toán</a>
    `;
    container.appendChild(totalDiv);
}

// Format price
function formatPrice(price) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(price);
}

// Show alert
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    }
}

// Submit order
async function submitOrder(formData) {
    try {
        const orderData = {
            customer_name: formData.get('customer_name'),
            customer_phone: formData.get('customer_phone'),
            customer_address: formData.get('customer_address'),
            customer_email: formData.get('customer_email'),
            payment_method: formData.get('payment_method'),
            notes: formData.get('notes'),
            items: cart.map(item => ({
                product_id: item.id,
                quantity: item.quantity
            }))
        };
        
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                         document.querySelector('meta[name=csrf-token]')?.getAttribute('content');
        
        const response = await fetch('/api/orders/orders/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(orderData)
        });
        
        if (response.ok) {
            const order = await response.json();
            // Clear cart
            cart = [];
            saveCart();
            updateCartCount();
            
            // Redirect to success page
            window.location.href = `/order-success/?order_id=${order.id}`;
        } else {
            const error = await response.json();
            showAlert('Có lỗi xảy ra khi đặt hàng: ' + (error.detail || 'Vui lòng thử lại'), 'danger');
        }
    } catch (error) {
        console.error('Error submitting order:', error);
        showAlert('Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại!', 'danger');
    }
}

// Load orders for admin
async function loadOrders() {
    try {
        const response = await fetch('/api/orders/orders/');
        const orders = await response.json();
        renderOrders(orders);
    } catch (error) {
        console.error('Error loading orders:', error);
        showAlert('Không thể tải danh sách đơn hàng', 'danger');
    }
}

// Render orders for admin
function renderOrders(orders) {
    const container = document.getElementById('orders-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    orders.forEach(order => {
        const orderDiv = document.createElement('div');
        orderDiv.className = 'admin-card';
        orderDiv.innerHTML = `
            <div class="row">
                <div class="col-md-8">
                    <h6>Đơn hàng #${order.id}</h6>
                    <p><strong>Khách hàng:</strong> ${order.customer_name}</p>
                    <p><strong>SĐT:</strong> ${order.customer_phone}</p>
                    <p><strong>Địa chỉ:</strong> ${order.customer_address}</p>
                    <p><strong>Tổng tiền:</strong> ${order.formatted_total}</p>
                </div>
                <div class="col-md-4 text-end">
                    <span class="status-badge status-${order.status}">${order.status_display}</span>
                    <div class="mt-2">
                        <select class="form-select form-select-sm" onchange="updateOrderStatus(${order.id}, this.value)">
                            <option value="pending" ${order.status === 'pending' ? 'selected' : ''}>Chờ xử lý</option>
                            <option value="confirmed" ${order.status === 'confirmed' ? 'selected' : ''}>Đã xác nhận</option>
                            <option value="preparing" ${order.status === 'preparing' ? 'selected' : ''}>Đang chuẩn bị</option>
                            <option value="ready" ${order.status === 'ready' ? 'selected' : ''}>Sẵn sàng</option>
                            <option value="delivered" ${order.status === 'delivered' ? 'selected' : ''}>Đã giao</option>
                            <option value="cancelled" ${order.status === 'cancelled' ? 'selected' : ''}>Đã hủy</option>
                        </select>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(orderDiv);
    });
}

// Update order status
async function updateOrderStatus(orderId, newStatus) {
    try {
        const response = await fetch(`/api/orders/orders/${orderId}/status/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (response.ok) {
            showAlert('Cập nhật trạng thái đơn hàng thành công!', 'success');
            loadOrders(); // Reload orders
        } else {
            showAlert('Có lỗi xảy ra khi cập nhật trạng thái', 'danger');
        }
    } catch (error) {
        console.error('Error updating order status:', error);
        showAlert('Có lỗi xảy ra khi cập nhật trạng thái', 'danger');
    }
}
