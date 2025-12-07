from django.contrib import admin
from django.urls import path, include
from gamification.views import CustomTokenCreateView, CustomTokenDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gamification.urls')), # localhost:8000/api/users/
    path('auth/', include('djoser.urls')), # localhost:8000/auth/users/ (Sign up)
    path('auth/token/login/', CustomTokenCreateView.as_view(), name='login'), # localhost:8000/auth/token/login
    path('auth/token/logout/', CustomTokenDestroyView.as_view(), name='logout'), # localhost:8000/auth/token/logout
]
