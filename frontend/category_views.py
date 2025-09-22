import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from products.models import Category
from products.serializers import CategorySerializer


@login_required(login_url='/admin-login/')
def admin_categories(request):
    """Trang quản lý danh mục"""
    if not request.user.is_staff:
        return render(request, 'frontend/admin/unauthorized.html', status=401)
    return render(request, 'frontend/admin/categories.html')


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='/admin-login/')
def create_category(request):
    """API tạo danh mục mới"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        # Validate required fields
        if not data.get('name'):
            return JsonResponse({'error': 'Tên danh mục là bắt buộc'}, status=400)
        
        # Convert checkbox value to boolean
        is_active = data.get('is_active', True)
        if isinstance(is_active, str):
            is_active = is_active == 'on'
        
        category = Category.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            is_active=is_active
        )
        
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data, status=201)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='/admin-login/')
def update_category(request, category_id):
    """API cập nhật danh mục"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        category = Category.objects.get(id=category_id)
        
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        # Update fields
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        if 'is_active' in data:
            is_active = data['is_active']
            if isinstance(is_active, str):
                is_active = is_active == 'on'
            category.is_active = is_active
        
        category.save()
        
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data)
        
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Danh mục không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
@login_required(login_url='/admin-login/')
def delete_category(request, category_id):
    """API xóa danh mục"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        category = Category.objects.get(id=category_id)
        
        # Check if category has products
        if category.product_set.exists():
            return JsonResponse({'error': 'Không thể xóa danh mục có sản phẩm'}, status=400)
        
        category.delete()
        return JsonResponse({'message': 'Danh mục đã được xóa thành công'})
        
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Danh mục không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
