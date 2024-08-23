from django.urls import path
from django.conf import settings
from .views import SignUpView, CustomPasswordChangeView, ProfilePageView,ProfileUpdateView, CustomPasswordResetView, CustomLoginView, logout_view

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfilePageView.as_view(), name='profile_view'),
    path('profile_edit/<int:pk>/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logoutt/', logout_view, name='logout'),
    

]