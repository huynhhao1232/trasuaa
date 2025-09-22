from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from products.models import Banner
from products.serializers import BannerSerializer
import json


@login_required(login_url='/admin-login/')
def admin_banners(request):
    """Trang quản lý banner"""
    if not request.user.is_staff:
        return redirect('admin-login')
    
    return render(request, 'frontend/admin/banners.html')


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='/admin-login/')
def create_banner(request):
    """API tạo banner mới"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        # Handle both JSON and FormData
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
            # Convert checkbox values from FormData
            data['is_active'] = data.get('is_active') == 'on'

        # Debug logging
        print("Received banner data:", data)
        print("Content type:", request.content_type)

        # Validate required fields
        required_fields = ['title', 'subtitle']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Field {field} is required'}, status=400)

        # Create banner
        banner = Banner.objects.create(
            title=data['title'],
            subtitle=data['subtitle'],
            is_active=data.get('is_active', True),
            order=int(data.get('order', 0)) if data.get('order') else 0
        )

        # Handle image upload if provided
        if 'image' in request.FILES:
            banner.image = request.FILES['image']
            banner.save()

        serializer = BannerSerializer(banner)
        return JsonResponse(serializer.data, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='/admin-login/')
def update_banner(request, banner_id):
    """API cập nhật banner"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        banner = Banner.objects.get(id=banner_id)

        # Handle both JSON and FormData
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
            # Convert checkbox values from FormData
            data['is_active'] = data.get('is_active') == 'on'

        # Debug logging
        print("Update banner data:", data)
        print("Content type:", request.content_type)

        # Update fields
        if 'title' in data:
            banner.title = data['title']
        if 'subtitle' in data:
            banner.subtitle = data['subtitle']
        if 'is_active' in data:
            banner.is_active = data['is_active']
        if 'order' in data:
            banner.order = int(data['order']) if data['order'] else 0

        banner.save()

        # Handle image upload if provided
        if 'image' in request.FILES:
            banner.image = request.FILES['image']
            banner.save()

        serializer = BannerSerializer(banner)
        return JsonResponse(serializer.data)

    except Banner.DoesNotExist:
        return JsonResponse({'error': 'Banner not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
@login_required(login_url='/admin-login/')
def delete_banner(request, banner_id):
    """API xóa banner"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        banner = Banner.objects.get(id=banner_id)
        banner.delete()
        return JsonResponse({'message': 'Banner deleted successfully'})

    except Banner.DoesNotExist:
        return JsonResponse({'error': 'Banner not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
