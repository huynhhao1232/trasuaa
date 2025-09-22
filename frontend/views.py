from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from products.models import Product, Category, Banner
from products.serializers import ProductSerializer, BannerSerializer
from .banner_views import admin_banners, create_banner, update_banner, delete_banner
import json


def home(request):
    """Trang chủ - hiển thị sản phẩm và banner"""
    return render(request, 'frontend/home.html')


def cart(request):
    """Trang giỏ hàng"""
    return render(request, 'frontend/cart.html')


def checkout(request):
    """Trang thanh toán"""
    return render(request, 'frontend/checkout.html')


def order_success(request):
    """Trang thành công sau khi đặt hàng"""
    return render(request, 'frontend/order_success.html')


def track_order(request):
    """Trang tra cứu đơn hàng"""
    order = None
    order_id = request.GET.get('order_id')
    
    if order_id:
        try:
            from orders.models import Order
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            order = None
    
    return render(request, 'frontend/track_order.html', {
        'order': order,
        'order_id': order_id
    })


def admin_login(request):
    """Trang đăng nhập admin"""
    if request.user.is_authenticated:
        return redirect('admin-panel')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin-panel')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    
    return render(request, 'frontend/admin/login.html')


def admin_logout(request):
    """Đăng xuất admin"""
    logout(request)
    return redirect('admin-login')


@login_required(login_url='/admin-login/')
def admin_panel(request):
    """Trang admin chính"""
    if not request.user.is_staff:
        return redirect('admin-login')
    return render(request, 'frontend/admin/admin_panel.html')


@login_required(login_url='/admin-login/')
def admin_products(request):
    """Trang quản lý sản phẩm"""
    if not request.user.is_staff:
        return redirect('admin-login')
    return render(request, 'frontend/admin/products.html')


@login_required(login_url='/admin-login/')
def admin_categories(request):
    """Trang quản lý danh mục"""
    if not request.user.is_staff:
        return redirect('admin-login')
    return render(request, 'frontend/admin/categories.html')


@login_required(login_url='/admin-login/')
def admin_orders(request):
    """Trang quản lý đơn hàng"""
    if not request.user.is_staff:
        return redirect('admin-login')
    return render(request, 'frontend/admin/orders.html')


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='/admin-login/')
def create_product(request):
    """API tạo sản phẩm mới"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        # Handle both JSON and FormData
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
            # Convert checkbox values from FormData - checkboxes send 'on' if checked, nothing if not checked
            data['is_available'] = data.get('is_available') == 'on'
            data['is_featured'] = data.get('is_featured') == 'on'
        
        # Debug logging
        print("Received data:", data)
        print("Content type:", request.content_type)
        
        # Validate required fields
        required_fields = ['name', 'description', 'category_id', 'price', 'size']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Field {field} is required'}, status=400)
        
        # Get category
        try:
            category = Category.objects.get(id=data['category_id'])
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=400)
        
        # Create product
        product = Product.objects.create(
            name=data['name'],
            description=data['description'],
            category=category,
            price=data['price'],
            size=data['size'],
            is_available=data.get('is_available', True),
            is_featured=data.get('is_featured', False),
            status=data.get('status', ''),
            discount_percentage=int(data.get('discount_percentage', 0)) if data.get('discount_percentage') else 0,
            original_price=float(data.get('original_price')) if data.get('original_price') else None
        )
        
        # Handle image upload if provided
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save()
        
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, status=201)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["PUT", "POST"])
@login_required(login_url='/admin-login/')
def update_product(request, product_id):
    """API cập nhật sản phẩm"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        product = Product.objects.get(id=product_id)
        
        # Handle both JSON and FormData
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
            # Convert checkbox values from FormData - checkboxes send 'on' if checked, nothing if not checked
            data['is_available'] = data.get('is_available') == 'on'
            data['is_featured'] = data.get('is_featured') == 'on'
        
        # Debug logging
        print("Update data:", data)
        print("Content type:", request.content_type)
        
        # Update fields
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'category_id' in data:
            try:
                category = Category.objects.get(id=data['category_id'])
                product.category = category
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=400)
        if 'price' in data:
            product.price = data['price']
        if 'size' in data:
            product.size = data['size']
        if 'is_available' in data:
            product.is_available = data['is_available']
        if 'is_featured' in data:
            product.is_featured = data['is_featured']
        if 'status' in data:
            product.status = data['status']
        if 'discount_percentage' in data:
            product.discount_percentage = int(data['discount_percentage']) if data['discount_percentage'] else 0
        if 'original_price' in data:
            product.original_price = float(data['original_price']) if data['original_price'] else None
        
        product.save()
        
        # Handle image upload if provided
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save()
        
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
        
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
@login_required(login_url='/admin-login/')
def delete_product(request, product_id):
    """API xóa sản phẩm"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})
        
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)