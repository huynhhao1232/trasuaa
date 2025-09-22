from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('preparing', 'Đang chuẩn bị'),
        ('ready', 'Sẵn sàng'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('online', 'Thanh toán online'),
    ]

    customer_name = models.CharField(max_length=100, verbose_name="Tên khách hàng")
    customer_phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    customer_address = models.TextField(verbose_name="Địa chỉ giao hàng")
    customer_email = models.EmailField(blank=True, verbose_name="Email")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod', verbose_name="Phương thức thanh toán")
    payment_status = models.BooleanField(default=False, verbose_name="Đã thanh toán")
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Tổng tiền")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    # Admin user who processed the order
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Xử lý bởi")

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.customer_name}"

    @property
    def formatted_total(self):
        return f"{float(self.total_amount):,.0f} VNĐ"

    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

    @property
    def payment_method_display(self):
        return dict(self.PAYMENT_CHOICES)[self.payment_method]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Đơn hàng")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    quantity = models.PositiveIntegerField(verbose_name="Số lượng")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price

    @property
    def formatted_price(self):
        return f"{float(self.price):,.0f} VNĐ"

    @property
    def formatted_total(self):
        return f"{float(self.total_price):,.0f} VNĐ"