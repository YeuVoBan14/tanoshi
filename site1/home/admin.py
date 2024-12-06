from django.contrib import admin
from .models import Order
# Register your models here.
from .views import generate_order_pdf
from django.utils.html import format_html
from reportlab.pdfgen import canvas
from io import BytesIO
from django.urls import path
from django.shortcuts import render
from django.utils.html import format_html
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'employee', 'customer', 'complete_expect', 'quantity', 'export_pdf_link')
    list_filter = ('employee', 'customer', 'complete_expect')
    search_fields = ('employee', 'customer')

    def export_pdf_link(self, obj):
        # Tạo liên kết để xuất PDF
        # Sử dụng reverse để tạo URL đúng cho hàm generate_order_pdf
        return format_html('<a href="{}">Export PDF</a>', 
                           f'generate-pdf/{obj.id}')
    export_pdf_link.short_description = 'Export PDF'

    def get_urls(self):
        # Thêm URL cho hành động xuất PDF của từng đơn hàng
        urls = super().get_urls()
        custom_urls = [
            path('generate-pdf/<int:order_id>/', self.admin_site.admin_view(generate_order_pdf), name='generate-pdf'),
        ]
        return custom_urls + urls

admin.site.register(Order, OrderItemAdmin)