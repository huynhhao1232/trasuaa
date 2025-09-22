from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price', 'formatted_price', 'formatted_total']
    fields = ['product', 'quantity', 'price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'status', 'payment_method', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status', 'created_at']
    search_fields = ['customer_name', 'customer_phone', 'customer_email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'formatted_total']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Thông tin khách hàng', {
            'fields': ('customer_name', 'customer_phone', 'customer_address', 'customer_email')
        }),
        ('Thông tin đơn hàng', {
            'fields': ('status', 'payment_method', 'payment_status', 'total_amount', 'notes')
        }),
        ('Thông tin xử lý', {
            'fields': ('processed_by', 'created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.processed_by and change:
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']
    list_filter = ['order__status', 'product__category']
    search_fields = ['order__customer_name', 'product__name']
    readonly_fields = ['total_price', 'formatted_price', 'formatted_total']