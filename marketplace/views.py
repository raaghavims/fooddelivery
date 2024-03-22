from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .context_processors import get_cart_amount, get_cart_counter
from .models import Cart
from menu.models import Category, FoodItem
from django.contrib.auth.decorators import login_required

from vendor.models import Vendor
from django.db.models import Prefetch

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def add_to_cart(request, foodid):
    if request.user.is_authenticated:
        if is_ajax(request):
            #check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=foodid)
                # check if user already added the same food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #increase cart item quantity
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased cart quantity', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amount(request)})
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added item to the cart', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'}) 
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'}) 
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in to continue'})
    

def decrease_cart(request, foodid):
    if request.user.is_authenticated:
        if is_ajax(request):
            #check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=foodid)
                # check if user already added the same food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #decrease cart item quantity
                    if checkCart.quantity > 1:
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amount(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'}) 
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'}) 
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in to continue'})
    

def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

@login_required(login_url='login')
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amount(request)})
            except:
                 return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist!'}) 
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})