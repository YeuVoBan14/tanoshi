from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from .models import Order

def home(request):
    if request.method == 'POST':
        # Lấy thông tin từ form
        employee = request.POST.get('employee')
        customer = request.POST.get('customer')
        complete_expect = request.POST.get('complete_expect') or None
        color = request.POST.get('color', '#0D6EFD')
        quantity = request.POST.get('quantity') or None
        size = request.POST.get('size')
        note = request.POST.get('note')
        image = request.FILES.get('image')

        # Tạo đơn hàng mới
        order = Order.objects.create(
            employee=employee,
            customer=customer,
            complete_expect=complete_expect,
            color=color,
            quantity=quantity,
            size=size,
            note=note,
            image=image
        )

        # Thêm thông báo thành công
        messages.success(request, 'Đơn hàng đã được tạo thành công!')

        # Gọi hàm tạo PDF và trả về PDF cho người dùng
        return generate_order_pdf(request, order.id)

    return render(request, 'home/home.html')


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