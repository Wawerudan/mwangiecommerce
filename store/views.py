
# views.py
from django.shortcuts import render, get_object_or_404,redirect
from .models import Product, Category
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.db.models import Q
from .models import Product,ProductVariant,CartItem,Cart,Wishlist
from .filters import VariantFilter

from django.core.paginator import Paginator
  # ✅ import PDF helper



def search(request):
    query = request.GET.get('q','')  # get search keyword
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        suggestions = Product.objects.filter( Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
).values_list('name', flat=True)[:10]
        return JsonResponse({'suggestions': list(suggestions)})

    # Full search mode (normal page load)

    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)| 
            Q(category__name__icontains=query)
        )
         # Get all variants for these products
        variants_qs = ProductVariant.objects.filter(product__in=products)
    else:
        products = Product.objects.all()
        variants_qs = ProductVariant.objects.all()

    # Apply VariantFilter to get filtered variants
    f = VariantFilter(request.GET, queryset=variants_qs)
    filtered_variants = f.qs

    # Available options should be based on filtered results
    available_colors = [c for c in filtered_variants.values_list('color', flat=True).distinct() if c]
    available_sizes = [s for s in filtered_variants.values_list('size', flat=True).distinct() if s]

    context = {
        'query': query,
        'products': products,
        'variants': filtered_variants,  # filtered variants
        'available_colors': available_colors,
        'available_sizes': available_sizes,
        'filter': f,
    }
    return render(request, 'store/search.html', context)
        

    
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()   # create the user
            login(request, user) # log them in immediately
            
            send_mail(
                subject="Welcome to Dan's Store!",
                message=f"Hi {user.first_name}, thanks for signing up. We're excited to have you!",
                from_email="wawerumwangidan@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, "Account created successfully!")
            return redirect("product_list")  # change "home" to your home page url name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "store/signup.html", 
                  {"form": form})
    

def product_list(request):
    shoe = Product.objects.filter(category__name="shoe")
    food = Product.objects.filter(category__name="Food")
    electronics = Product.objects.filter(category__name="Electronics")
    deals = Product.objects.filter(category__name="Deals")
    shoeformen =Product.objects.filter(category__name="shoeformen")[:7]

    # For each product, get its default variant (first variant)
    def attach_default_variant(products):
        for p in products:
            p.default_variant = p.variants.first()
        return products

    shoe = attach_default_variant(shoe)
    food = attach_default_variant(food)
    electronics = attach_default_variant(electronics)
    shoeformen = attach_default_variant(shoeformen)
    deals= attach_default_variant(deals)

    return render(request, "store/product_list.html", {
        "shoe": shoe,
        "food": food,
        "electronics": electronics,
        "shoeformen" :shoeformen,
        "deals":deals
    })
    
    

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get up to 4 related products from the same category, excluding the current product
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    return render(request, 'store/product_detail.html', {
        "product": product,
        "related_products": related_products,
    })
    


def attach_default_variant(products):
    for p in products:
        p.default_variant = p.variants.first()
    return products


def category_products(request, category_name):
    # Get the selected category
    category = get_object_or_404(Category, name=category_name)

    # Fetch all products in this category
    products = Product.objects.filter(category=category)
    products = attach_default_variant(products)
    paginator = Paginator(products, 8)  # show 6 per page

    page_number = request.GET.get('page')  # get current page number from URL
    page_obj = paginator.get_page(page_number)

    # Get all variants of those products
    variants_qs = ProductVariant.objects.filter(product__in=products)

    # Apply your VariantFilter
    f = VariantFilter(request.GET, queryset=variants_qs)
    filtered_variants = f.qs

    # Determine which products have matching variants
    filtered_product_ids = filtered_variants.values_list("product_id", flat=True).distinct()
    filtered_products = products.filter(id__in=filtered_product_ids)

    # Attach default variant to filtered ones
    filtered_products = attach_default_variant(filtered_products)

    # Get distinct available options for sidebar filters
    available_colors = [c for c in variants_qs.values_list("color", flat=True).distinct() if c]
    available_sizes = [s for s in variants_qs.values_list("size", flat=True).distinct() if s]

    return render(request, "store/category.html", {
        "category": category,
        "filter": f,
        "products": filtered_products,
        "available_colors": available_colors,
        "available_sizes": available_sizes,
        "page_obj":page_obj,
    })



def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, pk=variant_id)
    cart = get_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))

def remove_from_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, pk=variant_id)
    cart = get_cart(request)

    try:
        cart_item = CartItem.objects.get(cart=cart, variant=variant)
        cart_item.delete()  # removes the item completely
    except CartItem.DoesNotExist:
        pass  # item not found — ignore

    return redirect(request.META.get('HTTP_REFERER', '/'))

# store/views.py
def view_cart(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('variant__product')
    total = 0
    for item in cart_items:
        total += item.variant.price * item.quantity
        total = int(total)
    return render(request, 'store/cart.html',        
            {'cart': cart, 'cart_items': cart_items,
                                               'total':total})

 
@login_required
def profile(request):
    return render(request, "profile_list.html", {"user": request.user})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("product_list")  # redirect to homepage
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "store/login.html")
    return render(request, "store/login.html")

