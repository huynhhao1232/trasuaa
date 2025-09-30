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
    
    // Initialize sticky navbar
    initStickyNavbar();
});

// Handle click events
function handleClick(e) {
    if (e.target.classList.contains('btn-add-to-cart')) {
        e.preventDefault();
        const productId = parseInt(e.target.dataset.productId);
        addToCart(productId);
    }
    
    if (e.target.classList.contains('quantity-btn') || e.target.classList.contains('quantity-btn-modern')) {
        const action = e.target.getAttribute('data-action');
        const productId = parseInt(e.target.getAttribute('data-product-id'));
        updateQuantity(productId, action);
    }
    
    if (e.target.classList.contains('remove-item') || e.target.classList.contains('remove-btn-modern')) {
        const productId = parseInt(e.target.getAttribute('data-product-id'));
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
        
        // Check if product is in cart and update status
        const item = cart.find(item => item.id === product.id);
        if (item) {
            updateProductStatus(product.id, true);
        }
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
                    <span class="size-badge" id="status-${product.id}">${product.get_size_display}</span>
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
    
    // Update status badge to show "Đã chọn"
    updateProductStatus(productId, true);
    
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
    
    // Update status badge back to original size
    updateProductStatus(productId, false);
    
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
        
        // Add/remove animation class based on cart content
        if (totalItems > 0) {
            countElement.classList.add('has-items');
        } else {
            countElement.classList.remove('has-items');
        }
    }
}

// Render cart page
function renderCart() {
    const container = document.getElementById('cart-container');
    const emptyState = document.getElementById('cart-empty');
    
    if (!container) return;

    if (cart.length === 0) {
        container.style.display = 'none';
        if (emptyState) {
            emptyState.style.display = 'block';
        }
        return;
    }

    // Hide empty state and show cart
    if (emptyState) {
        emptyState.style.display = 'none';
    }
    container.style.display = 'block';

    let total = 0;
    container.innerHTML = '';

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item-modern';
        cartItem.innerHTML = `
            <div class="cart-item-content">
                <div class="cart-item-image-container">
                    <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                </div>
                <div class="cart-item-details">
                    <h5 class="cart-item-name">${item.name}</h5>
                    <p class="cart-item-price">${formatPrice(item.price)} mỗi sản phẩm</p>
                </div>
                <div class="cart-item-quantity">
                    <div class="quantity-controls-modern">
                        <button class="quantity-btn-modern decrease" data-action="decrease" data-product-id="${item.id}">
                            <i class="fas fa-minus"></i>
                        </button>
                        <span class="quantity-number">${item.quantity}</span>
                        <button class="quantity-btn-modern increase" data-action="increase" data-product-id="${item.id}">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                </div>
                <div class="cart-item-total">
                    <span class="total-price">${formatPrice(itemTotal)}</span>
                </div>
                <div class="cart-item-actions">
                    <button class="remove-btn-modern" data-product-id="${item.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
        container.appendChild(cartItem);
    });

    // Add total and checkout button
    const totalDiv = document.createElement('div');
    totalDiv.className = 'cart-summary-modern';
    totalDiv.innerHTML = `
        <div class="summary-card">
            <div class="summary-content">
                <h3 class="summary-title">Tổng cộng</h3>
                <div class="summary-total">
                    <span class="total-amount">${formatPrice(total)}</span>
                </div>
                <button class="checkout-btn-modern" onclick="window.location.href='/checkout/'">
                    <i class="fas fa-credit-card"></i>
                    <span>Thanh toán ngay</span>
                </button>
            </div>
        </div>
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
        
        const response = await fetch('/api/orders/create/', {
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
        const response = await fetch('/api/orders/');
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
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                         document.querySelector('meta[name=csrf-token]')?.getAttribute('content');
        
        const response = await fetch(`/api/orders/${orderId}/status/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (response.ok) {
            showAlert('Cập nhật trạng thái đơn hàng thành công!', 'success');
            loadOrders(); // Reload orders
        } else {
            console.error('Order status update failed:', response.status, response.statusText);
            const errorData = await response.text();
            console.error('Error response:', errorData);
            showAlert('Có lỗi xảy ra khi cập nhật trạng thái', 'danger');
        }
    } catch (error) {
        console.error('Error updating order status:', error);
        showAlert('Có lỗi xảy ra khi cập nhật trạng thái', 'danger');
    }
}

// Update product status badge
function updateProductStatus(productId, isSelected) {
    const statusElement = document.getElementById(`status-${productId}`);
    if (statusElement) {
        if (isSelected) {
            statusElement.textContent = 'Đã chọn';
            statusElement.className = 'size-badge selected-badge';
        } else {
            // Find the product to get its original size
            const product = products.find(p => p.id === productId);
            if (product) {
                statusElement.textContent = product.get_size_display;
                statusElement.className = 'size-badge';
            }
        }
    }
}

// Initialize sticky navbar functionality
function initStickyNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    let lastScrollTop = 0;
    let ticking = false;
    
    function updateNavbar() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add scrolled class when scrolling down
        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Always keep navbar visible - no hiding/showing
        navbar.style.transform = 'translateY(0)';
        
        lastScrollTop = scrollTop;
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateNavbar);
            ticking = true;
        }
    }
    
    // Listen for scroll events
    window.addEventListener('scroll', requestTick, { passive: true });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}
