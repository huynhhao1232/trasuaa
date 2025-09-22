from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Nhỏ'),
        ('M', 'Vừa'),
        ('L', 'Lớn'),
    ]
    
    STATUS_CHOICES = [
        ('', 'Không hiển thị'),
        ('hot', 'Hot'),
        ('sale', 'Giảm giá'),
        ('sold_out', 'Hết hàng'),
    ]

    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    description = models.TextField(verbose_name="Mô tả")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Danh mục")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá")
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='M', verbose_name="Kích thước")
    image = models.ImageField(upload_to='products/', verbose_name="Hình ảnh")
    is_available = models.BooleanField(default=True, verbose_name="Có sẵn")
    is_featured = models.BooleanField(default=False, verbose_name="Sản phẩm nổi bật")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='', blank=True, verbose_name="Trạng thái")
    discount_percentage = models.PositiveIntegerField(default=0, verbose_name="Phần trăm giảm giá")
    original_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Giá gốc")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_size_display()})"

    @property
    def formatted_price(self):
        return f"{float(self.price):,.0f} VNĐ"
    
    @property
    def formatted_original_price(self):
        if self.original_price:
            return f"{float(self.original_price):,.0f} VNĐ"
        return None
    
    @property
    def discount_amount(self):
        if self.original_price and int(self.discount_percentage) > 0:
            return float(self.original_price) - float(self.price)
        return 0
    
    @property
    def formatted_discount_amount(self):
        if self.discount_amount > 0:
            return f"{self.discount_amount:,.0f} VNĐ"
        return None
    
    @property
    def discount_display(self):
        if self.status == 'sale' and int(self.discount_percentage) > 0:
            return f"-{self.discount_percentage}%"
        return None


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    subtitle = models.CharField(max_length=300, verbose_name="Phụ đề")
    image = models.ImageField(upload_to='banners/', verbose_name="Hình ảnh")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title