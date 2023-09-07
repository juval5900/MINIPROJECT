from django.urls import path
from USERAPP import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('index/',views.index, name='index'),
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('loggout',views.loggout,name='loggout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('check_email/', views.check_email, name='check_email'),
    path('check_username/', views.check_username, name='check_username'),
    path('notifications',views.notifications,name='notifications'),
    path('error',views.error,name='error'),
    path('account',views.account,name='account'),
    path('charts',views.charts,name='charts'),
    path('docs',views.docs,name='docs'),
    path('help',views.help,name='help'),
    path('orders',views.orders,name='orders'),
    path('settings',views.settings,name='settings'),
    path('add_product/', views.add_product, name='add_product'),
    path('list_products/', views.list_products, name='list_products'),
    path('accounts/', include('allauth.urls')),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update-product/<int:product_id>/', views.update_product, name='update-product'),
    path('get-product-details/<int:product_id>/', views.get_product_details, name='get-product-details'),
]