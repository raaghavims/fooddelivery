from django.urls import path
from . import views



urlpatterns = [
    path("", views.marketplace, name="marketplace"),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    #ADD TO CART 
    path('add_to_cart/<int:foodid>/', views.add_to_cart, name='add_to_cart'),
    #REMOVE FROM CART
    path('decrease_cart/<int:foodid>/', views.decrease_cart, name='decrease_cart'),

    #DELETE CART ITEM
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),

    
]