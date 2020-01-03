from django.urls import path

from . import views

app_name = 'doodle'

urlpatterns = [
    path('', views.RoomListView.as_view(), name='index'),
    path('new/', views.RoomCreateView.as_view(), name='room-create'),
    path('<int:pk>/', views.RoomDetailView.as_view(), name='room'),
]
