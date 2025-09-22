from django.contrib import admin
from .models import Category, Product, Banner


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'size', 'is_available', 'is_featured', 'created_at']
    list_filter = ['category', 'size', 'is_available', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'is_featured']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Giá và kích thước', {
            'fields': ('price', 'size')
        }),
        ('Trạng thái', {
            'fields': ('is_available', 'is_featured')
        }),
    )


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    list_editable = ['is_active', 'order']
    ordering = ['order', '-created_at']