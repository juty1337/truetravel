from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_redirect, name='root_redirect'), 
    path('main/', views.main_page, name='main'),

    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),


    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('cart/', views.cart_view, name='cart'),


    path('add-to-cart/<int:tour_id>/', views.add_tour_to_cart, name='add_to_cart'),
    #path('add-tour-to-cart/<int:pk>/', views.add_tour_to_cart, name='add_tour_to_cart'),

    path('make-order/', views.make_order, name='make_order'),
    path('orders/', views.orders_view, name='orders'),

    path('checkout/', views.checkout, name='checkout'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('cart/add/<int:tour_id>/', views.add_tour_to_cart, name='add_tour_to_cart'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
]   
