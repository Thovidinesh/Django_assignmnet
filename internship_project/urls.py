from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Redirect root URL to login page
def redirect_to_login(request):
    return redirect('login')  # 'login' is the name of the login URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login),  # Redirect root URL to login page
    path('login/', include('main_app.urls')),  # Include your app URLs
]
