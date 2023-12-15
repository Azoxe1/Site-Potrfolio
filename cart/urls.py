from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from portfolio import settings
from .views import *

urlpatterns = [
    path('', cart_summary, name='cart_summary'),
    path('add/', cart_add, name='cart_add'),
    # path('delete/', views.cart_delete, name='cart_delete'),
    # path('update/', views.cart_update, name='cart_update'),

]