# Trà Sữa Online - Django Web Application

## 📝 Mô tả
Ứng dụng web bán trà sữa trực tuyến được xây dựng bằng Django với giao diện thân thiện và tính năng quản lý đầy đủ.

## ✨ Tính năng chính

### 👥 Trang người dùng
- **Trang chủ**: Hiển thị sản phẩm và banner
- **Giỏ hàng**: Quản lý sản phẩm đã chọn
- **Thanh toán**: Đặt hàng với thanh toán khi nhận hàng (COD)
- **Tra cứu đơn hàng**: Tìm kiếm đơn hàng bằng mã đơn hàng
- **Responsive**: Tương thích mọi thiết bị

### 🔧 Trang quản trị
- **Đăng nhập admin**: Bảo mật với authentication
- **Quản lý sản phẩm**: Thêm, sửa, xóa sản phẩm
- **Quản lý đơn hàng**: Xem và cập nhật trạng thái đơn hàng
- **Quản lý banner**: Tùy chỉnh banner trang chủ
- **Thống kê**: Dashboard với số liệu tổng quan

### 🛍️ Tính năng sản phẩm
- **Trạng thái sản phẩm**: Hot, Giảm giá, Hết hàng
- **Giảm giá**: Hiển thị phần trăm và số tiền giảm
- **Kích thước**: Nhỏ (S), Vừa (M), Lớn (L)
- **Hình ảnh**: Upload và preview hình ảnh sản phẩm
- **Danh mục**: Phân loại sản phẩm theo category

## 🚀 Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.8+
- Django 5.2+
- Pillow (xử lý hình ảnh)

### Cài đặt
```bash
# Clone repository
git clone <repository-url>
cd webtrasua

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy migrations
python manage.py migrate

# Tạo superuser
python manage.py createsuperuser

# Chạy server
python manage.py runserver
```

### Truy cập ứng dụng
- **Trang chủ**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin-login/

## 📁 Cấu trúc dự án

```
webtrasua/
├── trasua_project/          # Django project settings
├── products/                # App quản lý sản phẩm
├── orders/                  # App quản lý đơn hàng
├── frontend/                # App giao diện người dùng
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── media/                   # Uploaded files
└── requirements.txt         # Dependencies
```

## 🛠️ Công nghệ sử dụng

### Backend
- **Django 5.2**: Web framework
- **Django REST Framework**: API endpoints
- **SQLite**: Database (development)
- **Pillow**: Image processing

### Frontend
- **Bootstrap 5**: CSS framework
- **Font Awesome**: Icons
- **Vanilla JavaScript**: Interactive features
- **Responsive Design**: Mobile-friendly

## 📱 Tính năng nổi bật

### 🎨 Giao diện đẹp
- Design hiện đại với Bootstrap 5
- Responsive trên mọi thiết bị
- Animation và hiệu ứng mượt mà
- Color scheme thân thiện

### 🔒 Bảo mật
- CSRF protection
- User authentication
- Admin authorization
- Input validation

### ⚡ Performance
- Image optimization
- Cache busting
- Efficient database queries
- Lazy loading

## 📊 API Endpoints

### Products
- `GET /api/products/products/` - Lấy danh sách sản phẩm
- `GET /api/products/categories/` - Lấy danh mục
- `GET /api/products/banners/` - Lấy banner

### Orders
- `GET /api/orders/` - Lấy danh sách đơn hàng
- `POST /api/orders/create/` - Tạo đơn hàng mới
- `PATCH /api/orders/{id}/status/` - Cập nhật trạng thái đơn hàng

### Admin
- `POST /api/admin/products/` - Tạo sản phẩm
- `POST /api/admin/products/{id}/` - Cập nhật sản phẩm
- `DELETE /api/admin/products/{id}/delete/` - Xóa sản phẩm

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Liên hệ

- **Tác giả**: [Tên của bạn]
- **Email**: [email@example.com]
- **GitHub**: [@username](https://github.com/username)

---

⭐ **Nếu dự án hữu ích, hãy cho một star!** ⭐