from django.contrib import admin
from .models import Order
# Register your models here.

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('code','employee', 'customer', 'complete_expect', 'quantity',)
    list_filter = ('employee','customer','complete_expect')
    search_fields = ('employee','customer')
admin.site.register(Order, OrderItemAdmin)