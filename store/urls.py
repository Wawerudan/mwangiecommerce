# pyright: reportUnusedImport=false
# pylint: disable=unused-import

from django.urls import path
from . import views
from django.urls import path
from .views import ecommerce_bot,bot_page

urlpatterns = [
    path('api/', ecommerce_bot, name='ecommerce_bot'),
    path('', bot_page, name='bot_page'),

     path('', views.product_list, name='product_list'),
]





