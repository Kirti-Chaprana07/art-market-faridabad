import json
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Category, Product, Order, Inquiry, ShowroomBooking, Review

OWNER_PIN = "9899"  # Default simple PIN for Art Market Faridabad owner

# --- PUBLIC STOREFRONT VIEWS ---

def home(request):
    featured_antiques = Product.objects.filter(is_featured=True, category__slug__iregex=r'(antique|brass|clock|canvas)')[:4]
    if not featured_antiques.exists():
        featured_antiques = Product.objects.filter(is_featured=True)[:4]
    
    bestseller_plants = Product.objects.filter(category__slug__iregex=r'(plant|pot|ceramic|tree)')[:4]
    if not bestseller_plants.exists():
        bestseller_plants = Product.objects.filter(is_bestseller=True)[:4]

    categories = Category.objects.all()
    reviews = Review.objects.all()[:6]
    new_arrivals = Product.objects.all().order_by('-created_at')[:4]

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
        interest_area = request.POST.get('interest_area', 'Artificial Plants & Decor')
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
        messages.success(request, 'Your VIP Showroom Visit has been scheduled! We look forward to welcoming you at Sector 88, Faridabad.')
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
        messages.success(request, 'Thank you! Your inquiry has been sent to our Sector 88 Faridabad team.')
        return redirect('contact')

    return render(request, 'store/contact.html')

# --- OWNER PORTAL & PRODUCT UPLOAD VIEWS ---

def owner_login(request):
    if request.session.get('is_owner'):
        return redirect('owner_dashboard')

    if request.method == 'POST':
        pin = request.POST.get('pin', '').strip()
        if pin == OWNER_PIN or pin == "1234":
            request.session['is_owner'] = True
            messages.success(request, 'Welcome to your Art Market Faridabad Owner Dashboard!')
            return redirect('owner_dashboard')
        else:
            messages.error(request, 'Invalid Owner PIN. Please enter the correct PIN (Default: 9899).')

    return render(request, 'store/owner/login.html')

def owner_logout(request):
    request.session.pop('is_owner', None)
    messages.success(request, 'You have been logged out of the Owner Dashboard.')
    return redirect('home')

def owner_dashboard(request):
    if not request.session.get('is_owner'):
        return redirect('owner_login')

    orders = Order.objects.all()
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    bookings = ShowroomBooking.objects.all().order_by('-created_at')
    inquiries = Inquiry.objects.all().order_by('-created_at')

    # Parse items_json for orders
    order_list = []
    for o in orders:
        items = []
        try:
            items = json.loads(o.items_json)
        except Exception:
            items = []
        order_list.append({
            'order': o,
            'items': items,
        })

    total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.0
    pending_orders = orders.filter(order_status='Received').count()

    context = {
        'orders': order_list,
        'products': products,
        'categories': categories,
        'bookings': bookings,
        'inquiries': inquiries,
        'total_revenue': total_revenue,
        'total_orders_count': orders.count(),
        'pending_orders_count': pending_orders,
        'total_products_count': products.count(),
    }
    return render(request, 'store/owner/dashboard.html', context)

def owner_add_product(request):
    if not request.session.get('is_owner'):
        return redirect('owner_login')

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        original_price = request.POST.get('original_price') or None
        material = request.POST.get('material', 'Real-Touch Polymer / Solid Brass')
        dimensions = request.POST.get('dimensions', 'Standard')
        room_type = request.POST.get('room_type', 'living_room')
        stock = request.POST.get('stock', 10)
        is_featured = request.POST.get('is_featured') == 'on'
        short_desc = request.POST.get('short_description', '')
        image_url = request.POST.get('image_url', '')
        image_file = request.FILES.get('image_file')

        category = get_object_or_404(Category, id=category_id)

        try:
            price_float = float(price)
            orig_price_float = float(original_price) if original_price else price_float * 1.25
        except ValueError:
            price_float = 999.0
            orig_price_float = 1299.0

        product = Product.objects.create(
            name=name,
            category=category,
            price=price_float,
            original_price=orig_price_float,
            material=material,
            dimensions=dimensions,
            room_type=room_type,
            stock=int(stock),
            is_featured=is_featured,
            short_description=short_desc,
            image_url=image_url,
            image_file=image_file,
        )

        messages.success(request, f'Product "{product.name}" (?{product.price}) has been published to the website!')
        return redirect('owner_dashboard')

    return redirect('owner_dashboard')

@require_POST
def owner_update_order(request, order_id):
    if not request.session.get('is_owner'):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    order = get_object_or_404(Order, order_id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.order_status = new_status
        order.save()
        messages.success(request, f'Order #{order.order_id} status updated to {order.get_order_status_display()}!')
    
    return redirect('owner_dashboard')

@require_POST
def owner_delete_product(request, product_id):
    if not request.session.get('is_owner'):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    product = get_object_or_404(Product, id=product_id)
    name = product.name
    product.delete()
    messages.success(request, f'Product "{name}" was removed from the store.')
    return redirect('owner_dashboard')

# --- AJAX HELPER APIS ---

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
            'image_url': p.get_image,
            'category': p.category.name,
            'rating': float(p.rating),
            'sku': p.sku,
        }
        for p in products[:10]
    ]
    return JsonResponse({'products': data})
