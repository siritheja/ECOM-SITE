from django.contrib import admin
from .models import Product, OrderHead, OrderDetail, UserCart, Category
# Register your models here.
admin.site.register(Product)
admin.site.register(OrderHead)
admin.site.register(OrderDetail)
admin.site.register(UserCart)
admin.site.register(Category)