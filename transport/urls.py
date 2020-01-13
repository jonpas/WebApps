from django.urls import include, path

from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.TransportListView.as_view(), name='index'),
    path('<int:pk>/', views.TransportDetailView.as_view(), name='detail'),
    path('new/', views.TransportCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', views.TransportDeleteView.as_view(), name='delete'),
]
