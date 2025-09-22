from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, Banner
from .serializers import CategorySerializer, ProductSerializer, BannerSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'size', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer


class FeaturedProductsView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True, is_featured=True)
    serializer_class = ProductSerializer
    ordering = ['-created_at']


class BannerListView(generics.ListAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    ordering = ['order', '-created_at']


@api_view(['GET'])
def product_stats(request):
    """API endpoint để lấy thống kê sản phẩm"""
    total_products = Product.objects.filter(is_available=True).count()
    featured_products = Product.objects.filter(is_available=True, is_featured=True).count()
    categories = Category.objects.count()
    
    return Response({
        'total_products': total_products,
        'featured_products': featured_products,
        'categories': categories
    })