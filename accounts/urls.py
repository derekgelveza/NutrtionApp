from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard-data/', views.dashboard_data, name='dashboard_data'),
    path('products/', views.products, name='products'),
    path('customer/', views.customer, name='customer'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registration, name='registration'),
    path('logout/', views.logout_view, name='logout'),
    path('setup/', views.user_setup, name='setup'),

]