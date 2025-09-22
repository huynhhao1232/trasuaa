from django.urls import path
from . import views

urlpatterns = [
    # User pages
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order-success'),
    path('track-order/', views.track_order, name='track-order'),
    
    # Admin authentication
    path('admin-login/', views.admin_login, name='admin-login'),
    path('admin-logout/', views.admin_logout, name='admin-logout'),
    
    # Admin pages
    path('admin-panel/', views.admin_panel, name='admin-panel'),
    path('admin-panel/products/', views.admin_products, name='admin-products'),
    path('admin-panel/orders/', views.admin_orders, name='admin-orders'),
    path('admin-panel/banners/', views.admin_banners, name='admin-banners'),
    
    # Admin API endpoints
    path('api/admin/products/', views.create_product, name='create-product'),
    path('api/admin/products/<int:product_id>/', views.update_product, name='update-product'),
    path('api/admin/products/<int:product_id>/delete/', views.delete_product, name='delete-product'),
    path('api/admin/banners/', views.create_banner, name='create-banner'),
    path('api/admin/banners/<int:banner_id>/', views.update_banner, name='update-banner'),
    path('api/admin/banners/<int:banner_id>/delete/', views.delete_banner, name='delete-banner'),
]
