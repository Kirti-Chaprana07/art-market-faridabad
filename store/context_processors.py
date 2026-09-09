from .models import Category

def store_info(request):
    categories = Category.objects.all()
    return {
        'STORE_NAME': 'Art Market Faridabad',
        'STORE_TAGLINE': 'Premium Artificial Plants, Handcrafted Antique Decor & Luxury Canvas Art',
        'STORE_PHONE': '+91 98990 97676',
        'STORE_WHATSAPP': '919899097676',
        'STORE_EMAIL': 'artmarketfaridabad@gmail.com',
        'STORE_INSTAGRAM': 'https://www.instagram.com/artmarketfaridabad',
        'STORE_ADDRESS': 'Shop No. 19, Master Road, Sector 87-88 (Near Barfiwala Shop / Maharana Pratap Chowk), Faridabad - 121002, Haryana',
        'STORE_HOURS': 'Mon - Sun: 10:30 AM ? 9:00 PM (Open 7 Days)',
        'STORE_CATEGORIES': categories,
    }
