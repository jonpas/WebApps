from django.urls import include, path

from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.TransportListView.as_view(), name='index'),
    path('<int:pk>/', views.TransportDetailView.as_view(), name='detail'),
    path('new/', views.TransportCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TransportUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TransportDeleteView.as_view(), name='delete'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile-update'),
]
