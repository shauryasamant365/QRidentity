from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='birthday_index'),
    path('add/', views.add, name='birthday_add'),
]