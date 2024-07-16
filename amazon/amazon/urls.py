"""
URL configuration for amazon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

# import for media urls 
from django.conf import settings
from django.conf.urls.static import static
from . import views

#  product import 
from products import views as product_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    
    #  custom admin pannel
    
    path('admin/', views.admin_panel),
    path('admin/product/add/', views.add_product),
    path('admin/product/view/', views.view_products),
    path('admin/product/edit_product/<int>', views.edit_product,),
    path('admin/product/delete/<int>', views.delete),
    
    #  user auth urls
    
    path('login', views.user_login),
    path('register', views.user_register),
    path('logout', views.user_logout),
    path('user/general', views.generel_settings),
    path('user/order-history',views.order_history),
    
    # product urls
    
    path('', product_views.home),
    path('category/<str>', product_views.filter_category),
    path('sort/<sort_value>', product_views.sort_by_price),
    path('search', product_views.search_by_price),
    path('order/<payment_id>/<amount>',product_views.order),
    
    #  cart urls 
    
    path('add_to_cart/<product_id>/', product_views.add_to_cart),
    path('cart/', product_views.cart),
    path('cart/delete/<cart_id>', product_views.delete),
    path('cart/update/<update>/<cart_id>', product_views.cart_update),
]
# media urls 
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)