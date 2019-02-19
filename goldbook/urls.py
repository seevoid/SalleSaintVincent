from django.urls import path, include
from . import views

urlpatterns = [
    path('goldenbook', views.goldenbook, name='goldenbook'),
]