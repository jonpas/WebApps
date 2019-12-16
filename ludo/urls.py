from django.urls import include, path

from . import views

app_name = 'ludo'

urlpatterns = [
    path('', views.index, name='index'),
]
