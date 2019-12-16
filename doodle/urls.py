from django.urls import include, path

from . import views

app_name = 'doodle'

urlpatterns = [
    path('', views.index, name='index'),
]
