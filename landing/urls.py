from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('paypal_success', views.paypal_success, name='paypal_success'),
    path('set_price', views.set_price, name='set_price'),
]