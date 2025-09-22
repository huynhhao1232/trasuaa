from rest_framework import serializers
from .models import Category, Product, Banner


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'product_count', 'created_at']
    
    def get_product_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    formatted_price = serializers.CharField(read_only=True)
    get_status_display = serializers.CharField(read_only=True)
    formatted_original_price = serializers.CharField(read_only=True)
    discount_amount = serializers.ReadOnlyField()
    formatted_discount_amount = serializers.CharField(read_only=True)
    discount_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'price', 'formatted_price', 'original_price', 'formatted_original_price',
            'discount_percentage', 'discount_amount', 'formatted_discount_amount',
            'discount_display', 'size', 'image', 'is_available',
            'is_featured', 'status', 'get_status_display', 'created_at'
        ]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'subtitle', 'image', 'is_active', 'order']
