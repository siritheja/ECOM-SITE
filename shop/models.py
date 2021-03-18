from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category/')
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    disc_price = models.FloatField()
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    description = models.TextField()
    image = models.ImageField(default='product/default.jpg',upload_to='product/')
    def __str__(self):
        return self.name

class OrderHead(models.Model):
    order_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    amount = models.FloatField(null=True)

class OrderDetail(models.Model):
    order_id = models.IntegerField()
    items = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()    

class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

class Counter(models.Model):
    counter_val = models.SmallIntegerField()
    total_max_counter = models.SmallIntegerField()