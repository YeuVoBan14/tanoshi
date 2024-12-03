from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from .models import Order
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
        if created_date:
            created_date = datetime.strptime(created_date, "%Y-%m-%d").date()
        # Chuyển thành chuỗi với định dạng "XS: 12, S: 10"
        note_size_str = ', '.join([f"{size}: {size_dict[size]}" for size in sizes])
        total_quantity = sum(int(size) for size in note_size if size.isdigit())
        # Tạo đơn hàng mới
        order = Order.objects.create(
            employee=employee,
            customer=customer,
            complete_expect=complete_expect,
            color=color,
            quantity=total_quantity,
            note_size=note_size_str,  # Lưu note_size theo định dạng mới
            note=note,
            created=created_date,
            code=code,
            image=image
        )

        # Thêm thông báo thành công
        messages.success(request, 'Đơn hàng đã được tạo thành công!')

        # Gọi hàm tạo PDF và trả về PDF cho người dùng
        return generate_order_pdf(request, order.id)

    return render(request, 'home/home.html', {
        'sizes': ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL']
    })


def generate_order_pdf(request, order_id):
    try:
        # Lấy đơn hàng từ ID
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse('Đơn hàng không tồn tại', status=404)

    # Chuẩn bị context với thông tin đơn hàng
    context = {
        'order': order,
    }

    # Render HTML cho PDF
    html = render_to_string('home/pdf_order.html', context)

    # Tạo đối tượng PDF từ HTML
    pdf = BytesIO()
    pisa_status = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)

    if pisa_status.err:
        return HttpResponse('Có lỗi khi tạo PDF', status=500)

    # Trả về PDF cho người dùng
    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    content = f"Order_{order.code}.pdf"
    response['Content-Disposition'] = f'attachment; filename={content}'
    return response