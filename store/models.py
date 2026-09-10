from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    icon = models.CharField(max_length=50, default="fa-gem")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    ROOM_CHOICES = [
        ('all', 'All Spaces'),
        ('living_room', 'Living Room & Foyer'),
        ('balcony', 'Balcony & Garden'),
        ('mandir', 'Mandir & Pooja Room'),
        ('office', 'Office & Workspace'),
        ('bedroom', 'Bedroom & Lounge'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=50, unique=True, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Discounted / Selling Rate (?)")
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    material = models.CharField(max_length=150, blank=True, default="Real-Touch Polymer / Brass / Ceramic")
    dimensions = models.CharField(max_length=100, blank=True, default="Standard")
    weight = models.CharField(max_length=50, blank=True, default="1.5 kg")
    room_type = models.CharField(max_length=50, choices=ROOM_CHOICES, default='living_room')
    stock = models.PositiveIntegerField(default=10)
    
    # Image support: both direct photo upload and external URL
    image_file = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True)
    
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    reviews_count = models.PositiveIntegerField(default=12)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if not self.sku:
            import random
            self.sku = f"AMF-{random.randint(100, 999)}"
        if not self.short_description and self.name:
            self.short_description = f"Premium {self.name} available at Art Market Faridabad."
        if not self.description and self.name:
            self.description = f"High quality {self.name}. Hand-crafted and inspected before delivery from Sector 88, Faridabad."
        if not self.original_price or self.original_price <= self.price:
            self.original_price = float(self.price) * 1.25
        super().save(*args, **kwargs)

    @property
    def get_image(self):
        if self.image_file:
            return self.image_file.url
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1545241047-6083a3684587?auto=format&fit=crop&w=800&q=80"

    @property
    def discount_percent(self):
        if self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    def __str__(self):
        return f"{self.name} (?{self.price})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Received', 'New Order (Pending)'),
        ('Processing', 'Processing & Packing'),
        ('Dispatched', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery (COD)'),
        ('UPI', 'UPI / QR Code Transfer'),
        ('ONLINE', 'Online Card / NetBanking'),
    ]

    order_id = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100, default="Faridabad")
    state = models.CharField(max_length=100, default="Haryana")
    pincode = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='COD')
    order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Received')
    items_json = models.TextField(help_text="JSON serialized list of ordered items")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name} (?{self.total_amount})"

class Inquiry(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    inquiry_type = models.CharField(max_length=100, default="Product Inquiry")
    product_name = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} ({self.inquiry_type})"

class ShowroomBooking(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    visit_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    guests_count = models.PositiveIntegerField(default=2)
    interest_area = models.CharField(max_length=150, default="Artificial Plants & Decor")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking: {self.name} on {self.visit_date} ({self.time_slot})"

class Review(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=100, default="Faridabad")
    rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    product_name = models.CharField(max_length=200, blank=True, default="Artificial Plants & Decor")
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating}★) - {self.title}"


class PhoneOTP(models.Model):
    phone = models.CharField(max_length=20, db_index=True)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Phone OTP"
        verbose_name_plural = "Phone OTPs"

    def is_valid(self):
        from django.utils import timezone
        from datetime import timedelta
        # Valid for 10 minutes and not yet used
        return not self.is_used and (timezone.now() - self.created_at) < timedelta(minutes=10)

    def __str__(self):
        return f"OTP {self.otp} for {self.phone} ({'Valid' if self.is_valid() else 'Expired/Used'})"
