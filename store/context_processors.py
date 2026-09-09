from .models import Category

def store_info(request):
    categories = Category.objects.all()
    return {
        'STORE_NAME': 'Art Market Faridabad',
        'STORE_TAGLINE': 'Artificial Plants, Green Wall Transformations, Designer Planters & Antique Decor',
        'STORE_PHONE': '+91 98990 97676',
        'STORE_WHATSAPP': '919899097676',
        'STORE_EMAIL': 'artmarketfaridabad@gmail.com',
        'STORE_INSTAGRAM': 'https://www.instagram.com/artmarketfaridabad',
        'STORE_ADDRESS': 'G. Floor, Maharana Pratap Chowk, Plot No 19, Master Rd, near Chandi Wala Bagh, Sector 88, Faridabad, Haryana 121002',
        'STORE_SHORT_ADDRESS': 'Plot No 19, Master Rd, Maharana Pratap Chowk, Sector 88, Faridabad',
        'STORE_HOURS': 'Mon - Sun: 10:30 AM - 9:00 PM (Open 7 Days)',
        'STORE_MAP_URL': 'https://www.google.com/maps/place/Art+Market+Faridabad/',
        'STORE_CATEGORIES': categories,
    }
