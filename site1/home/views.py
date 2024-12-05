from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from .models import Order
from datetime import datetime

from django.shortcuts import render, redirect
from datetime import datetime

def home(request):
    if request.method == 'POST':
        # Lấy thông tin từ form
        employee = request.POST.get('employee')
        customer = request.POST.get('customer')
        complete_expect = request.POST.get('complete_expect') or None
        created_date = request.POST.get('created-date')
        color = request.POST.get('color', '#0D6EFD')
        note_size = request.POST.getlist('note_size[]')
        note = request.POST.get('note')
        code = request.POST.get('code')
        image = request.FILES.get('image')

        # Tạo dictionary để lưu thông tin kích cỡ và số lượng
        size_dict = {}
        sizes = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL']
        for i, size in enumerate(sizes):
            quantity = note_size[i] if i < len(note_size) else '0'
            size_dict[size] = quantity

        # Xử lý created_date
        if not created_date:
            created_date = datetime.now().date()  # Sử dụng ngày hiện tại nếu không có input
        else:
            try:
                created_date = datetime.strptime(created_date, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, 'Ngày tạo đơn không hợp lệ')
                return redirect('home')

        # Chuyển thành chuỗi với định dạng "XS: 12, S: 10"
        note_size_str = ', '.join([f"{size}: {size_dict[size]}" for size in sizes])
        total_quantity = sum(int(size) for size in note_size if size.isdigit())

        try:
            # Tạo đơn hàng mới
            order = Order.objects.create(
                employee=employee,
                customer=customer,
                complete_expect=complete_expect,
                color=color,
                quantity=total_quantity,
                note_size=note_size_str,
                note=note,
                created=created_date,
                code=code,
                image=image
            )

            # Thêm thông báo thành công
            messages.success(request, 'Đơn hàng đã được tạo thành công!')

            # Gọi hàm tạo PDF và trả về PDF cho người dùng
            return generate_order_pdf(request, order.id)
        except Exception as e:
            messages.error(request, f'Lỗi khi tạo đơn hàng: {str(e)}')
            return redirect('home')

    return render(request, 'home/home.html', {
        'sizes': ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL']
    })

from django.conf import settings
import os

def fetch_resources(uri, rel):
    """
    Hàm callback để xử lý đường dẫn tới resources (ảnh)
    """
    if uri.startswith("/media/"):
        return os.path.join(settings.MEDIA_ROOT, uri.replace("/media/", ""))
    return uri

import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse
import os

def generate_order_pdf(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        
        # Xử lý note_size thành dictionary
        size_dict = {}
        if order.note_size:
            size_pairs = order.note_size.split(', ')
            for pair in size_pairs:
                if ': ' in pair:
                    size, value = pair.split(': ')
                    size_dict[size] = value

        # Sử dụng đường dẫn tuyệt đối cho logo
        logo_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'images', 'log.png'))
        logo_path1 = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'images', 'a.png'))

        # Thêm logging
        print(f"Logo path: {logo_path}")
        print(f"Logo exists: {os.path.exists(logo_path)}")

        context = {
            'order': order,
            'size_dict': size_dict,
            'logo_path': logo_path,
            'logo_path1': logo_path1,
        }

        # Render template thành HTML
        html = render_to_string('home/pdf_order.html', context)

        # Cấu hình wkhtmltopdf
        options = {
            'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': True,
            'disable-smart-shrinking': True,
            'quiet': None
        }

        try:
            config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
            pdf = pdfkit.from_string(html, False, options=options, configuration=config)
            print("PDF generated successfully")
            
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=Order_{order.code}.pdf'
            return response
            
        except Exception as e:
            print(f"PDF generation error: {str(e)}")
            raise
        
    except Exception as e:
        print(f"General error: {str(e)}")
        messages.error(request, f"Error generating PDF: {str(e)}")
        return redirect('home')