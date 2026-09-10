from django.urls import path
from . import views

urlpatterns = [
    # Storefront
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<str:order_id>/', views.order_success, name='order_success'),
    path('visit-showroom/', views.visit_showroom, name='visit_showroom'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # User Authentication & Customer Account
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('account/', views.user_account, name='account'),
    path('api/send-otp/', views.api_send_otp, name='api_send_otp'),
    path('api/verify-otp/', views.api_verify_otp, name='api_verify_otp'),
    
    # Owner Management Portal
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/login/', views.owner_login, name='owner_login'),
    path('owner/logout/', views.owner_logout, name='owner_logout'),
    path('owner/product/add/', views.owner_add_product, name='owner_add_product'),
    path('owner/product/<int:product_id>/delete/', views.owner_delete_product, name='owner_delete_product'),
    path('owner/order/<str:order_id>/status/', views.owner_update_order, name='owner_update_order'),
    
    # AJAX APIs
    path('api/products/', views.api_products, name='api_products'),
]
