from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # ✅ Лучше использовать это
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Генерируем slug только если он пуст
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')
    in_stock = models.PositiveIntegerField(default=0)
    country = models.CharField(max_length=100, blank=True)
    climate = models.CharField(max_length=100, blank=True)
    attractions = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='tours/')
    meal_type = models.CharField(max_length=100, blank=True)
    room_type = models.CharField(max_length=100, blank=True)
    insurance = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tours', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now) 
    latitude = models.FloatField(default=0.0, verbose_name="Широта")
    longitude = models.FloatField(default=0.0, verbose_name="Долгота")

    def __str__(self):
        return self.name
    
class TourImage(models.Model):
    tour = models.ForeignKey(
        'Tour', 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name='Тур'
    )
    image = models.ImageField(
        upload_to='tours/',
        verbose_name='Изображение'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    def __str__(self):
        return f"Изображение для тура: {self.tour.name}"

    class Meta:
        verbose_name = 'Изображение тура'
        verbose_name_plural = 'Изображения туров'
        ordering = ['-uploaded_at']


def main_image(self):
    return self.images.first().image.url if self.images.exists() else ''

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    departure_date = models.DateField(null=True, blank=True)
    nights = models.PositiveIntegerField(null=True, blank=True)
    guests = models.PositiveIntegerField(null=True, blank=True)

    def total_price(self):
        if self.product:
            return self.product.price * self.quantity
        elif self.tour:
            return self.tour.price * self.quantity
        return 0


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('cancelled', 'Отменен'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default='new', max_length=20)
    reason = models.TextField(blank=True, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    departure_date = models.DateField(null=True, blank=True)
    nights = models.PositiveIntegerField(null=True, blank=True)
    guests = models.PositiveIntegerField(null=True, blank=True)
    def total_price(self):
        if self.product:
            return self.product.price * self.quantity
        elif self.tour:
            return self.tour.price * self.quantity
        return 0

    def __str__(self):
        if self.product:
            return f"Продукт: {self.product.name} x {self.quantity}"
        elif self.tour:
            return f"Тур: {self.tour.name} x {self.quantity}"
        return "Неизвестный элемент заказа"
