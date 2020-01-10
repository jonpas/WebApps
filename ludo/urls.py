from django.urls import path

from . import views

app_name = 'ludo'

urlpatterns = [
    path('', views.RoomListView.as_view(), name='index'),
    path('<int:pk>/', views.RoomDetailView.as_view(), name='room'),
    path('new/', views.RoomCreateView.as_view(), name='room-create'),
    path('<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room-delete'),
]
