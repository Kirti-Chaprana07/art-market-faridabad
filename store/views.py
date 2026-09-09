import json
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Order, Inquiry, ShowroomBooking, Review

def home(request):
    featured_antiques = Product.objects.filter(is_featured=True, category__slug__iregex=r'(antique|brass|clock|canvas)')[:4]
    if not featured_antiques.exists():
        featured_antiques = Product.objects.filter(is_featured=True)[:4]
    
    bestseller_plants = Product.objects.filter(category__slug__iregex=r'(plant|pot|ceramic)')[:4]
    if not bestseller_plants.exists():
        bestseller_plants = Product.objects.filter(is_bestseller=True)[:4]

    categories = Category.objects.all()
    reviews = Review.objects.all()[:6]
    new_arrivals = Product.objects.filter(is_new_arrival=True)[:4]

    context = {
        'featured_antiques': featured_antiques,
        'bestseller_plants': bestseller_plants,
        'categories': categories,
        'reviews': reviews,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'store/index.html', context)

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Category Filter
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Room Filter
    room = request.GET.get('room')
    if room and room != 'all':
        products = products.filter(room_type=room)

    # Search query
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(material__icontains=query) |
            Q(sku__icontains=query)
        )

    # Price Filter
    max_price = request.GET.get('max_price')
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'selected_room': room,
        'query': query,
        'sort_by': sort_by,
        'max_price': max_price,
        'total_count': products.count(),
    }
    return render(request, 'store/shop.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

def cart(request):
    return render(request, 'store/cart.html')

def checkout(request):
    if request.method == 'POST':
        customer_name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        address = request.POST.get('address')
        city = request.POST.get('city', 'Faridabad')
        state = request.POST.get('state', 'Haryana')
        pincode = request.POST.get('pincode')
        payment_method = request.POST.get('payment_method', 'COD')
        total_amount = request.POST.get('total_amount', '0')
        items_json = request.POST.get('items_json', '[]')

        order_id = f"AMF-{uuid.uuid4().hex[:6].upper()}"

        try:
            total_float = float(total_amount)
        except ValueError:
            total_float = 0.0

        order = Order.objects.create(
            order_id=order_id,
            customer_name=customer_name,
            phone=phone,
            email=email,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            total_amount=total_float,
            payment_method=payment_method,
            items_json=items_json,
        )

        return redirect('order_success', order_id=order.order_id)

    return render(request, 'store/checkout.html')

def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    items = []
    try:
        items = json.loads(order.items_json)
    except Exception:
        items = []

    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'store/order_success.html', context)

def visit_showroom(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        visit_date = request.POST.get('visit_date')
        time_slot = request.POST.get('time_slot')
        guests_count = request.POST.get('guests_count', 2)
        interest_area = request.POST.get('interest_area', 'Antiques & Artificial Plants')
        notes = request.POST.get('notes', '')

        ShowroomBooking.objects.create(
            name=name,
            phone=phone,
            email=email,
            visit_date=visit_date,
            time_slot=time_slot,
            guests_count=guests_count,
            interest_area=interest_area,
            notes=notes,
        )
        messages.success(request, 'Your VIP Showroom Visit has been scheduled! Our team in Faridabad will contact you shortly.')
        return redirect('visit_showroom')

    return render(request, 'store/visit.html')

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        inquiry_type = request.POST.get('inquiry_type', 'General Inquiry')
        message = request.POST.get('message')

        Inquiry.objects.create(
            name=name,
            phone=phone,
            email=email,
            inquiry_type=inquiry_type,
            message=message,
        )
        messages.success(request, 'Thank you! Your message has been sent to our Faridabad store team.')
        return redirect('contact')

    return render(request, 'store/contact.html')

@require_POST
def submit_inquiry_api(request):
    try:
        data = json.loads(request.body)
        Inquiry.objects.create(
            name=data.get('name', 'Anonymous'),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            inquiry_type=data.get('inquiry_type', 'Instant Lead'),
            product_name=data.get('product_name', ''),
            message=data.get('message', ''),
        )
        return JsonResponse({'status': 'success', 'message': 'Inquiry received successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
def submit_review_api(request):
    try:
        data = json.loads(request.body)
        review = Review.objects.create(
            name=data.get('name', 'Anonymous'),
            city=data.get('city', 'Faridabad'),
            rating=int(data.get('rating', 5)),
            title=data.get('title', 'Great Product!'),
            comment=data.get('comment', ''),
            product_name=data.get('product_name', 'Antique Decor & Plants'),
        )
        return JsonResponse({'status': 'success', 'message': 'Review submitted!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def api_products(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(material__icontains=query)
        )
    if category:
        products = products.filter(category__slug=category)
        
    data = [
        {
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': float(p.price),
            'original_price': float(p.original_price),
            'image_url': p.image_url,
            'category': p.category.name,
            'rating': float(p.rating),
            'sku': p.sku,
        }
        for p in products[:10]
    ]
    return JsonResponse({'products': data})
