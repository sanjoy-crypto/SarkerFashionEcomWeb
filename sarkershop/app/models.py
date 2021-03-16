from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

DIVISION = (
    ('Mymensingh', 'Mymensingh'),
    ('Rajshahi', 'Rajshahi'),
    ('Dhaka', 'Dhaka'),
    ('Chittagong', 'Chittagong'),
    ('Khulna', 'Khulna'),
    ('Barisal', 'Barisal'),
    ('Sylhet', 'Sylhet'),
    ('Rangpur', 'Rangpur'),
)


class Customer(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(null=True)
    locality = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    division = models.CharField(choices=DIVISION, max_length=50)

    def __str__(self):
        return self.name


CATEGORY = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),

)


class Product(models.Model):
    title = models.CharField(max_length=100, null=True)
    Selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100, null=True)
    category = models.CharField(choices=CATEGORY, max_length=100, null=True)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


STATUS = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS, max_length=100, default='Pending', null=True)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
