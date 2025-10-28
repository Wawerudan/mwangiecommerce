"""
URL configuration for Dan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from store import views
from store.payment import mpesa
from django.urls import path, include





urlpatterns = [ 
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('search/', views.search, name='search'),
    path('', views.product_list, name='product_list'),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("profile/",views.profile,name='profile'),
    path("login/", views.login_view, name='login'),
    path("signup/", views.signup_view, name='signup'), 
    path('stkpush/', mpesa.lipa_na_mpesa_online, name='stkpush'),
    path('stk_callback/', mpesa.stk_callback, name='stk_callback'),
    path('admin/', admin.site.urls),
     path('products/<int:product_id>/', views.product_detail, name='product_detail'),
      path('cart/add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path("remove-from-cart/<int:variant_id>/", views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),


]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)