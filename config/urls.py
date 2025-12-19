from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from presupuestos.views import dashboard

# Vista para redirigir el login
def login_redirect(request):
    """Redirige al dashboard cuando intentan acceder a login"""
    return redirect('dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('presupuestos/', include('presupuestos.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    
    # ¡IMPORTANTE! Añade esta línea que falta:
    path('accounts/login/', login_redirect, name='login'),
    
    path('', lambda request: redirect('dashboard'), name='home'),
]