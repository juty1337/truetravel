from django.shortcuts import render, redirect, get_object_or_404, render
from .models import *
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from django.db.models import Q
from django.utils.timezone import now
from rest_framework import viewsets
from .models import Tour, Category, Order
from .serializers import TourSerializer, CategorySerializer, OrderSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Tour

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'shop/tour_detail.html', {'tour': tour})


def main_redirect(request):
    return redirect('main')







def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def about(request):
    return render(request, 'shop/about.html')

def contacts(request):
    return render(request, 'shop/contacts.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'shop/login.html')

def logout_view(request):
    logout(request)
    return redirect('about')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.tour.price * item.quantity for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def checkout(request):
    CartItem.objects.filter(user=request.user).delete()
    return redirect('main')





@login_required
def add_tour_to_cart(request, tour_id):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, pk=tour_id)
        quantity = int(request.POST.get('quantity', 1))
        departure_date = request.POST.get('departure_date')
        nights = request.POST.get('nights')
        guests = request.POST.get('guests')

        # Создаём элемент корзины в БД
        CartItem.objects.create(
            user=request.user,
            tour=tour,
            quantity=quantity,
            departure_date=departure_date,
            nights=nights,
            guests=guests,
        )
        return redirect('cart')



@login_required
def make_order(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if not request.user.check_password(password):
            messages.error(request, 'Неверный пароль')
            return redirect('cart')

        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, 'Корзина пуста')
            return redirect('cart')

        order = Order.objects.create(user=request.user)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                tour=item.tour,
                quantity=item.quantity,
                departure_date=item.departure_date,
                nights=item.nights,
                guests=item.guests,
            )

            # Обновляем остаток для продуктов
            if item.product:
                item.product.in_stock -= item.quantity
                item.product.save()

        cart_items.delete()
        messages.success(request, 'Заказ оформлен!')
        return redirect('orders')
    return redirect('cart')


def main_page(request):
    category_slug = request.GET.get('category')
    sort_option = request.GET.get('sort')

    tours = Tour.objects.all()

    # Фильтрация по категории по slug
    if category_slug:
        tours = tours.filter(category__slug=category_slug)

    # Сортировка
    if sort_option == 'year':
        tours = tours.order_by('-created_at') 
    elif sort_option in ['name', 'price']:
        tours = tours.order_by(sort_option)

    categories = Category.objects.all()

    cart_items = []
    total_price = 0

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)

    context = {
        'best_tours': tours,
        'categories': categories,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'shop/main.html', context)





@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/orders.html', {'orders': orders})




class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


def about(request):
    latest_tours = Tour.objects.order_by('-id')[:5]
    return render(request, 'shop/about.html', {'latest_tours': latest_tours})

def contacts(request):
    return render(request, 'shop/contacts.html')