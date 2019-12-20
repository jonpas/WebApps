from django.urls import include, path

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tags/new/', views.TagCreateView.as_view(), name='tag-create'),
    path('tags/<int:pk>/edit/', views.TagUpdateView.as_view(), name='tag-update'),
    path('tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag-delete'),
    path('lists/new/', views.ListCreateView.as_view(), name='list-create'),
    path('lists/<int:pk>/edit/', views.ListUpdateView.as_view(), name='list-update'),
    path('lists/<int:pk>/delete/', views.ListDeleteView.as_view(), name='list-delete'),
    path('tasks/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/new/<int:list>/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
]
