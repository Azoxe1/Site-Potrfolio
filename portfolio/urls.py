"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from shop.api import *
from shop.views import *
from feedback.views import contact
from app_loging.views import *

from portfolio.views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    #reset_password_test
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
          name ='password_reset_confirm'),
    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
         name ='password_reset_done'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name ='password_reset_complete'),
    #base
    path('', base, name='base'),
    path('admin/', admin.site.urls),
    #админка
    path('baton/', include('baton.urls')),
    #auth
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    #projects
    path('projects/', projects, name='projects'),
    path('contact_form/', contact, name='contact_form'),
    path('lk/', lk, name='lk'),
    path('', include('social_django.urls', namespace='social')),
    #shop
    path('shop/', index, name='shop'),
    path('category/', category_list, name='category'),
    path('category/<title>/', product_list_view, name='product_list_view'),
    path('product/<title>/', product_view, name='product_view'),
    path('review/<title>/', add_review, name='add_review'),
    # path('add_cat/', add_category, name='add_category'),
    path('cart/', include('cart.urls')),
    ####API methods#########
    path('api/v1/projects/', ProjectsView.as_view(), name='api_projects'),
    path('api/v1/products/', ProductsView.as_view(), name='api_projects'),
    path('api/v1/categories/', CategoriesView.as_view(), name='api_projects'),
    ####API AUTH methods#########
      path('api/v1/drf-auth/', include('rest_framework.urls')),
      path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/registration/', RegisterAccount.as_view(), name='api_reg'),
    path('api/v1/confirm/', ConfirmAccount.as_view(), name='api_conf'),
    path('api/v1/contact/', ContactView.as_view(), name='api_contact'),
    path('api/v1/details/', AccountDetails.as_view(), name='api_details'),
    path('api/v1/login/', LoginAccount.as_view(), name='api_login'),
    path('api/v1/order/', OrderView.as_view(), name='api_order'),
    path('api/v1/cart/', CartView.as_view(), name='api_cart'),
    #оптимизиция_не работает
    # path('silk/', include('silk.urls', namespace='silk'))
    #DRF
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
