from django.urls import path , include
from . import views

app_name='shop'

urlpatterns = [
    path('',views.categories,name='index'),
    path('<int:category>',views.itemByCategory,name="itemByCategory"),
    path('item_<int:id>/',views.detail,name='detail'),
    path('checkout/',views.checkout,name='checkout'),
    path('cart/',views.userCart,name='cart'),
]