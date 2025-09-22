#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trasua_project.settings')
django.setup()

from products.models import Category, Product, Banner
from django.core.files.base import ContentFile
from PIL import Image
import io

def create_sample_data():
    print("Creating sample data...")
    
    # Create categories
    categories_data = [
        {
            'name': 'Trà sữa truyền thống',
            'description': 'Các loại trà sữa cổ điển với hương vị truyền thống'
        },
        {
            'name': 'Trà sữa hiện đại',
            'description': 'Trà sữa với các topping và hương vị mới lạ'
        },
        {
            'name': 'Trà trái cây',
            'description': 'Trà kết hợp với các loại trái cây tươi ngon'
        },
        {
            'name': 'Smoothie',
            'description': 'Smoothie trái cây tươi, bổ dưỡng'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories.append(category)
        print(f"Created category: {category.name}")
    
    # Create sample products
    products_data = [
        {
            'name': 'Trà sữa trân châu đen',
            'description': 'Trà sữa thơm ngon với trân châu đen dai giòn, hương vị truyền thống',
            'category': categories[0],
            'price': 25000,
            'size': 'M',
            'is_featured': True
        },
        {
            'name': 'Trà sữa matcha',
            'description': 'Trà sữa matcha Nhật Bản với vị đắng nhẹ, thơm ngon',
            'category': categories[0],
            'price': 30000,
            'size': 'M',
            'is_featured': True
        },
        {
            'name': 'Trà sữa thái',
            'description': 'Trà sữa thái với vị chua ngọt đặc trưng',
            'category': categories[0],
            'price': 28000,
            'size': 'M',
            'is_featured': False
        },
        {
            'name': 'Trà sữa chocolate',
            'description': 'Trà sữa chocolate đậm đà, ngọt ngào',
            'category': categories[1],
            'price': 32000,
            'size': 'M',
            'is_featured': True
        },
        {
            'name': 'Trà sữa kem cheese',
            'description': 'Trà sữa với lớp kem cheese béo ngậy',
            'category': categories[1],
            'price': 35000,
            'size': 'M',
            'is_featured': True
        },
        {
            'name': 'Trà đào cam sả',
            'description': 'Trà đào tươi với cam sả, giải nhiệt mùa hè',
            'category': categories[2],
            'price': 25000,
            'size': 'M',
            'is_featured': False
        },
        {
            'name': 'Trà chanh dây',
            'description': 'Trà chanh dây chua ngọt, tươi mát',
            'category': categories[2],
            'price': 22000,
            'size': 'M',
            'is_featured': False
        },
        {
            'name': 'Smoothie dâu tây',
            'description': 'Smoothie dâu tây tươi, bổ dưỡng',
            'category': categories[3],
            'price': 30000,
            'size': 'M',
            'is_featured': False
        },
        {
            'name': 'Smoothie xoài',
            'description': 'Smoothie xoài chín, ngọt thơm',
            'category': categories[3],
            'price': 28000,
            'size': 'M',
            'is_featured': False
        }
    ]
    
    # Create a simple placeholder image
    def create_placeholder_image():
        img = Image.new('RGB', (300, 300), color='#8B4513')
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        return ContentFile(img_io.getvalue(), 'placeholder.jpg')
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'description': product_data['description'],
                'category': product_data['category'],
                'price': product_data['price'],
                'size': product_data['size'],
                'is_featured': product_data['is_featured'],
                'image': create_placeholder_image()
            }
        )
        print(f"Created product: {product.name}")
    
    # Create banners
    banners_data = [
        {
            'title': 'Khuyến mãi đặc biệt',
            'subtitle': 'Giảm 20% cho đơn hàng đầu tiên',
            'order': 1
        },
        {
            'title': 'Trà sữa mới',
            'subtitle': 'Khám phá hương vị mới lạ',
            'order': 2
        }
    ]
    
    for banner_data in banners_data:
        banner, created = Banner.objects.get_or_create(
            title=banner_data['title'],
            defaults={
                'subtitle': banner_data['subtitle'],
                'order': banner_data['order'],
                'image': create_placeholder_image()
            }
        )
        print(f"Created banner: {banner.title}")
    
    print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()
