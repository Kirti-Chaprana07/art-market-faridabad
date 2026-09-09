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
    sku = models.CharField(max_length=50, unique=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Discounted / Selling Price")
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    material = models.CharField(max_length=150, help_text="e.g. Solid Brass, Distressed Teak Wood, Real-Touch Silk")
    dimensions = models.CharField(max_length=100, help_text="e.g. 18in H x 12in W")
    weight = models.CharField(max_length=50, blank=True, help_text="e.g. 3.2 kg")
    room_type = models.CharField(max_length=50, choices=ROOM_CHOICES, default='living_room')
    stock = models.PositiveIntegerField(default=10)
    image_url = models.URLField(max_length=500)
    image_url_2 = models.URLField(max_length=500, blank=True)
    image_url_3 = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    reviews_count = models.PositiveIntegerField(default=18)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discount_percent(self):
        if self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    def __str__(self):
        return f"{self.name} (?{self.price})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Received', 'Order Received'),
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

    def __str__(self):
        return f"Inquiry from {self.name} ({self.inquiry_type})"

class ShowroomBooking(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    visit_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    guests_count = models.PositiveIntegerField(default=2)
    interest_area = models.CharField(max_length=150, default="Antiques & Artificial Plants")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.name} on {self.visit_date} ({self.time_slot})"

class Review(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=100, default="Faridabad")
    rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    product_name = models.CharField(max_length=200, blank=True, default="Antique Decor & Plants")
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating}?) - {self.title}"
