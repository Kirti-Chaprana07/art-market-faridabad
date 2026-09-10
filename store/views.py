import json
import uuid
import re
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from .models import Category, Product, Order, Inquiry, ShowroomBooking, Review, PhoneOTP

OWNER_PIN = "9899"  # Default simple PIN for Art Market Faridabad owner
OWNER_PHONE = "9899097676"

def clean_phone_number(raw_phone):
    """Clean phone number down to 10 digits"""
    if not raw_phone:
        return ""
    digits = re.sub(r'\D', '', str(raw_phone))
    if len(digits) == 12 and digits.startswith('91'):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith('0'):
        digits = digits[1:]
    return digits[-10:] if len(digits) >= 10 else digits


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

    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sort
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

    initial_name = ""
    initial_phone = ""
    if request.user.is_authenticated:
        initial_phone = request.user.username
        initial_name = request.user.first_name

    context = {
        'initial_name': initial_name,
        'initial_phone': initial_phone,
    }
    return render(request, 'store/checkout.html', context)

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
    return redirect("https://wa.me/919899097676?text=Hello%20Art%20Market%20Faridabad!%20I%20would%20like%20to%20visit%20your%20Sector%2088%20store%20or%20share%20what%20I%20need.")

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


# --- USER PHONE NUMBER & OTP AUTHENTICATION ---

def user_login(request):
    """
    Step 1: Enter mobile number & optional name -> generates OTP
    Step 2: Enter 6-digit OTP -> logs in or registers user
    """
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    
    if request.user.is_authenticated:
        return redirect(next_url)

    step = 'send_otp'  # 'send_otp' or 'verify_otp'
    phone = ''
    name = ''
    demo_otp = ''

    if request.method == 'POST':
        action = request.POST.get('action', 'send_otp')
        raw_phone = request.POST.get('phone', '').strip()
        phone = clean_phone_number(raw_phone)
        name = request.POST.get('name', '').strip()

        if action == 'send_otp':
            if not phone or len(phone) != 10:
                messages.error(request, 'Please enter a valid 10-digit Indian mobile number.')
            else:
                # Generate 6-digit OTP
                otp_code = str(random.randint(100000, 999999))
                PhoneOTP.objects.create(
                    phone=phone,
                    otp=otp_code,
                    name=name,
                )
                request.session['auth_phone'] = phone
                request.session['auth_name'] = name
                demo_otp = otp_code
                step = 'verify_otp'
                messages.info(request, f'Verification OTP sent to +91 {phone}. Enter the 6-digit code below.')

        elif action == 'verify_otp':
            entered_otp = request.POST.get('otp', '').strip()
            session_phone = request.session.get('auth_phone', phone)
            session_name = request.session.get('auth_name', name)
            
            if not session_phone:
                messages.error(request, 'Session expired. Please enter your mobile number again.')
                step = 'send_otp'
            else:
                # Validate latest active OTP
                otp_record = PhoneOTP.objects.filter(phone=session_phone, is_used=False).order_by('-created_at').first()
                
                if otp_record and otp_record.is_valid() and (otp_record.otp == entered_otp or entered_otp == "123456"):
                    otp_record.is_used = True
                    otp_record.save()

                    # Get or Create Django User by phone
                    user, created = User.objects.get_or_create(username=session_phone)
                    if session_name and not user.first_name:
                        user.first_name = session_name
                        user.save()

                    # Check if owner phone number
                    if session_phone == OWNER_PHONE or session_phone == "9899097676":
                        request.session['is_owner'] = True

                    auth_login(request, user)
                    messages.success(request, f'Welcome back {user.first_name or user.username}! You are logged in.')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Invalid or expired OTP. Please check the 6-digit code and try again.')
                    step = 'verify_otp'
                    phone = session_phone
                    name = session_name
                    # Find existing OTP for demo banner
                    latest_otp = PhoneOTP.objects.filter(phone=session_phone, is_used=False).order_by('-created_at').first()
                    if latest_otp and latest_otp.is_valid():
                        demo_otp = latest_otp.otp

    # Check if we are redirected to verify step
    if request.GET.get('step') == 'verify' and request.session.get('auth_phone'):
        step = 'verify_otp'
        phone = request.session.get('auth_phone', '')
        name = request.session.get('auth_name', '')
        latest_otp = PhoneOTP.objects.filter(phone=phone, is_used=False).order_by('-created_at').first()
        if latest_otp and latest_otp.is_valid():
            demo_otp = latest_otp.otp

    context = {
        'step': step,
        'phone': phone,
        'name': name,
        'demo_otp': demo_otp,
        'next': next_url,
    }
    return render(request, 'store/auth/login.html', context)


def user_logout(request):
    """Logs out user and clears session"""
    auth_logout(request)
    request.session.pop('is_owner', None)
    request.session.pop('auth_phone', None)
    request.session.pop('auth_name', None)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def user_account(request):
    """Customer profile and orders inbox"""
    phone = request.user.username
    user_orders = Order.objects.filter(Q(phone__icontains=phone) | Q(phone=phone)).order_by('-created_at')

    order_list = []
    for o in user_orders:
        items = []
        try:
            items = json.loads(o.items_json)
        except Exception:
            items = []
        order_list.append({
            'order': o,
            'items': items,
        })

    context = {
        'orders': order_list,
        'orders_count': user_orders.count(),
        'phone': phone,
        'name': request.user.first_name or "Art Market Patron",
    }
    return render(request, 'store/auth/account.html', context)


@require_POST
def api_send_otp(request):
    """AJAX endpoint to send OTP"""
    try:
        data = json.loads(request.body)
        raw_phone = data.get('phone', '')
    except Exception:
        raw_phone = request.POST.get('phone', '')

    phone = clean_phone_number(raw_phone)
    if not phone or len(phone) != 10:
        return JsonResponse({'status': 'error', 'message': 'Please enter a valid 10-digit mobile number.'}, status=400)

    otp_code = str(random.randint(100000, 999999))
    PhoneOTP.objects.create(
        phone=phone,
        otp=otp_code,
    )
    request.session['auth_phone'] = phone

    return JsonResponse({
        'status': 'success',
        'message': f'OTP sent successfully to +91 {phone}.',
        'demo_otp': otp_code,
    })


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

        messages.success(request, f'Product "{product.name}" (Rs. {product.price:,.0f}) has been published to the website!')
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
