from django.urls import include, path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/<int:pk>/', views.UserDetailView.as_view(), name='profile'),
    path('accounts/<int:pk>/edit/', views.UserUpdateView.as_view(), name='profile-update'),
    path('accounts/register/', views.UserCreateView.as_view(), name='register'),
]
