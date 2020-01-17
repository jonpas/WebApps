from django.urls import path

from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.TransportListView.as_view(), name='index'),
    path('search/', views.TransportFilterView.as_view(), name='search'),
    path('<int:pk>/', views.TransportDetailView.as_view(), name='detail'),
    path('new/', views.TransportCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TransportUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TransportDeleteView.as_view(), name='delete'),
    path('<int:pk>/reserve/', views.TransportReserveView.as_view(), name='reserve'),
    path('<int:pk>/cancel/', views.TransportCancelView.as_view(), name='cancel'),
    path('<int:pk>/confirm/', views.TransportConfirmView.as_view(), name='confirm'),
    path('<int:pk>/depart/', views.TransportDepartView.as_view(), name='depart'),
    path('<int:pk>/complete/', views.TransportCompleteView.as_view(), name='complete'),
    path('<int:pk>/rate/<int:user>', views.TransportRateView.as_view(), name='rate'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile-update'),
]
