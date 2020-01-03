from django.urls import path

from . import views

app_name = 'doodle'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
