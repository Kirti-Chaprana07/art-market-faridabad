from .models import Category

def store_info(request):
    categories = Category.objects.all()
    return {
        'STORE_NAME': 'Art Market Faridabad',
        'STORE_TAGLINE': 'Handcrafted Antique Treasures & Lush Artificial Botanicals',
        'STORE_PHONE': '+91 98765 43210',
        'STORE_WHATSAPP': '919876543210',
        'STORE_EMAIL': 'hello@artmarketfaridabad.com',
        'STORE_ADDRESS': 'Art Market Showroom, Sector 15 / Main Mathura Road, Faridabad, Haryana - 121007',
        'STORE_HOURS': 'Mon - Sun: 10:00 AM ? 9:00 PM (Open 7 Days)',
        'STORE_CATEGORIES': categories,
    }
