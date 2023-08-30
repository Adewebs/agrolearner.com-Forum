from django.urls import path
from . import views

urlpatterns=[
    path('', views.getRoutes),
    path('rooms/', views.getrooms),
    path('room/<int:pk>/', views.getroom),
]