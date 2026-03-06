from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from students import views  # Мы импортируем views ТОЛЬКО из students

urlpatterns = [
    path('admin/', admin.site.urls),
    # Change the empty string '' to 'students/'
    path('students/', include('students.urls')), 
    
    # You might want to move these inside students/urls.py eventually,
    # but for now, they will stay at the root level (e.g., /register/)
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)