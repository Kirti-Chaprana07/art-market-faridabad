from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<str:order_id>/', views.order_success, name='order_success'),
    path('visit-showroom/', views.visit_showroom, name='visit_showroom'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # AJAX APIs
    path('api/products/', views.api_products, name='api_products'),
    path('api/inquiry/', views.submit_inquiry_api, name='submit_inquiry_api'),
    path('api/review/', views.submit_review_api, name='submit_review_api'),
]
