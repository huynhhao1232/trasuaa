from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/create/', views.CreateOrderView.as_view(), name='create-order'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update-order-status'),
    path('stats/', views.order_stats, name='order-stats'),
]
