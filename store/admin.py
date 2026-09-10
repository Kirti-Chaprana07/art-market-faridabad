from django.contrib import admin
from .models import Category, Product, Order, Inquiry, ShowroomBooking, Review, PhoneOTP

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'original_price', 'stock', 'room_type', 'is_featured', 'is_bestseller', 'is_new_arrival')
    list_filter = ('category', 'room_type', 'is_featured', 'is_bestseller', 'is_new_arrival')
    search_fields = ('name', 'sku', 'material', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_featured', 'is_bestseller')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'phone', 'city', 'total_amount', 'payment_method', 'order_status', 'created_at')
    list_filter = ('order_status', 'payment_method', 'city', 'created_at')
    search_fields = ('order_id', 'customer_name', 'phone', 'email')
    list_editable = ('order_status',)

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'inquiry_type', 'product_name', 'created_at')
    list_filter = ('inquiry_type', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')

@admin.register(ShowroomBooking)
class ShowroomBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'visit_date', 'time_slot', 'guests_count', 'interest_area', 'created_at')
    list_filter = ('visit_date', 'time_slot', 'interest_area')
    search_fields = ('name', 'phone', 'email')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'title', 'city', 'product_name', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'city')
    search_fields = ('name', 'title', 'comment')

@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp', 'name', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('phone', 'otp', 'name')
    readonly_fields = ('created_at',)
