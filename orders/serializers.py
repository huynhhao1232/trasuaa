from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=0, read_only=True)
    formatted_price = serializers.CharField(read_only=True)
    formatted_total = serializers.CharField(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_id', 'quantity', 'price',
            'total_price', 'formatted_price', 'formatted_total'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    formatted_total = serializers.CharField(read_only=True)
    status_display = serializers.CharField(read_only=True)
    payment_method_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_phone', 'customer_address',
            'customer_email', 'status', 'status_display', 'payment_method',
            'payment_method_display', 'payment_status', 'total_amount',
            'formatted_total', 'notes', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100)
    customer_phone = serializers.CharField(max_length=15)
    customer_address = serializers.CharField()
    customer_email = serializers.EmailField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, default='cod')
    notes = serializers.CharField(required=False, allow_blank=True)
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Đơn hàng phải có ít nhất một sản phẩm.")
        return value
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate total amount first
        total_amount = 0
        for item_data in items_data:
            from products.models import Product
            product = Product.objects.get(id=item_data['product_id'])
            quantity = item_data['quantity']
            price = product.price
            total_amount += quantity * price
        
        # Create order with total_amount
        order = Order.objects.create(
            total_amount=total_amount,
            **validated_data
        )
        
        # Create order items
        for item_data in items_data:
            from products.models import Product
            product = Product.objects.get(id=item_data['product_id'])
            quantity = item_data['quantity']
            price = product.price
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
        
        return order
