from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from servicos import views as servicos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', include('clientes.urls')),
    path('servicos/', include('servicos.urls')),
    path('dashboard/', servicos_views.dashboard, name='dashboard'),
    path('', lambda request: redirect('dashboard')),
]