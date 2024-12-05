
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('orders/', views.order_list, name='order_list'),
path('generate-pdf/<int:order_id>/', views.generate_order_pdf1, name='generate_pdf'),



]